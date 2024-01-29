"""bgcLSPServer package."""

############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################

# util imports
import asyncio
import re

import time
import uuid
import sys, os, logging
from typing import List, Optional
from urllib.parse import urlparse

# antlr4
from antlr4.IntervalSet import IntervalSet
from antlr4 import InputStream, CommonTokenStream, Token, ParseTreeWalker

# antlr4-c3
# TODO fail relative import beyond top-level package
# from ...antlrLib.CodeCompletionCore.CodeCompletionCore import CodeCompletionCore, CandidatesCollection
from codeCompletionCore.CodeCompletionCore import CodeCompletionCore, CandidatesCollection

# pygls
# Deprecated from 0.13
# from pygls.lsp.methods import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE,
# TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL)
# from pygls.lsp.types import (CompletionItem, CompletionList, CompletionOptions, CompletionParams,
# ConfigurationItem, ConfigurationParams, Diagnostic, DidChangeTextDocumentParams,
#                              DidCloseTextDocumentParams, DidOpenTextDocumentParams, MessageType, Position, Range,
#                              Registration, RegistrationParams, SemanticTokens,
#                              SemanticTokensLegend, SemanticTokensParams, Unregistration, UnregistrationParams)
# from pygls.lsp.types.basic_structures import (WorkDoneProgressBegin, WorkDoneProgressEnd, WorkDoneProgressReport)
from pygls.server import LanguageServer
from pygls.workspace import Document
# Migrating to pygls v1.0
# https://pygls.readthedocs.io/en/latest/pages/migrating-to-v1.html
from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE,
                              TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, CompletionItem,
                              CompletionList, CompletionOptions, CompletionParams, ConfigurationItem,
                              ConfigurationParams, Diagnostic, DidChangeTextDocumentParams, DidCloseTextDocumentParams,
                              DidOpenTextDocumentParams, MessageType, Registration, RegistrationParams, SemanticTokens,
                              SemanticTokensLegend, SemanticTokensParams, Unregistration, UnregistrationParams,
                              WorkDoneProgressBegin, WorkDoneProgressEnd, WorkDoneProgressReport,
                              TEXT_DOCUMENT_DID_SAVE, DidSaveTextDocumentParams)

# user relative imports
from .utils.computeTokenIndex import computeTokenPosition, computeTokenIndex, CaretPosition, TokenPosition
from .utils.suggestVariables import suggestVariables

from .cst.SymbolTableVisitor import SymbolTableVisitor
from .cst.DiagnosticListener import DiagnosticListener

from .gen.python.BgcDsl.BgcDslLexer import BgcDslLexer
from .gen.python.BgcDsl.BgcDslParser import BgcDslParser
from .gen.python.BgcDsl.BgcDslVisitor import BgcDslVisitor
from .fileWriter.Generator import BgcCodeGenerator

# debug import
# from pprint import pprint
# python path hacking / DO NOT USE for live code
# if not os.path.join(sys.path[0], 'example-dsl', 'lspExampleServer') in sys.path:
#     sys.path.append(os.path.join( sys.path[0], 'example-dsl', 'lspExampleServer') )
# pprint(sys.path)

COUNT_DOWN_START_IN_SECONDS = 10
COUNT_DOWN_SLEEP_IN_SECONDS = 1


class bgcLSPServer( LanguageServer ):
    CMD_PROGRESS = 'progress'
    CMD_REGISTER_COMPLETIONS = 'registerCompletions'
    CMD_UNREGISTER_COMPLETIONS = 'unregisterCompletions'

    CONFIGURATION_SECTION = 'ODslBGCServer'

    def __init__(self, *args):
        super().__init__( *args )
        # set ErrorListener
        self.error_listener: DiagnosticListener = DiagnosticListener()
        # set empty input stream
        input_stream: InputStream = InputStream( str() )

        # set lexer
        self.lexer: BgcDslLexer = BgcDslLexer( input_stream )
        # set ErrorListener for diagnostics
        self.lexer.removeErrorListeners()
        self.lexer.addErrorListener( self.error_listener )

        # set token stream pipe between lexer and parser
        self.tokenStream: CommonTokenStream = CommonTokenStream( self.lexer )

        # set parser
        self.parser: BgcDslParser = BgcDslParser( self.tokenStream )
        # set ErrorListener for diagnostics
        self.parser.removeErrorListeners()
        self.parser.addErrorListener( self.error_listener )


