#  Copyright (c) 2023-2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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

import asyncio
from typing import List
from unittest import TestCase

from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, ClientCapabilities, CompletionItem, CompletionItemKind,
    CompletionParams, DiagnosticSeverity, DidChangeTextDocumentParams, DidCloseTextDocumentParams,
    DidOpenTextDocumentParams, InitializeParams, Position, SemanticTokensParams, TextDocumentContentChangeEvent_Type2,
    TextDocumentIdentifier, TextDocumentItem, VersionedTextDocumentIdentifier,
)
from parameterized import parameterized

from odsllib.lsp import (
    CaretPosition, collect_candidates, compute_caret_token_position, compute_token_position, encode_semantic_tokens,
    find_caret_token, find_context_for_token, keyword_items, parse_source, token_range,
)
from odsllib.lsp.server import AntlrLanguageServer
from tests.gen.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from tests.gen.TestExprCore.TestExprCoreParser import TestExprCoreParser

OPERATORS = ["(", "*", "+", "-", "/"]
OPERATOR_TOKEN = [4, 0]  # semantic token type 'operator' (legend index 4), no modifiers


def parse(text: str, require_eof: bool = True):
    return parse_source(text, TestExprCoreLexer, TestExprCoreParser, "expression", diagnostic_source="test",
                        require_eof=require_eof)


def ranges(diagnostics):
    return [((d.range.start.line, d.range.start.character), (d.range.end.line, d.range.end.character))
            for d in diagnostics]


# ---------------------------------------------------------------------------------------------------------------------
# Parsing and diagnostics
# ---------------------------------------------------------------------------------------------------------------------

class TestParsing(TestCase):

    @parameterized.expand([
        ("valid_input", "var c = a + b()", True, [], []),
        # A valid assignment
        # Input: 'var c = a + b()'
        # Expected Result: no diagnostics

        ("syntax_error", "var c = \n a + )", True, ["expecting ID"], [((1, 5), (1, 6))]),
        # A syntax error is reported in LSP coordinates (0-based lines and columns)
        # Input: 'var c = ' and ' a + )' on the next line
        # Expected Result: one error at the ')' on line 1, column 5 to 6

        ("lexer_error", "a # b", True, ["token recognition error"], [((0, 2), (0, 3))]),
        # A character the lexer does not know is reported
        # Input: 'a # b'
        # Expected Result: one token recognition error at the '#'

        ("trailing_input", "var c = a b", True, ["stopped before the end"], [((0, 10), (0, 11))]),
        # The start rule does not end with EOF; unconsumed input used to be ignored silently
        # Input: 'var c = a b'
        # Expected Result: one error at the unconsumed 'b'

        ("trailing_input_check_disabled", "var c = a b", False, [], []),
        # The check for unconsumed input can be switched off
        # Input: 'var c = a b' with require_eof=False
        # Expected Result: no diagnostics

        ("error_ranges_cover_tokens", "var 12abc", True,
         ["token recognition error", "token recognition error", "expecting '='"],
         [((0, 4), (0, 5)), ((0, 5), (0, 6)), ((0, 9), (0, 10))]),
        # Every error range covers the offending token (it is never empty)
        # Input: 'var 12abc' (digits are no tokens of the test grammar)
        # Expected Result: two lexer errors for the digits and a missing '=' at the end

        ("empty_input", "", True, ["expecting {VAR, LET, ID}"], [((0, 0), (0, 1))]),
        # Empty input misses the expression
        # Input: ''
        # Expected Result: one error at the start that lists the possible tokens
    ])
    def test_diagnostics(self, test_name, text, require_eof, expected_messages, expected_ranges):
        result = parse(text, require_eof)

        self.assertEqual(len(expected_messages), len(result.diagnostics), test_name)
        self.assertEqual(bool(expected_messages), result.has_errors, test_name)
        for diagnostic, message in zip(result.diagnostics, expected_messages):
            self.assertIn(message, diagnostic.message, test_name)
            self.assertEqual(DiagnosticSeverity.Error, diagnostic.severity, test_name)
            self.assertEqual("test", diagnostic.source, test_name)
        self.assertEqual(expected_ranges, ranges(result.diagnostics), test_name)

    @parameterized.expand([
        ("assignment", "var c = a + b()", "varc=a+b()"),
        # An assignment is parsed completely
        # Input: 'var c = a + b()'
        # Expected Result: the tree text holds all tokens without whitespace

        ("expression", "a + b", "a+b"),
        # A simple expression is a valid start as well
        # Input: 'a + b'
        # Expected Result: the tree text 'a+b'

        ("trailing_input", "var c = a b", "varc=a"),
        # Unconsumed input is not part of the tree
        # Input: 'var c = a b'
        # Expected Result: the tree text without the trailing 'b'
    ])
    def test_parse_tree(self, test_name, text, expected_text):
        self.assertEqual(expected_text, parse(text).tree.getText(), test_name)

    @parameterized.expand([
        ("without_token", None, 3, 4, (2, 4, 2, 5)),
        # Without a token, the range covers one character at the 1-based line and 0-based column
        # Input: no token, line 3, column 4
        # Expected Result: line 2 (0-based), characters 4 to 5

        ("without_token_at_start", None, 1, 0, (0, 0, 0, 1)),
        # The first character of a document
        # Input: no token, line 1, column 0
        # Expected Result: line 0, characters 0 to 1

        ("without_token_far_away", None, 10, 20, (9, 20, 9, 21)),
        # A position further down in a document
        # Input: no token, line 10, column 20
        # Expected Result: line 9, characters 20 to 21

        ("with_token", 0, 1, 0, (0, 0, 0, 3)),
        # With a token, the range starts at line and column and is as long as the token
        # Input: token 0 ('var') of 'var c = a + b()', line 1, column 0
        # Expected Result: line 0, characters 0 to 3
    ])
    def test_token_range(self, test_name, token_index, line, column, expected_range):
        token = parse("var c = a + b()").tokens.get(token_index) if token_index is not None else None
        rng = token_range(token, line, column)
        self.assertEqual(expected_range, (rng.start.line, rng.start.character, rng.end.line, rng.end.character),
                         test_name)


