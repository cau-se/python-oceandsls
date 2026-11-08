#  Copyright (c) 2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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
"""Tests of the server command line (odsllib.lsp.cli) and the symbol completion (odsllib.lsp.symbols)."""

import argparse
import asyncio
import os
import tempfile
from unittest import TestCase

from parameterized import parameterized

from odsllib.lsp.cli import readable_directory, readable_file, run_server, server_argument_parser
from odsllib.lsp.compute_token_index import TokenPosition
from odsllib.lsp.symbols import run_async, suggest_symbols
from odsllib.symbol_table import RoutineSymbol, SymbolTable, SymbolTableOptions, VariableSymbol


class FakeServer:
    """Records how the server was started."""

    def __init__(self):
        self.started = None

    def start_tcp(self, host, port):
        self.started = ("tcp", host, port)

    def start_ws(self, host, port):
        self.started = ("ws", host, port)

    def start_io(self):
        self.started = ("io",)


class TestCommandLine(TestCase):

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(self.directory.cleanup)
        self.file = os.path.join(self.directory.name, "model.txt")
        with open(self.file, "w", encoding="utf-8") as f:
            f.write("model")

    @parameterized.expand([
        ("stdio", [], ("io",)),
        # Without transport options the server communicates over stdin/stdout
        # Input: no arguments
        # Expected Result: start_io()

        ("tcp", ["--tcp", "--port", "3000"], ("tcp", "127.0.0.1", 3000)),
        # A TCP server on a port
        # Input: --tcp --port 3000
        # Expected Result: start_tcp() on 127.0.0.1:3000

        ("websocket", ["--ws", "--host", "0.0.0.0"], ("ws", "0.0.0.0", 2087)),
        # A WebSocket server on a host and the default port
        # Input: --ws --host 0.0.0.0
        # Expected Result: start_ws() on 0.0.0.0:2087

        ("tcp_with_debug", ["--tcp", "--debug"], ("tcp", "127.0.0.1", 2087)),
        # Logging options do not change the transport
        # Input: --tcp --debug
        # Expected Result: start_tcp() on the default host and port
    ])
    def test_run_server_starts_the_selected_transport(self, test_name, argv, expected):
        server = FakeServer()
        run_server(server, server_argument_parser("test", "a test server"), argv=argv)
        self.assertEqual(expected, server.started, test_name)

    @parameterized.expand([
        ("file", ["-f", "{file}", "--debug"], [True], None, True),
        # A file is processed instead of starting the server
        # Input: -f FILE --debug and a file handler
        # Expected Result: the handler gets the file, the server is not started, debug is set

        ("file_without_handler", ["-f", "{file}"], None, ("io",), False),
        # Without a file handler the server is started
        # Input: -f FILE and no file handler
        # Expected Result: start_io()

        ("handler_without_file", [], [], ("io",), False),
        # A file handler alone does not prevent the start
        # Input: no arguments and a file handler
        # Expected Result: start_io(), the handler is not called
    ])
    def test_run_server_processes_a_file(self, test_name, argv, handler_calls, expected_start, expected_debug):
        server, processed = FakeServer(), []
        argv = [a.format(file=self.file) for a in argv]
        args = run_server(server, server_argument_parser("test", "a test server"),
                          on_file=processed.append if handler_calls is not None else None, argv=argv)

        self.assertEqual([self.file] * len(handler_calls or []), processed, test_name)
        self.assertEqual(expected_start, server.started, test_name)
        self.assertEqual(expected_debug, args.debug, test_name)

    @parameterized.expand([
        ("without_file_and_log_file", None, False, ["tcp", "ws", "host", "port", "debug"]),
        # Optional arguments can be left out
        # Input: file_help=None, log_file=False
        # Expected Result: neither 'file' nor 'log_file' among the arguments

        ("without_log_file", "check a file", False, ["tcp", "ws", "host", "port", "file", "debug"]),
        # Only the log file left out
        # Input: a file help text, log_file=False
        # Expected Result: 'file', but no 'log_file'

        ("all", "check a file", True, ["tcp", "ws", "host", "port", "file", "log_file", "debug"]),
        # All common arguments
        # Input: a file help text, log_file=True
        # Expected Result: all arguments including 'file' and 'log_file'
    ])
    def test_optional_arguments(self, test_name, file_help, log_file, expected_arguments):
        parser = server_argument_parser("test", "a test server", file_help=file_help, log_file=log_file)
        self.assertEqual(sorted(expected_arguments), sorted(vars(parser.parse_args([]))), test_name)

    @parameterized.expand([
        ("existing_file", readable_file, "file.txt", True),
        # An existing file is accepted
        # Input: readable_file with an existing file
        # Expected Result: its path

        ("missing_file", readable_file, "missing.txt", False),
        # A missing file is rejected
        # Input: readable_file with a path that does not exist
        # Expected Result: ArgumentTypeError

        ("existing_directory", readable_directory, "", True),
        # An existing directory is accepted
        # Input: readable_directory with an existing directory
        # Expected Result: its path

        ("file_as_directory", readable_directory, "file.txt", False),
        # A file is no directory
        # Input: readable_directory with a file
        # Expected Result: ArgumentTypeError

        ("directory_as_file", readable_file, "", False),
        # A directory is no file
        # Input: readable_file with a directory
        # Expected Result: ArgumentTypeError
    ])
    def test_paths_are_checked(self, test_name, check, name, expected_valid):
        with open(os.path.join(self.directory.name, "file.txt"), "w", encoding="utf-8"):
            pass
        path = os.path.join(self.directory.name, name)
        if expected_valid:
            self.assertEqual(path, check(path), test_name)
        else:
            with self.assertRaises(argparse.ArgumentTypeError, msg=test_name):
                check(path)


