"""tddlspserver package."""

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

# Util imports
from logging import getLogger, DEBUG
from re import compile
from uuid import uuid4
from os import getcwd, linesep, path
from typing import Dict, List, Optional, Tuple

# Antlr4
from antlr4 import CommonTokenStream, FileStream, InputStream, Token
from antlr4.IntervalSet import IntervalSet

# Antlr4-c3
from codeCompletionCore.CodeCompletionCore import CandidatesCollection, CodeCompletionCore

# Pygls
from lsprotocol.types import (
    CompletionItem, CompletionList, CompletionOptions, CompletionParams, Diagnostic, DidChangeTextDocumentParams,
    DidCloseTextDocumentParams, DidOpenTextDocumentParams, DidSaveTextDocumentParams, MessageType, Position, Range,
    Registration, RegistrationParams, SemanticTokens, SemanticTokensLegend, SemanticTokensParams,
    TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, Unregistration, UnregistrationParams
)
from pygls.server import LanguageServer
from pygls.workspace import Document

# User relative imports
from .cst.calculate_complexity_visitor import CalculateComplexityVisitor
from .cst.cmake_file_generator_visitor import CMakeFileGeneratorVisitor
from .cst.f90_file_generator_visitor import F90FileGeneratorVisitor
from .cst.diagnostic_listener import DiagnosticListener
from .cst.pf_file_generator_visitor import PFFileGeneratorVisitor
from .cst.system_file_visitor import SystemFileVisitor
from .cst.symbol_table_visitor import SymbolTableVisitor
from .gen.python.TestSuite.TestSuiteLexer import TestSuiteLexer
from .gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from .symboltable.symbol_table import MetricSymbol, ModuleSymbol, PathSymbol, RoutineSymbol, VariableSymbol
from .utils.compute_token_index import CaretPosition, TokenPosition, compute_token_position
from .utils.suggest_variables import suggest_symbols
from .utils.tdd_errors_strategy import TDDErrorStrategy