# ---------------------------------------------------------------------------------------------------------------------
# Caret handling
# ---------------------------------------------------------------------------------------------------------------------

class TestCaret(TestCase):
    TEXT = "var c = a + b()"

    @parameterized.expand([
        ("keyword_start", TEXT, 1, 0, "var"),
        # The caret at the start of a keyword
        # Input: 'var c = a + b()', line 1, column 0
        # Expected Result: 'var'

        ("inside_keyword", TEXT, 1, 2, "var"),
        # The caret inside a keyword
        # Input: 'var c = a + b()', line 1, column 2
        # Expected Result: 'var'

        ("behind_keyword", TEXT, 1, 3, "var"),
        # The caret directly behind a keyword
        # Input: 'var c = a + b()', line 1, column 3
        # Expected Result: 'var'

        ("behind_identifier", TEXT, 1, 5, "c"),
        # The caret behind an identifier
        # Input: 'var c = a + b()', line 1, column 5
        # Expected Result: 'c'

        ("behind_operator", TEXT, 1, 11, "b"),
        # The caret behind an operator (not a word): the next token is used
        # Input: 'var c = a + b()', line 1, column 11
        # Expected Result: 'b'

        ("whitespace_behind_operator", TEXT, 1, 7, "a"),
        # The caret in the whitespace behind '=' selects the next token
        # Input: 'var c = a + b()', line 1, column 7
        # Expected Result: 'a'

        ("start_of_identifier", TEXT, 1, 8, "a"),
        # The caret at the start of an identifier
        # Input: 'var c = a + b()', line 1, column 8
        # Expected Result: 'a'

        ("after_last_token", "var c = a ", 1, 10, "<EOF>"),
        # The caret behind the last token selects the end of the input
        # Input: 'var c = a ', line 1, column 10
        # Expected Result: EOF

        ("later_line", "var c =\n  a", 2, 3, "a"),
        # The caret on a later line
        # Input: 'var c =' and '  a' on the next line, line 2, column 3
        # Expected Result: 'a'

        ("empty_document", "", 1, 0, "<EOF>"),
        # An empty document only has EOF
        # Input: '', line 1, column 0
        # Expected Result: EOF
    ])
    def test_find_caret_token(self, test_name, text, line, column, expected_text):
        result = parse(text)
        index = find_caret_token(result.tokens, CaretPosition(line, column))
        self.assertEqual(expected_text, result.tokens.get(index).text, test_name)

    @parameterized.expand([
        ("inside_identifier", "var c = alpha", 10, "al", "alpha"),
        # The text in front of the caret is the prefix of the identifier
        # Input: 'var c = alpha', column 10
        # Expected Result: prefix 'al' of the token 'alpha' in an identifier context

        ("behind_identifier", "var c = alpha", 13, "alpha", "alpha"),
        # The caret behind an identifier
        # Input: 'var c = alpha', column 13
        # Expected Result: prefix 'alpha' of the token 'alpha'

        ("start_of_identifier", "var c = alpha", 8, "", "alpha"),
        # The caret at the start of an identifier
        # Input: 'var c = alpha', column 8
        # Expected Result: an empty prefix of the token 'alpha'

        ("second_operand", "var c = a + beta", 14, "be", "beta"),
        # An identifier behind an operator
        # Input: 'var c = a + beta', column 14
        # Expected Result: prefix 'be' of the token 'beta'
    ])
    def test_compute_caret_token_position(self, test_name, text, column, expected_prefix, expected_token):
        result = parse(text)
        position = compute_caret_token_position(result.tree, result.tokens, CaretPosition(1, column))

        self.assertEqual(expected_prefix, position.text, test_name)
        self.assertEqual(expected_token, result.tokens.get(position.index).text, test_name)
        self.assertIsInstance(position.context, TestExprCoreParser.IdentifierContext, test_name)

    @parameterized.expand([
        ("token_outside_tree", "a", 99, None),
        # A token index behind the input
        # Input: the tree of 'a', token index 99
        # Expected Result: no context

        ("no_tree", None, 0, None),
        # Without a parse tree
        # Input: no tree, token index 0
        # Expected Result: no context

        ("identifier", "a", 0, TestExprCoreParser.IdentifierContext),
        # The innermost context of an identifier token
        # Input: the tree of 'a', token index 0
        # Expected Result: an identifier context

        ("assignment_operator", TEXT, 4, TestExprCoreParser.AssignmentContext),
        # A token that belongs directly to the assignment
        # Input: the tree of 'var c = a + b()', token index 4 ('=')
        # Expected Result: the assignment context
    ])
    def test_find_context_for_token(self, test_name, text, token_index, expected_class):
        tree = parse(text).tree if text is not None else None
        context = find_context_for_token(tree, token_index)
        if expected_class is None:
            self.assertIsNone(context, test_name)
        else:
            self.assertIsInstance(context, expected_class, test_name)

    @parameterized.expand([
        ("variable_reference", 9, "a", "a"),
        # The legacy function finds the token in front of the caret
        # Input: 'var c = a + b()', column 9
        # Expected Result: the token 'a' with the prefix 'a'

        ("function_reference", 13, "b", "b"),
        # A function name
        # Input: 'var c = a + b()', column 13
        # Expected Result: the token 'b' with the prefix 'b'

        ("variable_name", 5, "c", "c"),
        # The name of the assigned variable
        # Input: 'var c = a + b()', column 5
        # Expected Result: the token 'c' with the prefix 'c'

        ("keyword_start", 0, "var", ""),
        # The caret at the start of the input
        # Input: 'var c = a + b()', column 0
        # Expected Result: the token 'var' with an empty prefix
    ])
    def test_legacy_compute_token_position(self, test_name, column, expected_token, expected_prefix):
        result = parse(self.TEXT)
        position = compute_token_position(result.tree, result.tokens, CaretPosition(1, column))

        self.assertIsNotNone(position, test_name)
        self.assertEqual(expected_token, result.tokens.get(position.index).text, test_name)
        self.assertEqual(expected_prefix, position.text, test_name)


