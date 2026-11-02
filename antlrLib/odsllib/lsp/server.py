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
"""A pygls language server skeleton for ANTLR based DSLs.

Subclasses configure the generated lexer/parser classes and the start rule and may override the hooks
:meth:`AntlrLanguageServer.semantic_diagnostics`, :meth:`AntlrLanguageServer.symbol_completions` and
:meth:`AntlrLanguageServer.document_saved`. The server provides:

* ``textDocument/didOpen``, ``didChange``, ``didSave``, ``didClose`` with syntax (and semantic) diagnostics
* ``textDocument/completion`` with grammar keywords and DSL specific symbols
* ``textDocument/semanticTokens/full`` derived from the token stream
* the ``registerCompletions``/``unregisterCompletions`` commands used by the VS Code clients

Nothing is ever written to stdout, which carries the JSON-RPC stream when the server runs over stdio.
"""

from __future__ import annotations

import inspect
import logging
import uuid
from typing import Dict, Iterable, List, Optional, Set, Type

from antlr4 import Lexer, Parser
from lsprotocol.types import (
    CompletionItem, CompletionList, CompletionOptions, CompletionParams, Diagnostic, DidChangeTextDocumentParams,
    DidCloseTextDocumentParams, DidOpenTextDocumentParams, DidSaveTextDocumentParams, MessageType, Position,
    Registration, RegistrationParams, SemanticTokens, SemanticTokensParams, TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, Unregistration, UnregistrationParams,
)
from pygls.server import LanguageServer

from ..code_completion_core import CandidatesCollection
from .completion import collect_candidates, keyword_items, matches_prefix
from .compute_token_index import CaretPosition, TokenPosition, compute_caret_token_position
from .error_strategy import InputMismatchErrorStrategy
from .parsing import ParseResult, parse_source
from .semantic_tokens import (
    DEFAULT_COMMENT_TOKENS, DEFAULT_NUMBER_TOKENS, DEFAULT_STRING_TOKENS, LEGEND, encode_semantic_tokens,
)

logger = logging.getLogger(__name__)


