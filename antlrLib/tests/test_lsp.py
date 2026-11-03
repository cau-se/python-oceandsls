#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Tests for the shared language server infrastructure in :mod:`odsllib.lsp`."""

from typing import List

import pytest
from antlr4 import Token
from lsprotocol.types import (
    CompletionItemKind, CompletionParams, DiagnosticSeverity, DidChangeTextDocumentParams, DidCloseTextDocumentParams,
    DidOpenTextDocumentParams, Position, SemanticTokensParams, TextDocumentIdentifier, TextDocumentItem,
    VersionedTextDocumentIdentifier, TextDocumentContentChangeEvent_Type2,
)
from lsprotocol.types import ClientCapabilities, InitializeParams

from odsllib.lsp import (
    CaretPosition, encode_semantic_tokens, find_caret_token, find_context_for_token, keyword_items, parse_source,
    collect_candidates, compute_caret_token_position, compute_token_position, token_range,
)
from odsllib.lsp.server import AntlrLanguageServer
from tests.gen.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from tests.gen.TestExprCore.TestExprCoreParser import TestExprCoreParser


def parse(text: str):
    return parse_source(text, TestExprCoreLexer, TestExprCoreParser, "expression", diagnostic_source="test")


# ---------------------------------------------------------------------------------------------------------------------
# Parsing and diagnostics
# ---------------------------------------------------------------------------------------------------------------------

class TestParsing:
    def test_valid_input_has_no_diagnostics(self):
        result = parse("var c = a + b()")
        assert result.diagnostics == []
        assert not result.has_errors
        assert result.tree.getText() == "varc=a+b()"

    def test_syntax_error_is_reported_with_lsp_coordinates(self):
        result = parse("var c = \n a + )")
        assert result.has_errors
        diagnostic = result.diagnostics[0]
        assert diagnostic.severity == DiagnosticSeverity.Error
        assert diagnostic.source == "test"
        # ')' is on the second line (0-based line 1), column 5
        assert diagnostic.range.start == Position(line=1, character=5)
        assert diagnostic.range.end == Position(line=1, character=6)

    def test_lexer_error_is_reported(self):
        result = parse("a # b")
        assert any("token recognition error" in d.message for d in result.diagnostics)

    def test_trailing_input_is_reported(self):
        """The start rule does not end with EOF; unconsumed input used to be ignored silently."""
        result = parse("var c = a b")
        assert len(result.diagnostics) == 1
        assert "stopped before the end" in result.diagnostics[0].message
        assert result.diagnostics[0].range.start == Position(line=0, character=10)

    def test_trailing_input_check_can_be_disabled(self):
        result = parse_source("var c = a b", TestExprCoreLexer, TestExprCoreParser, "expression", require_eof=False)
        assert result.diagnostics == []

    def test_error_range_covers_the_offending_token(self):
        result = parse("var 12abc")
        assert result.diagnostics, "expected an error"
        assert all(d.range.end.character > d.range.start.character for d in result.diagnostics)

    def test_token_range_without_token(self):
        rng = token_range(None, 3, 4)
        assert (rng.start.line, rng.start.character, rng.end.character) == (2, 4, 5)


# ---------------------------------------------------------------------------------------------------------------------
# Caret handling
# ---------------------------------------------------------------------------------------------------------------------