# ---------------------------------------------------------------------------------------------------------------------
# Completion and semantic tokens
# ---------------------------------------------------------------------------------------------------------------------

class TestCompletion(TestCase):

    @parameterized.expand([
        ("operators", "var c = a ", 10, "", OPERATORS),
        # Operators are suggested behind an operand
        # Input: 'var c = a ', column 10, no prefix
        # Expected Result: the operators and '(', all of kind Operator

        ("prefix_filter", "var c = a ", 10, "*", ["*"]),
        # The typed prefix filters the candidates
        # Input: 'var c = a ', column 10, prefix '*'
        # Expected Result: only '*'

        ("other_prefix", "var c = a ", 10, "+", ["+"]),
        # Another prefix
        # Input: 'var c = a ', column 10, prefix '+'
        # Expected Result: only '+'

        ("symbolic_tokens_only", "", 0, "", []),
        # VAR, LET and ID have no literal names and must not appear as '<INVALID>' or similar
        # Input: '', column 0, no prefix
        # Expected Result: no keyword items

        ("identifier_expected", "var c = a + ", 12, "", []),
        # Behind an operator only an identifier may follow
        # Input: 'var c = a + ', column 12, no prefix
        # Expected Result: no keyword items
    ])
    def test_keyword_items(self, test_name, text, column, prefix, expected_labels):
        result = parse(text)
        index = find_caret_token(result.tokens, CaretPosition(1, column))
        items = keyword_items(result.parser, collect_candidates(result.parser, index), prefix=prefix)

        self.assertEqual(expected_labels, sorted(i.label for i in items), test_name)
        self.assertTrue(all(i.kind == CompletionItemKind.Operator for i in items), test_name)

    @parameterized.expand([
        ("two_lines", "var c =\n a + b()", [[0, 6, 1, *OPERATOR_TOKEN], [1, 3, 1, *OPERATOR_TOKEN],
                                             [0, 3, 1, *OPERATOR_TOKEN], [0, 1, 1, *OPERATOR_TOKEN]]),
        # Tokens are encoded relative to the previous one
        # Input: 'var c =' and ' a + b()' on the next line
        # Expected Result: '=' at line 0, column 6, then '+' on the next line (delta 1, column 3), '(' and ')'

        ("one_operator", "var c = a", [[0, 6, 1, *OPERATOR_TOKEN]]),
        # Only operators are classified in the test grammar (its keywords have no literal names)
        # Input: 'var c = a'
        # Expected Result: the '=' only

        ("empty", "", []),
        # An empty document
        # Input: ''
        # Expected Result: no tokens

        ("parentheses", "let x = (a)", [[0, 6, 1, *OPERATOR_TOKEN], [0, 2, 1, *OPERATOR_TOKEN],
                                         [0, 2, 1, *OPERATOR_TOKEN]]),
        # Parentheses are operators as well
        # Input: 'let x = (a)'
        # Expected Result: '=', '(' and ')'
    ])
    def test_semantic_tokens_encoding(self, test_name, text, expected_entries):
        result = parse(text)
        data = encode_semantic_tokens(result.parser, result.tokens)

        self.assertEqual(0, len(data) % 5, test_name)
        self.assertEqual(expected_entries, [data[i:i + 5] for i in range(0, len(data), 5)], test_name)


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
        if TestExprCoreParser.RULE_variableRef in candidates.rules:
            return [CompletionItem(label=name) for name in ("alpha", "beta")]
        return []

    def document_saved(self, uri, result):
        self.saved.append(uri)