class AntlrLanguageServer(LanguageServer):
    """Generic language server for an ANTLR grammar. See module documentation."""

    CMD_REGISTER_COMPLETIONS = "registerCompletions"
    CMD_UNREGISTER_COMPLETIONS = "unregisterCompletions"

    #: Generated ANTLR lexer and parser classes
    lexer_class: Type[Lexer]
    parser_class: Type[Parser]
    #: Name of the parser rule used to parse a whole document
    start_rule: str
    #: Error strategy factory; None keeps ANTLR's default strategy
    error_strategy_factory = InputMismatchErrorStrategy
    #: Report input the start rule did not consume
    require_eof: bool = True
    #: Rules reported as candidates instead of their tokens (passed to the c3 engine)
    preferred_rules: Set[int] = set()
    #: Tokens never suggested
    ignored_tokens: Set[int] = set()
    #: Token types treated as identifiers when looking for the token under the caret
    word_token_types: Set[int] = set()
    #: Characters triggering completion in the client
    trigger_characters: List[str] = []
    #: Symbolic token names highlighted as strings, numbers and comments
    string_tokens: Iterable[str] = DEFAULT_STRING_TOKENS
    number_tokens: Iterable[str] = DEFAULT_NUMBER_TOKENS
    comment_tokens: Iterable[str] = DEFAULT_COMMENT_TOKENS

    def __init__(self, name: str, version: str, **kwargs):
        super().__init__(name, version, **kwargs)
        #: Last parse result for each open document
        self.parse_results: Dict[str, ParseResult] = {}
        self._completion_registration_id: Optional[str] = None
        self._register_default_features()

    # -----------------------------------------------------------------------------------------------------------------
    # Feature registration
    # -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _handler(method):
        """Wrap a bound method in a plain function: pygls stores registration data as attributes on handlers."""
        if inspect.iscoroutinefunction(method):
            async def async_handler(*args):
                return await method(*args)
            return async_handler

        def handler(*args):
            return method(*args)
        return handler

    def _register_default_features(self) -> None:
        h = self._handler
        self.feature(TEXT_DOCUMENT_DID_OPEN)(h(self.on_did_open))
        self.feature(TEXT_DOCUMENT_DID_CHANGE)(h(self.on_did_change))
        self.feature(TEXT_DOCUMENT_DID_SAVE)(h(self.on_did_save))
        self.feature(TEXT_DOCUMENT_DID_CLOSE)(h(self.on_did_close))
        self.feature(TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=list(self.trigger_characters)))(
            h(self.on_completion)
        )
        self.feature(TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, LEGEND)(h(self.on_semantic_tokens))
        self.command(self.CMD_REGISTER_COMPLETIONS)(h(self.register_completions))
        self.command(self.CMD_UNREGISTER_COMPLETIONS)(h(self.unregister_completions))

    # -----------------------------------------------------------------------------------------------------------------
    # Transport independent API (used by the handlers, the CLI and unit tests)
    # -----------------------------------------------------------------------------------------------------------------

    @property
    def diagnostic_source(self) -> str:
        return self.name

    def parse(self, source: str) -> ParseResult:
        """Parse a document with a fresh lexer/parser."""
        return parse_source(
            source, self.lexer_class, self.parser_class, self.start_rule, self.error_strategy_factory,
            self.diagnostic_source, self.require_eof,
        )

    def validate(self, uri: str, source: str) -> List[Diagnostic]:
        """Parse a document, remember the result and return syntax and semantic diagnostics."""
        result = self.parse(source)
        self.parse_results[uri] = result
        diagnostics = list(result.diagnostics)
        try:
            diagnostics.extend(self.semantic_diagnostics(result, uri))
        except Exception:  # never let a broken check suppress syntax diagnostics
            logger.exception("Semantic analysis failed for %s", uri)
        return diagnostics

    def complete(self, uri: str, source: str, position: Position) -> CompletionList:
        """Compute completion items for an LSP (0-based) position."""
        result = self.parse(source)
        caret = CaretPosition(position.line + 1, position.character)
        token_position = compute_caret_token_position(result.tree, result.tokens, caret, self.word_token_types)
        candidates = collect_candidates(result.parser, token_position.index, self.preferred_rules, self.ignored_tokens)

        items: List[CompletionItem] = keyword_items(result.parser, candidates, token_position.text)
        try:
            symbols = self.symbol_completions(result, token_position, candidates, uri)
        except Exception:
            logger.exception("Symbol completion failed for %s", uri)
            symbols = []
        labels = {item.label for item in items}
        for item in symbols:
            if item.label not in labels and matches_prefix(item.filter_text or item.label, token_position.text):
                labels.add(item.label)
                items.append(item)
        return CompletionList(is_incomplete=False, items=items)

    def semantic_tokens(self, source: str) -> SemanticTokens:
        result = self.parse(source)
        return SemanticTokens(
            data=encode_semantic_tokens(
                result.parser, result.tokens, self.string_tokens, self.number_tokens, self.comment_tokens
            )
        )

    # -----------------------------------------------------------------------------------------------------------------
    # Hooks for DSL specific behavior
    # -----------------------------------------------------------------------------------------------------------------

    def semantic_diagnostics(self, result: ParseResult, uri: str) -> List[Diagnostic]:
        """Return DSL specific diagnostics for a parsed document (default: none)."""
        return []

    def symbol_completions(
            self, result: ParseResult, position: TokenPosition, candidates: CandidatesCollection, uri: str
    ) -> List[CompletionItem]:
        """Return completion items for the preferred rule candidates (default: none)."""
        return []

    def document_saved(self, uri: str, result: ParseResult) -> None:
        """Called after a document was saved and re-validated (default: nothing)."""

    # -----------------------------------------------------------------------------------------------------------------
    # LSP handlers
    # -----------------------------------------------------------------------------------------------------------------

    def _source(self, uri: str) -> str:
        return self.workspace.get_text_document(uri).source

    def _publish(self, uri: str) -> List[Diagnostic]:
        diagnostics = self.validate(uri, self._source(uri))
        self.publish_diagnostics(uri, diagnostics)
        return diagnostics

    def on_did_open(self, params: DidOpenTextDocumentParams) -> None:
        self._publish(params.text_document.uri)

    def on_did_change(self, params: DidChangeTextDocumentParams) -> None:
        self._publish(params.text_document.uri)

    def on_did_save(self, params: DidSaveTextDocumentParams) -> None:
        uri = params.text_document.uri
        self._publish(uri)
        try:
            self.document_saved(uri, self.parse_results[uri])
        except Exception as e:
            logger.exception("Processing saved document %s failed", uri)
            self.show_message(f"Processing {uri} failed: {e}", MessageType.Error)

    def on_did_close(self, params: DidCloseTextDocumentParams) -> None:
        uri = params.text_document.uri
        self.parse_results.pop(uri, None)
        self.publish_diagnostics(uri, [])

    def on_completion(self, params: CompletionParams) -> CompletionList:
        uri = params.text_document.uri
        return self.complete(uri, self._source(uri), params.position)

    def on_semantic_tokens(self, params: SemanticTokensParams) -> SemanticTokens:
        return self.semantic_tokens(self._source(params.text_document.uri))

    async def register_completions(self, *args) -> None:
        """Dynamically register the completion feature on the client."""
        registration_id = str(uuid.uuid4())
        params = RegistrationParams(registrations=[Registration(
            id=registration_id, method=TEXT_DOCUMENT_COMPLETION,
            register_options={"triggerCharacters": list(self.trigger_characters)},
        )])
        try:
            await self.register_capability_async(params)
            self._completion_registration_id = registration_id
            self.show_message("Successfully registered completions method")
        except Exception:
            logger.exception("Completion registration failed")
            self.show_message("Error happened during completions registration.", MessageType.Error)

    async def unregister_completions(self, *args) -> None:
        """Unregister the completion feature registered by :meth:`register_completions`."""
        if self._completion_registration_id is None:
            self.show_message("Completions were not registered dynamically.", MessageType.Warning)
            return
        params = UnregistrationParams(unregisterations=[
            Unregistration(id=self._completion_registration_id, method=TEXT_DOCUMENT_COMPLETION)
        ])
        try:
            await self.unregister_capability_async(params)
            self._completion_registration_id = None
            self.show_message("Successfully unregistered completions method")
        except Exception:
            logger.exception("Completion unregistration failed")
            self.show_message("Error happened during completions unregistration.", MessageType.Error)