class TestCaret:
    TEXT = "var c = a + b()"

    @pytest.mark.parametrize("column, expected_text", [
        (0, "var"),   # start of the keyword
        (2, "var"),   # inside the keyword
        (3, "var"),   # directly behind the keyword
        (5, "c"),     # behind the identifier
        (11, "b"),    # behind the operator (not a word): the next token is used
    ])
    def test_find_caret_token(self, column, expected_text):
        result = parse(self.TEXT)
        index = find_caret_token(result.tokens, CaretPosition(1, column))
        assert result.tokens.get(index).text == expected_text

    def test_caret_in_whitespace_selects_next_token(self):
        result = parse(self.TEXT)
        index = find_caret_token(result.tokens, CaretPosition(1, 7))  # between '=' and ' a'? '=' ends at 7
        assert result.tokens.get(index).text in ("=", "a")
        index = find_caret_token(result.tokens, CaretPosition(1, 8))
        assert result.tokens.get(index).text == "a"

    def test_caret_after_last_token_selects_eof(self):
        result = parse("var c = a ")
        index = find_caret_token(result.tokens, CaretPosition(1, 10))
        assert result.tokens.get(index).type == Token.EOF

    def test_caret_on_later_line(self):
        result = parse("var c =\n  a")
        index = find_caret_token(result.tokens, CaretPosition(2, 3))
        assert result.tokens.get(index).text == "a"

    def test_prefix_and_context(self):
        result = parse("var c = alpha")
        position = compute_caret_token_position(result.tree, result.tokens, CaretPosition(1, 10))
        assert position.text == "al"
        assert result.tokens.get(position.index).text == "alpha"
        assert isinstance(position.context, TestExprCoreParser.IdentifierContext)

    def test_find_context_outside_tree(self):
        result = parse("a")
        assert find_context_for_token(result.tree, 99) is None
        assert find_context_for_token(None, 0) is None

    def test_legacy_compute_token_position(self):
        result = parse("var c = a + b()")
        position = compute_token_position(result.tree, result.tokens, CaretPosition(1, 9))
        assert position is not None
        assert result.tokens.get(position.index).text == "a"
        assert position.text == "a"


# ---------------------------------------------------------------------------------------------------------------------
# Completion and semantic tokens
# ---------------------------------------------------------------------------------------------------------------------

class TestCompletion:
    def test_operator_candidates(self):
        result = parse("var c = a ")
        index = find_caret_token(result.tokens, CaretPosition(1, 10))
        items = keyword_items(result.parser, collect_candidates(result.parser, index))
        labels = {i.label for i in items}
        assert {"+", "-", "*", "/", "("} <= labels
        assert all(i.kind == CompletionItemKind.Operator for i in items)

    def test_symbolic_tokens_are_not_suggested(self):
        result = parse("")
        items = keyword_items(result.parser, collect_candidates(result.parser, 0))
        # VAR, LET and ID have no literal names and must not appear as "<INVALID>" or similar
        assert all(i.label not in ("VAR", "LET", "ID", "<INVALID>") for i in items)

    def test_prefix_filter(self):
        result = parse("var c = a ")
        index = find_caret_token(result.tokens, CaretPosition(1, 10))
        items = keyword_items(result.parser, collect_candidates(result.parser, index), prefix="*")
        assert [i.label for i in items] == ["*"]

    def test_semantic_tokens_encoding(self):
        result = parse("var c =\n a + b()")
        data = encode_semantic_tokens(result.parser, result.tokens)
        assert len(data) % 5 == 0
        entries = [data[i:i + 5] for i in range(0, len(data), 5)]
        # '=' on line 0, column 6 is the first classified token (an operator, legend index 4)
        assert entries[0] == [0, 6, 1, 4, 0]
        # '+' on the next line: delta line 1, absolute column 3
        assert entries[1] == [1, 3, 1, 4, 0]


# ---------------------------------------------------------------------------------------------------------------------
# Base server
# ---------------------------------------------------------------------------------------------------------------------

class ExprServer(AntlrLanguageServer):
    lexer_class = TestExprCoreLexer
    parser_class = TestExprCoreParser
    start_rule = "expression"
    preferred_rules = {TestExprCoreParser.RULE_variableRef}

    def __init__(self):
        super().__init__("expr-test-server", "0.1")
        self.saved: List[str] = []

    def semantic_diagnostics(self, result, uri):
        if "boom" in result.source:
            raise RuntimeError("broken check")
        return []

    def symbol_completions(self, result, position, candidates, uri):
        from lsprotocol.types import CompletionItem
        if TestExprCoreParser.RULE_variableRef in candidates.rules:
            return [CompletionItem(label=name) for name in ("alpha", "beta")]
        return []

    def document_saved(self, uri, result):
        self.saved.append(uri)