bgc_server = bgcLSPServer( 'pygls-odsl-bgc-prototype', 'v0.1' )

logger = logging.getLogger( __name__ )


def _validate(ls: bgcLSPServer, params):
    # msg to debug console
    # TODO setup debug logger
    # ls.show_message_log( 'Validating file...' )

    # get file content for lexer input stream
    text_doc: Document = ls.workspace.get_document( params.text_document.uri )
    source: str = text_doc.source
    # validate format if source is determined
    diagnostics: List[Diagnostic] = _validate_format( ls, source ) if source is not None else []
    # return diagnostics
    ls.publish_diagnostics( text_doc.uri, diagnostics )


def _validate_format(ls: bgcLSPServer, source: str):
    """Validates file format."""
    # get input stream of characters for lexer
    input_stream: InputStream = InputStream( source )

    # set the input stream and reset the lexer/parser/listener
    ls.error_listener.reset()
    ls.lexer.inputStream = input_stream
    ls.tokenStream = CommonTokenStream( ls.lexer )
    ls.parser.setInputStream( ls.tokenStream )

    try:
        # launch parser by invoking top-level rule
        ls.parser.bgcModel()
    
    except OSError as err:
        # TODO add exception
        msg = err.filename.msg

        ls.error_listener.diagnostics.append( msg )

    # return diagnostics
    return ls.error_listener.diagnostics


def get_symbol_name_at_position(uri, position):
    logger.info( 'uri: %s\n', uri, 'position: %s\n', position )


def lookup_symbol(uri, name):
    logger.info( 'uri: %s\n', uri, 'name: %s\n', name )


@bgc_server.feature( TEXT_DOCUMENT_COMPLETION, CompletionOptions( trigger_characters=[','] ) )
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""

    # set input stream of characters for lexer
    text_doc: Document = bgc_server.workspace.get_document( params.text_document.uri )
    source: str = text_doc.source
    input_stream: InputStream = InputStream( source )

    # reset the lexer/parser
    bgc_server.error_listener.reset()
    bgc_server.lexer.inputStream = input_stream
    bgc_server.tokenStream = CommonTokenStream( bgc_server.lexer )
    bgc_server.parser.setInputStream( bgc_server.tokenStream )


    # launches parser by invoking top-level rule
    Top_levelContext = BgcDslParser.BgcModelContext
    parseTree: Top_levelContext = bgc_server.parser.bgcModel()

    # get token index under caret position
    # params.position.line + 1 as lsp line counts from 0 and antlr4 line counts from 1
    tokenIndex: TokenPosition = computeTokenPosition( parseTree, bgc_server.tokenStream,
                                                      CaretPosition( params.position.line + 1,
                                                                     params.position.character ) )

    # set emtpy return list
    completionList: CompletionList = CompletionList( is_incomplete=False, items=[] )

    # return if no index could be determined
    if tokenIndex is None:
        # TODO add exception
        return completionList

    # launch c3 core with parser
    core: CodeCompletionCore = CodeCompletionCore( bgc_server.parser )

    core.ignoredTokens = {Token.EPSILON}
    core.preferredRules = {BgcDslParser, BgcDslParser}

    # get completion candidates
    candidates: CandidatesCollection = core.collectCandidates( tokenIndex.index )

    # TODO add interesting rules
    if any( rule in candidates.rules for rule in [None] ):

        symbolTableVisitor: SymbolTableVisitor = SymbolTableVisitor( 'completions' )

        symbolTable = symbolTableVisitor.visit( parseTree )

        variables = suggestVariables( symbolTable, tokenIndex )

        for variable in variables:
            completionList.items.append( CompletionItem( label=variable ) )

    # get labels of completion candidates to return
    labels_list: List[str] = []
    for key, valueList in candidates.tokens.items():
        completionList.items.append( CompletionItem(
            label=IntervalSet.elementName( IntervalSet, bgc_server.parser.literalNames,
                                           bgc_server.parser.symbolicNames, key ) ) )

    # return completion candidates labels
    return completionList


@bgc_server.feature( TEXT_DOCUMENT_DID_CHANGE )
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate( ls, params )