URI = "file:///tmp/test.expr"


class TestBaseServer(TestCase):

    def setUp(self):
        self.server = ExprServer()
        self.server.capabilities = self.server.lsp.lsp_initialize(
            InitializeParams(process_id=None, root_uri=None, capabilities=ClientCapabilities())).capabilities
        self.published = []
        self.server.publish_diagnostics = lambda uri, diagnostics, *a, **k: self.published.append((uri, diagnostics))
        self.server.show_message = lambda *a, **k: None

    def open_doc(self, text):
        self.server.lsp.workspace.put_text_document(
            TextDocumentItem(uri=URI, language_id="expr", version=1, text=text))
        self.server.on_did_open(DidOpenTextDocumentParams(
            text_document=TextDocumentItem(uri=URI, language_id="expr", version=1, text=text)))

    def change_doc(self, text):
        self.server.lsp.workspace.update_text_document(
            VersionedTextDocumentIdentifier(uri=URI, version=2), TextDocumentContentChangeEvent_Type2(text=text))
        self.server.on_did_change(DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(uri=URI, version=2),
            content_changes=[TextDocumentContentChangeEvent_Type2(text=text)]))

    @parameterized.expand([
        ("syntax_error", "var c = )", 1),
        # Opening a document publishes its syntax errors
        # Input: 'var c = )'
        # Expected Result: one diagnostic from the server

        ("valid_document", "var c = a", 0),
        # A valid document
        # Input: 'var c = a'
        # Expected Result: an empty list of diagnostics is published

        ("failing_semantic_check", "var boom = )", 1),
        # A failing semantic check keeps the syntax diagnostics
        # Input: 'var boom = )' (the test server's semantic check raises for 'boom')
        # Expected Result: the syntax error is still published

        ("failing_semantic_check_valid_syntax", "var boom = a", 0),
        # A failing semantic check of a valid document does not prevent publishing
        # Input: 'var boom = a'
        # Expected Result: an empty list of diagnostics is published

        ("empty_document", "", 1),
        # An empty document misses its expression
        # Input: ''
        # Expected Result: one diagnostic
    ])
    def test_did_open_publishes_diagnostics(self, test_name, text, expected_count):
        self.open_doc(text)
        uri, diagnostics = self.published[-1]

        self.assertEqual(URI, uri, test_name)
        self.assertEqual(expected_count, len(diagnostics), test_name)
        self.assertTrue(all(d.source == "expr-test-server" for d in diagnostics), test_name)

    @parameterized.expand([
        ("error_fixed", "var c = )", "var c = a", 0),
        # A change that fixes the error clears the diagnostics
        # Input: 'var c = )' changed to 'var c = a'
        # Expected Result: an empty list of diagnostics is published

        ("error_introduced", "var c = a", "var c = )", 1),
        # A change that introduces an error
        # Input: 'var c = a' changed to 'var c = )'
        # Expected Result: one diagnostic is published

        ("other_error", "var c = )", "var c = a b", 1),
        # A change that replaces one error with another
        # Input: 'var c = )' changed to 'var c = a b'
        # Expected Result: one diagnostic (unconsumed input) is published
    ])
    def test_did_change_republishes(self, test_name, text, changed_text, expected_count):
        self.open_doc(text)
        self.change_doc(changed_text)
        uri, diagnostics = self.published[-1]

        self.assertEqual(URI, uri, test_name)
        self.assertEqual(expected_count, len(diagnostics), test_name)

    @parameterized.expand([
        ("with_errors", "var c = )"),
        # Closing a document with errors clears them
        # Input: 'var c = )'
        # Expected Result: an empty list of diagnostics is published and the parse result is dropped

        ("valid_document", "var c = a"),
        # Closing a valid document
        # Input: 'var c = a'
        # Expected Result: an empty list of diagnostics is published and the parse result is dropped

        ("empty_document", ""),
        # Closing an empty document
        # Input: ''
        # Expected Result: an empty list of diagnostics is published and the parse result is dropped
    ])
    def test_did_close_clears_diagnostics(self, test_name, text):
        self.open_doc(text)
        self.server.on_did_close(DidCloseTextDocumentParams(text_document=TextDocumentIdentifier(uri=URI)))

        self.assertEqual((URI, []), self.published[-1], test_name)
        self.assertNotIn(URI, self.server.parse_results, test_name)

    @parameterized.expand([
        ("symbols", "var c = ", 8, ["alpha", "beta"]),
        # The completion handler merges keywords and symbols
        # Input: 'var c = ', character 8 (a variable reference may follow)
        # Expected Result: the symbols 'alpha' and 'beta'

        ("symbol_prefix", "var c = al", 10, ["alpha"]),
        # The typed prefix filters the symbols
        # Input: 'var c = al', character 10
        # Expected Result: only 'alpha'

        ("other_symbol_prefix", "var c = be", 10, ["beta"]),
        # Another prefix
        # Input: 'var c = be', character 10
        # Expected Result: only 'beta'

        ("no_match", "var c = x", 9, []),
        # A prefix that matches nothing
        # Input: 'var c = x', character 9
        # Expected Result: no items

        ("keywords", "var c = a ", 10, ["+", "-", "*", "/", "("]),
        # Behind an operand, keywords (operators) are suggested
        # Input: 'var c = a ', character 10
        # Expected Result: the operators and '('
    ])
    def test_completion(self, test_name, text, character, expected_labels):
        self.open_doc(text)
        position = Position(line=0, character=character)
        handled = self.server.on_completion(CompletionParams(text_document=TextDocumentIdentifier(uri=URI),
                                                             position=position))
        completed = self.server.complete(URI, text, position)

        self.assertEqual(expected_labels, [i.label for i in handled.items], test_name)
        self.assertEqual(expected_labels, [i.label for i in completed.items], test_name)

    @parameterized.expand([
        ("one_operator", "var c = a", [0, 6, 1, *OPERATOR_TOKEN]),
        # The handler returns the encoded tokens of the open document
        # Input: 'var c = a'
        # Expected Result: the '=' token

        ("two_operators", "var c = a + b", [0, 6, 1, *OPERATOR_TOKEN, 0, 4, 1, *OPERATOR_TOKEN]),
        # Several tokens
        # Input: 'var c = a + b'
        # Expected Result: '=' and '+'

        ("empty", "", []),
        # An empty document
        # Input: ''
        # Expected Result: no tokens
    ])
    def test_semantic_tokens_handler(self, test_name, text, expected_data):
        self.open_doc(text)
        tokens = self.server.on_semantic_tokens(SemanticTokensParams(text_document=TextDocumentIdentifier(uri=URI)))
        self.assertEqual(expected_data, tokens.data, test_name)

    @parameterized.expand([
        ("completion", lambda caps: caps.completion_provider is not None),
        # Completion is advertised
        # Input: the capabilities returned by initialize
        # Expected Result: a completion provider

        ("semantic_tokens_legend", lambda caps: caps.semantic_tokens_provider.legend.token_types[0] == "keyword"),
        # Semantic tokens are advertised with the server's legend
        # Input: the capabilities returned by initialize
        # Expected Result: the legend starts with 'keyword'

        ("commands", lambda caps: {"registerCompletions", "unregisterCompletions"}
         <= set(caps.execute_command_provider.commands)),
        # The completion commands are advertised
        # Input: the capabilities returned by initialize
        # Expected Result: 'registerCompletions' and 'unregisterCompletions'

        ("text_document_sync", lambda caps: caps.text_document_sync.open_close and caps.text_document_sync.save),
        # Document synchronisation is advertised
        # Input: the capabilities returned by initialize
        # Expected Result: open/close and save notifications
    ])
    def test_capabilities_are_advertised(self, test_name, check):
        self.assertTrue(check(self.server.capabilities), test_name)

    @parameterized.expand([
        ("completion", TEXT_DOCUMENT_COMPLETION, False),
        # The completion request is handled
        # Input: 'textDocument/completion'
        # Expected Result: a registered feature

        ("did_open", TEXT_DOCUMENT_DID_OPEN, False),
        # Opening documents is handled
        # Input: 'textDocument/didOpen'
        # Expected Result: a registered feature

        ("did_change", TEXT_DOCUMENT_DID_CHANGE, False),
        # Changes are handled
        # Input: 'textDocument/didChange'
        # Expected Result: a registered feature

        ("did_close", TEXT_DOCUMENT_DID_CLOSE, False),
        # Closing documents is handled
        # Input: 'textDocument/didClose'
        # Expected Result: a registered feature

        ("did_save", TEXT_DOCUMENT_DID_SAVE, False),
        # Saving documents is handled
        # Input: 'textDocument/didSave'
        # Expected Result: a registered feature

        ("semantic_tokens", TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, False),
        # Semantic tokens are handled
        # Input: 'textDocument/semanticTokens/full'
        # Expected Result: a registered feature

        ("register_command", "registerCompletions", True),
        # The command to register completion
        # Input: 'registerCompletions'
        # Expected Result: a registered command

        ("unregister_command", "unregisterCompletions", True),
        # The command to unregister completion
        # Input: 'unregisterCompletions'
        # Expected Result: a registered command
    ])
    def test_features_are_registered(self, test_name, method, is_command):
        registered = self.server.lsp.fm.commands if is_command else self.server.lsp.fm.features
        self.assertIn(method, registered, test_name)

    @parameterized.expand([
        ("once", ["register", "unregister"], ["register", "unregister"], [(0, 1)]),
        # Unregistering uses the id of the registration
        # Input: register, then unregister completion
        # Expected Result: both calls use the same id

        ("three_rounds", ["register", "unregister"] * 3, ["register", "unregister"] * 3, [(0, 1), (2, 3), (4, 5)]),
        # Every round uses the id of its own registration
        # Input: register and unregister three times
        # Expected Result: each unregistration uses the id of the registration before it

        ("unregister_first", ["unregister", "register", "unregister"], ["register", "unregister"], [(0, 1)]),
        # Unregistering without a registration does nothing
        # Input: unregister, register, unregister
        # Expected Result: only the registration and the second unregistration are sent, with the same id
    ])
    def test_unregister_uses_registration_id(self, test_name, actions, expected_calls, same_id_pairs):
        calls = []

        async def fake_register(params):
            calls.append(("register", params.registrations[0].id))

        async def fake_unregister(params):
            calls.append(("unregister", params.unregisterations[0].id))

        self.server.register_capability_async = fake_register
        self.server.unregister_capability_async = fake_unregister
        for action in actions:
            asyncio.run(self.server.register_completions() if action == "register"
                        else self.server.unregister_completions())

        self.assertEqual(expected_calls, [kind for kind, _ in calls], test_name)
        for first, second in same_id_pairs:
            self.assertEqual(calls[first][1], calls[second][1], test_name)
