"""Minimal stdio server for the end-to-end test (``python -m tests.expr_server``)."""

import logging

from odsllib.lsp.server import AntlrLanguageServer
from tests.gen.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from tests.gen.TestExprCore.TestExprCoreParser import TestExprCoreParser


class ExprServer(AntlrLanguageServer):
    lexer_class = TestExprCoreLexer
    parser_class = TestExprCoreParser
    start_rule = "expression"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # logging goes to stderr, never to stdout
    ExprServer("expr-e2e-server", "0.1").start_io()