class TestSymbolCompletion(TestCase):

    def setUp(self):
        self.table = SymbolTable("main", SymbolTableOptions(False))
        for name in ("Alpha", "alpine", "beta"):
            self.table.add_new_symbol_of_type(VariableSymbol, None, name, len(name))
        self.table.add_new_symbol_of_type(RoutineSymbol, None, "always")

    @parameterized.expand([
        ("all_variables", None, VariableSymbol, ["Alpha", "alpine", "beta"]),
        # Without a position all symbols of a type are suggested
        # Input: no position, VariableSymbol
        # Expected Result: all three variables

        ("routines", None, RoutineSymbol, ["always"]),
        # Symbols of another type
        # Input: no position, RoutineSymbol
        # Expected Result: the routine 'always'

        ("prefix_case_insensitive", TokenPosition(index=0, context=None, text="AL"), VariableSymbol,
         ["Alpha", "alpine"]),
        # The typed text filters the names case-insensitively
        # Input: the text 'AL' in front of the caret, VariableSymbol
        # Expected Result: 'Alpha' and 'alpine'

        ("whitespace_prefix", TokenPosition(0, None, " "), VariableSymbol, ["Alpha", "alpine", "beta"]),
        # Whitespace in front of the caret does not filter
        # Input: the text ' ' in front of the caret, VariableSymbol
        # Expected Result: all three variables

        ("no_match", TokenPosition(0, None, "x"), VariableSymbol, []),
        # A prefix no name starts with
        # Input: the text 'x' in front of the caret, VariableSymbol
        # Expected Result: no suggestions
    ])
    def test_suggest_symbols(self, test_name, position, symbol_type, expected_names):
        self.assertEqual(expected_names, sorted(suggest_symbols(self.table, position, symbol_type)), test_name)

    @parameterized.expand([
        ("values", None, lambda text, symbols: sorted(str(s.value) for s in symbols), ["4", "5", "6"]),
        # A DSL can filter by its own rules, e.g. present values instead of names
        # Input: no position and a filter that returns the values
        # Expected Result: the values of the three variables

        ("values_with_prefix", TokenPosition(0, None, "al"),
         lambda text, symbols: sorted(str(s.value) for s in symbols), ["4", "5", "6"]),
        # The filter decides what to do with the typed text
        # Input: the text 'al' in front of the caret and a filter that ignores it
        # Expected Result: the values of all three variables

        ("count", None, lambda text, symbols: [str(len(symbols))], ["3"]),
        # The filter gets all symbols at once
        # Input: no position and a filter that returns the number of symbols
        # Expected Result: '3'
    ])
    def test_a_dsl_can_filter_by_its_own_rules(self, test_name, position, dsl_filter, expected):
        calls = []

        def filter_function(text, symbols, symbol_type):
            calls.append((text, symbol_type))
            return dsl_filter(text, symbols)

        result = suggest_symbols(self.table, position, VariableSymbol, filter_function=filter_function)

        self.assertEqual(expected, result, test_name)
        self.assertEqual([(position.text if position else "", VariableSymbol)], calls, test_name)

    @parameterized.expand([
        ("variables_in_running_loop", True, VariableSymbol, 3),
        # A coroutine can be run from inside a running event loop
        # Input: the variables of the table, collected inside asyncio.run()
        # Expected Result: three variables

        ("variables_without_loop", False, VariableSymbol, 3),
        # Without a running event loop
        # Input: the variables of the table, collected directly
        # Expected Result: three variables

        ("routines_in_running_loop", True, RoutineSymbol, 1),
        # Another symbol type inside a running event loop
        # Input: the routines of the table, collected inside asyncio.run()
        # Expected Result: one routine
    ])
    def test_run_async(self, test_name, inside_loop, symbol_type, expected_count):
        async def in_loop():
            return run_async(self.table.get_symbols_of_type, symbol_type, False)

        symbols = asyncio.run(in_loop()) if inside_loop else run_async(self.table.get_symbols_of_type, symbol_type,
                                                                       False)
        self.assertEqual(expected_count, len(symbols), test_name)