@bgc_server.feature( TEXT_DOCUMENT_DID_CLOSE )
def did_close(server: bgcLSPServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message( 'Text Document Did Close' )


@bgc_server.feature( TEXT_DOCUMENT_DID_SAVE )
def did_save(server: bgcLSPServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""
    
    uri_path = params.text_document.uri
    uri_parsed = urlparse(uri_path).path
    # set input stream of characters for lexer
    text_doc: Document = bgc_server.workspace.get_document( params.text_document.uri )
    source: str = text_doc.source
    input_stream: InputStream = InputStream( source )

    # reset the lexer/parser
    bgc_server.error_listener.reset()
    bgc_server.lexer.inputStream = input_stream
    bgc_server.tokenStream = CommonTokenStream( bgc_server.lexer )
    bgc_server.parser.setInputStream( bgc_server.tokenStream )

    Top_levelContext = BgcDslParser.BgcModelContext
    parseTree: Top_levelContext = bgc_server.parser.bgcModel()
    tableVisitor = SymbolTableVisitor( str(os.getcwd( )))
    tableVisitor.visit(parseTree)
    print(f'path existssss{os.path.isdir(uri_parsed)}')
    print(uri_path)
    generator = BgcCodeGenerator(tableVisitor.symbolTable, os.path.dirname(uri_parsed))
    
    generator.generate()

    # TODO
    server.show_message(f'Saved in {os.path.dirname(uri_parsed)}')
    server.show_message( 'Text Document Did Save' )


@bgc_server.feature( TEXT_DOCUMENT_DID_OPEN )
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message( 'Text Document Did Open' )
    _validate( ls, params )


@bgc_server.feature( TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
                     SemanticTokensLegend( token_types=["operator"], token_modifiers=[] ) )
def semantic_tokens(ls: bgcLSPServer, params: SemanticTokensParams):
    """See https://microsoft.github.io/language-server-protocol/specification#textDocument_semanticTokens
    for details on how semantic tokens are encoded."""

    TOKENS = re.compile( '".*"(?=:)' )

    uri = params.text_document.uri
    doc = ls.workspace.get_document( uri )

    last_line = 0
    last_start = 0

    data = []

    for lineno, line in enumerate( doc.lines ):
        last_start = 0

        for match in TOKENS.finditer( line ):
            start, end = match.span()
            data += [(lineno - last_line), (start - last_start), (end - start), 0, 0]

            last_line = lineno
            last_start = start

    return SemanticTokens( data=data )


@bgc_server.command( bgcLSPServer.CMD_PROGRESS )
async def progress(ls: bgcLSPServer, *args):
    """Create and start the progress on the client."""
    token = 'token'
    # Create
    await ls.progress.create_async( token )
    # Begin
    ls.progress.begin( token, WorkDoneProgressBegin( title='Indexing', percentage=0 ) )
    # Report
    for i in range( 1, 10 ):
        ls.progress.report( token, WorkDoneProgressReport( message=f'{i * 10}%', percentage=i * 10 ), )
        await asyncio.sleep( 2 )
    # End
    ls.progress.end( token, WorkDoneProgressEnd( message='Finished' ) )


@bgc_server.command( bgcLSPServer.CMD_REGISTER_COMPLETIONS )
async def register_completions(ls: bgcLSPServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams( registrations=[Registration( id=str( uuid.uuid4() ), method=TEXT_DOCUMENT_COMPLETION,
                                                              register_options={"triggerCharacters": "[':']"} )] )
    response = await ls.register_capability_async( params )
    if response is None:
        ls.show_message( 'Successfully registered completions method' )
    else:
        ls.show_message( 'Error happened during completions registration.', MessageType.Error )


@bgc_server.command( bgcLSPServer.CMD_UNREGISTER_COMPLETIONS )
async def unregister_completions(ls: bgcLSPServer, *args):
    """Unregister completions method on the client."""
    params = UnregistrationParams(
        unregisterations=[Unregistration( id=str( uuid.uuid4() ), method=TEXT_DOCUMENT_COMPLETION )] )
    response = await ls.unregister_capability_async( params )
    if response is None:
        ls.show_message( 'Successfully unregistered completions method' )
    else:
        ls.show_message( 'Error happened during completions unregistration.', MessageType.Error )