@pytest.fixture(name="server")
def server_fixture():
    srv = ExprServer()
    srv.capabilities = srv.lsp.lsp_initialize(
        InitializeParams(process_id=None, root_uri=None, capabilities=ClientCapabilities())).capabilities
    published = []
    srv.publish_diagnostics = lambda uri, diagnostics, *a, **k: published.append((uri, diagnostics))
    srv.show_message = lambda *a, **k: None
    srv.published = published
    return srv


URI = "file:///tmp/test.expr"


def open_doc(server, text):
    server.lsp.workspace.put_text_document(TextDocumentItem(uri=URI, language_id="expr", version=1, text=text))
    server.on_did_open(DidOpenTextDocumentParams(
        text_document=TextDocumentItem(uri=URI, language_id="expr", version=1, text=text)))


class TestBaseServer:
    def test_did_open_publishes_syntax_errors(self, server):
        open_doc(server, "var c = )")
        uri, diagnostics = server.published[-1]
        assert uri == URI and len(diagnostics) >= 1
        assert diagnostics[0].source == "expr-test-server"

    def test_did_change_republishes(self, server):
        open_doc(server, "var c = )")
        server.lsp.workspace.update_text_document(
            VersionedTextDocumentIdentifier(uri=URI, version=2),
            TextDocumentContentChangeEvent_Type2(text="var c = a"))
        server.on_did_change(DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(uri=URI, version=2),
            content_changes=[TextDocumentContentChangeEvent_Type2(text="var c = a")]))
        assert server.published[-1] == (URI, [])

    def test_failing_semantic_check_keeps_syntax_diagnostics(self, server):
        open_doc(server, "var boom = )")
        assert server.published[-1][1], "syntax error must still be published"

    def test_did_close_clears_diagnostics(self, server):
        open_doc(server, "var c = )")
        server.on_did_close(DidCloseTextDocumentParams(text_document=TextDocumentIdentifier(uri=URI)))
        assert server.published[-1] == (URI, [])
        assert URI not in server.parse_results

    def test_completion_merges_keywords_and_symbols(self, server):
        open_doc(server, "var c = ")
        result = server.on_completion(CompletionParams(
            text_document=TextDocumentIdentifier(uri=URI), position=Position(line=0, character=8)))
        labels = [i.label for i in result.items]
        assert "alpha" in labels and "beta" in labels

    def test_completion_filters_by_typed_prefix(self, server):
        result = server.complete(URI, "var c = al", Position(line=0, character=10))
        assert [i.label for i in result.items] == ["alpha"]

    def test_semantic_tokens_handler(self, server):
        open_doc(server, "var c = a")
        tokens = server.on_semantic_tokens(SemanticTokensParams(text_document=TextDocumentIdentifier(uri=URI)))
        assert tokens.data == [0, 6, 1, 4, 0]

    def test_capabilities_are_advertised(self, server):
        caps = server.capabilities
        assert caps.completion_provider is not None
        assert caps.semantic_tokens_provider.legend.token_types[0] == "keyword"
        assert "registerCompletions" in caps.execute_command_provider.commands

    def test_features_are_registered(self, server):
        from lsprotocol.types import TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL
        features = server.lsp.fm.features
        for method in (TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL):
            assert method in features
        assert {"registerCompletions", "unregisterCompletions"} <= set(server.lsp.fm.commands)

    def test_unregister_uses_registration_id(self, server):
        import asyncio
        calls = []

        async def fake_register(params):
            calls.append(("register", params.registrations[0].id))

        async def fake_unregister(params):
            calls.append(("unregister", params.unregisterations[0].id))

        server.register_capability_async = fake_register
        server.unregister_capability_async = fake_unregister
        asyncio.run(server.register_completions())
        asyncio.run(server.unregister_completions())
        assert calls[0][1] == calls[1][1]