class TDDLSPServer(LanguageServer):
    CMD_REGISTER_COMPLETIONS = "registerCompletions"
    CMD_UNREGISTER_COMPLETIONS = "unregisterCompletions"
    CMD_RECOMMEND_SUT_BLOCKING = "recommendSUT"

    CONFIGURATION_SECTION = "ODsl-TDD-DSL-Server"

    # Number of SuT to return for metric calculation
    N_SHOW_METRICS = 0

    SHOW_DEBUG_OUTPUT: bool = True
    DEBUG_OUTPUT_SEPERATOR: str = "\t"
    DEBUG_HEADER: str = DEBUG_OUTPUT_SEPERATOR.join([
            "Scope", "Source", "Cyclomatic Complexity", "Depth", "LOC", "Parameters", "Conditionals", "Loops",
            "Branches", "Variables", "Returns", "Calls", "Decision Points", "Halstead Complexity", "(d)Operators ηT",
            "(d)Operands ηD", "(t)Operators NT", "(t)Operands ND", "Operator ratio nNT", "Operands ratio nND",
            "Vocabulary (ηT + ηD)", "Program Length (NT + ND)", "Calculated Length", "Volume", "Difficulty", "Effort",
            "Time to program", "delivered bugs", "Test Score", "Testability Difficulty", "Testability Index",
            "Normalized Testability Difficulty", "Aggregated Testability Difficulty", "Test Index",
            "Normalized Test Score", "Aggregated Test Score", "Test Factor"
    ])

    LOG = getLogger(__name__)

    def __init__(self, *args):
        super().__init__(*args)
        self.error_listener = DiagnosticListener()  # Set error listener
        self.lexer = self._init_lexer()
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = self._init_parser()
        self.files: Dict[str, Tuple[float, str, str]] = {}  # Empty attribute init for generated files
        self.fxtran_path = "fxtran"  # Default Fxtran system file path can be overwritten
        self.sort_metric = None  # Recommendation metric option
        self.input_path = None
        self.parse_tree = None

    def _init_lexer(self) -> TestSuiteLexer:
        """Initialize the lexer with error listeners."""
        lexer = TestSuiteLexer(InputStream(''))  # Set lexer from empty input stream
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)
        return lexer

    def _init_parser(self) -> TestSuiteParser:
        """Initialize the parser with error listeners and custom error strategy."""
        parser = TestSuiteParser(self.token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        parser._errHandler = TDDErrorStrategy()  # Set error strategy to custom input mismatch report
        return parser

    def reset_parser_state(self, input_stream: InputStream) -> None:
        """Reset the parser state with a new input stream."""
        self.error_listener.reset()  # Reset the error listener state
        self.lexer.inputStream = input_stream  # Assign new input stream to the lexer
        self.token_stream = CommonTokenStream(self.lexer)  # Reset the token stream with the updated lexer
        self.parser.setInputStream(self.token_stream)  # Update the parser with the new token stream


tdd_server = TDDLSPServer("pygls-odsl-tdd-prototype", "v0.8")


def _validate(text_doc: Document, server: TDDLSPServer = tdd_server) -> None:
    """Validates LSP input."""
    diagnostics = _validate_format(server, text_doc.source) if text_doc.source else []  # Validate format of file content for lexer input stream
    server.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_format(server: TDDLSPServer, source: str) -> List[Diagnostic]:
    """Validates file format."""
    server.reset_parser_state(InputStream(source))  # Get input stream of characters for lexer
    try:
        parse_tree = server.parser.testSuite()  # Parse the input source by invoking top-level rule
        # Check if the parser stopped before reaching EOF
        if not server.token_stream.fetchedEOF:
            end_pos = Position(parse_tree.stop.line, parse_tree.stop.column)
            eof_range = Range(start=end_pos, end=end_pos)
            server.error_listener.diagnostics.append(
                    Diagnostic(message="Parser stopped before end of file.", range=eof_range)
            )
        server.parse_tree = parse_tree
    except OSError as err:
        server.error_listener.diagnostics.append(err.filename.msg)
    return server.error_listener.diagnostics


@tdd_server.feature(TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[","]))
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""
    text_doc = get_text_document(params)
    tdd_server.reset_parser_state(InputStream(text_doc.source))  # Reset parser state with the current document source

    # Parse until fetched
    token_index = None
    while not tdd_server.token_stream.fetchedEOF:
        parse_tree = tdd_server.parser.testSuite()  # Parse the source to generate a parse tree by invoking top-level rule
        # Get token index under caret position
        # params.position.line + 1 as lsp line counts from 0 and antlr4 line counts from 1
        if token_index is None:
            # Compute the position of the caret in the token stream
            token_index = compute_token_position(
                    parse_tree, tdd_server.token_stream, CaretPosition(params.position.line + 1, params.position.character)
            )

    completion_list = CompletionList(is_incomplete=False, items=[])
    if token_index is None:
        # Return if no index could be determined
        # TODO add warning
        return completion_list

    core = CodeCompletionCore(tdd_server.parser)  # Launch c3 core with parser
    core.ignoredTokens = {Token.EPSILON}  # Ignore epsilon tokens
    core.preferredRules = {TestSuiteParser.RULE_reference, TestSuiteParser.RULE_srcPath, TestSuiteParser.RULE_testModule}

    # Collect candidates for code completion at the token index
    candidates = core.collectCandidates(token_index.index)
    # Resolve candidates for preferred rules
    if candidates.rules:
        symbol_types = []

        # Determine symbol types based on the rule candidates
        if TestSuiteParser.RULE_reference in candidates.rules:
            symbol_table_visitor: SymbolTableVisitor = SymbolTableVisitor("completions", getcwd(), tdd_server.fxtran_path)
            symbol_types.extend([VariableSymbol, RoutineSymbol])  # FunctionSymbol is derived from RoutineSymbol
        elif TestSuiteParser.RULE_testModule in candidates.rules:
            symbol_table_visitor: SymbolTableVisitor = SymbolTableVisitor("completions", getcwd(), tdd_server.fxtran_path)
            symbol_types.append(ModuleSymbol)
        elif TestSuiteParser.RULE_srcPath in candidates.rules:
            symbol_table_visitor: SystemFileVisitor = SystemFileVisitor("paths", getcwd())
            symbol_types.append(PathSymbol)

        symbol_table = symbol_table_visitor.visit(parse_tree)

        # Suggest symbols based on the identified symbol types
        for symbol_type in symbol_types:
            symbols = suggest_symbols(
                    symbol_table=symbol_table,
                    position=token_index,
                    symbol_type=symbol_type
            )
            completion_list.items.extend([CompletionItem(label=s) for s in symbols])

    # Add terminal tokens to the completion candidates
    stripped_literal_names = stripTerminals(elements=tdd_server.parser.literalNames)  # Strip default ' from terminals
    for key, valueList in candidates.tokens.items():
        label = IntervalSet.elementName(IntervalSet, stripped_literal_names, tdd_server.parser.symbolicNames, key)
        if label == "NEWLINE":
            label = linesep  # Replace newline with os.newline token
        if label == "<UNKNOWN>" or label in tdd_server.parser.symbolicNames:
            label = None  # Remove symbolic names or unknown tokens from completions
        if label:
            completion_list.items.append(CompletionItem(label=label))

    # VSCode empty list workaround: Add an empty completion item if no suggestions are available
    if not completion_list.items:
        completion_list.items.append(CompletionItem(label=""))

    # Optionally print debug output for the completion items
    if tdd_server.SHOW_DEBUG_OUTPUT:
        for entry in completion_list.items:
            print(entry)

    return completion_list


def stripTerminals(elements: List[str], terminal: str = "'") -> List[str]:
    """Strip string terminals from list elements."""
    return [e.strip(terminal) for e in elements]


@tdd_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(server: TDDLSPServer, params: DidChangeTextDocumentParams):
    """Validate input and return text document did change notification."""
    text_doc = get_text_document(params)
    _validate(text_doc, server)


@tdd_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: TDDLSPServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message("Text Document Did Close")


@tdd_server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(server: TDDLSPServer, params: DidSaveTextDocumentParams):
    """Execute file generator and return text document did save notification."""
    # LSP client or cli call
    input_stream: InputStream
    file_path: str
    if params:
        # LSP client
        text_doc: Document = get_text_document(params)
        file_path = path.abspath(text_doc.path)
        input_stream = InputStream(text_doc.source)
    else:
        # cli
        file_path = tdd_server.input_path
        input_stream = FileStream(tdd_server.input_path)

    server.parseTree = parse_stream(input_stream, server)  # Launch parser
    if server.parseTree:
        symbol_table_visitor: SymbolTableVisitor = SymbolTableVisitor("variables", getcwd(), tdd_server.fxtran_path)
        # Get symboltable for f90 generator
        symbol_table = symbol_table_visitor.visit(server.parseTree)

        rel_file_path: str = path.relpath(file_path, getcwd())  # Get relative input path for file generation
        # Generate pf files
        pf_file_generator_visitor: PFFileGeneratorVisitor = PFFileGeneratorVisitor(
                work_path=getcwd(), files=tdd_server.files, symbol_table=symbol_table, rel_file_path=rel_file_path
        )
        tdd_server.files = pf_file_generator_visitor.visit(server.parseTree)  # Write pf files and save generated files
        # Generate F90 files
        f90_file_generator_visitor: F90FileGeneratorVisitor = F90FileGeneratorVisitor(
                work_path=getcwd(), files=tdd_server.files, symbol_table=symbol_table, rel_file_path=rel_file_path
        )
        tdd_server.files = f90_file_generator_visitor.visit(server.parseTree)  # Update fortran file and save generated files
        # Generate CMake files
        cmake_file_generator_visitor: CMakeFileGeneratorVisitor = CMakeFileGeneratorVisitor(
                work_path=getcwd(), files=tdd_server.files, symbol_table=symbol_table
        )
        tdd_server.files = cmake_file_generator_visitor.visit(server.parseTree)  # Update CMake files and save generated files
        server.show_message("Text Document Did Save")


def parse_stream(stream: InputStream, server: TDDLSPServer = tdd_server) -> Optional:
    """Parse a file stream and return the parse tree."""
    try:
        server.reset_parser_state(stream)
        return server.parser.testSuite()
    except OSError as err:
        print(f"An error occurred while parsing: {err}")
        return None


@tdd_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(server: TDDLSPServer, params: DidOpenTextDocumentParams):
    """Validate input and return text document did open notification."""
    text_doc = get_text_document(params)
    server.show_message(f"Text Document Did Open: {text_doc.uri}", msg_type=MessageType.Info)
    _validate(text_doc)


def get_text_document(params) -> Document:
    """Return managed document."""
    return tdd_server.workspace.get_text_document(params.text_document.uri)


@tdd_server.feature(
        TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, SemanticTokensLegend(token_types=["operator"], token_modifiers=[])
)
def semantic_tokens(server: TDDLSPServer, params: SemanticTokensParams) -> SemanticTokens:
    """See https://microsoft.github.io/language-server-protocol/specification#textDocument_semanticTokens
    for details on how semantic tokens are encoded.
    """
    TOKENS = compile("\".*\"(?=:)")  # Regex to match quoted strings followed by a colon

    uri = params.text_document.uri
    doc = server.workspace.get_text_document(uri)

    last_line = 0
    last_start = 0
    data = []

    # Iterate over each line in the document to find matching tokens
    for lineno, line in enumerate(doc.lines):
        last_start = 0

        # Find tokens using the regex pattern
        for match in TOKENS.finditer(line):
            start, end = match.span()
            data += [(lineno - last_line), (start - last_start), (end - start), 0, 0]

            last_line = lineno
            last_start = start

    return SemanticTokens(data=data)


@tdd_server.command(TDDLSPServer.CMD_RECOMMEND_SUT_BLOCKING)
def recommend_SUT(tdd_server: TDDLSPServer, *args):
    """Calculates the complexity of the SuTs in the path and returns test recommendations."""
    calculate_complexity_visitor = CalculateComplexityVisitor(
            name="paths", test_work_path=getcwd(), fxtran_path=tdd_server.fxtran_path,
            sort_metric=tdd_server.sort_metric, debug=tdd_server.SHOW_DEBUG_OUTPUT,
            debug_seperator=tdd_server.DEBUG_OUTPUT_SEPERATOR
    )
    symbol_table = calculate_complexity_visitor.visit(tdd_server.parse_tree)
    metric_list = suggest_symbols(symbol_table, position=None, symbol_type=MetricSymbol)

    # Show the top N metrics as determined by the configuration
    for metric in metric_list[:tdd_server.N_SHOW_METRICS]:
        tdd_server.show_message(metric)

    # Write debug output to file if enabled
    if tdd_server.SHOW_DEBUG_OUTPUT:
        metric_list.insert(0, tdd_server.DEBUG_HEADER)
        debug_file_write(path.join(getcwd(), tdd_server.sort_metric), "\n".join(metric_list))

    tdd_server.show_message(f"Recommend SuT by {tdd_server.sort_metric}...")


def debug_file_write(file_path: str = None, content: str = None):
    """Writes debugging information to a file."""
    if tdd_server.LOG.isEnabledFor(DEBUG):
        tdd_server.LOG.debug("Log metric to file %s\n" % file_path)

    # Write the content to the specified file path
    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write(content)


@tdd_server.command(TDDLSPServer.CMD_REGISTER_COMPLETIONS)
async def register_completions(server: TDDLSPServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams(
            registrations=[Registration(
                    id=str(uuid4()), method=TEXT_DOCUMENT_COMPLETION,
                    register_options={"triggerCharacters": ","}
            )]
    )

    response = await server.register_capability_async(params)

    # Notify the user based on the response status
    if response is None:
        server.show_message("Successfully registered completions method")
    else:
        server.show_message("Error happened during completions registration.", MessageType.Error)


@tdd_server.command(TDDLSPServer.CMD_UNREGISTER_COMPLETIONS)
async def unregister_completions(server: TDDLSPServer, *args):
    """Unregister completions method on the client."""
    params = UnregistrationParams(
            unregisterations=[Unregistration(id=str(uuid4()), method=TEXT_DOCUMENT_COMPLETION)]
    )

    response = await server.unregister_capability_async(params)

    # Notify the user based on the response status
    if response is None:
        server.show_message("Successfully unregistered completions method")
    else:
        server.show_message("Error happened during completions unregistration.", MessageType.Error)
