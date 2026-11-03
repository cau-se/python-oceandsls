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

import pytest

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


@pytest.mark.parametrize("argv, expected", [
    ([], ("io",)),
    (["--tcp", "--port", "3000"], ("tcp", "127.0.0.1", 3000)),
    (["--ws", "--host", "0.0.0.0"], ("ws", "0.0.0.0", 2087)),
])
def test_run_server_starts_the_selected_transport(argv, expected):
    server = FakeServer()
    run_server(server, server_argument_parser("test", "a test server"), argv=argv)
    assert server.started == expected


def test_run_server_processes_a_file_instead_of_starting(tmp_path):
    source = tmp_path / "model.txt"
    source.write_text("model")
    server, processed = FakeServer(), []
    args = run_server(server, server_argument_parser("test", "a test server"), on_file=processed.append,
                      argv=["-f", str(source), "--debug"])
    assert processed == [str(source)] and server.started is None and args.debug


def test_optional_arguments_can_be_left_out():
    parser = server_argument_parser("test", "a test server", file_help=None, log_file=False)
    args = parser.parse_args([])
    assert not hasattr(args, "file") and not hasattr(args, "log_file")


def test_paths_are_checked(tmp_path):
    (tmp_path / "file.txt").write_text("")
    assert readable_file(str(tmp_path / "file.txt")) == str(tmp_path / "file.txt")
    assert readable_directory(str(tmp_path)) == str(tmp_path)
    with pytest.raises(argparse.ArgumentTypeError):
        readable_file(str(tmp_path / "missing.txt"))
    with pytest.raises(argparse.ArgumentTypeError):
        readable_directory(str(tmp_path / "file.txt"))


@pytest.fixture(name="table")
def table_fixture():
    table = SymbolTable("main", SymbolTableOptions(False))
    for name in ("Alpha", "alpine", "beta"):
        table.add_new_symbol_of_type(VariableSymbol, None, name, len(name))
    table.add_new_symbol_of_type(RoutineSymbol, None, "always")
    return table


def test_all_symbols_of_a_type_are_suggested_without_a_position(table):
    assert sorted(suggest_symbols(table, None, VariableSymbol)) == ["Alpha", "alpine", "beta"]
    assert suggest_symbols(table, None, RoutineSymbol) == ["always"]


def test_names_are_filtered_by_the_typed_text(table):
    position = TokenPosition(index=0, context=None, text="AL")
    assert sorted(suggest_symbols(table, position, VariableSymbol)) == ["Alpha", "alpine"]
    assert suggest_symbols(table, TokenPosition(0, None, " "), VariableSymbol) == ["Alpha", "alpine", "beta"]


def test_a_dsl_can_filter_by_its_own_rules(table):
    def by_value(text, symbols, symbol_type):
        assert symbol_type is VariableSymbol and text == ""
        return sorted(str(symbol.value) for symbol in symbols)

    assert suggest_symbols(table, None, VariableSymbol, filter_function=by_value) == ["4", "5", "6"]


def test_run_async_works_inside_a_running_event_loop(table):
    async def inside_loop():
        return run_async(table.get_symbols_of_type, VariableSymbol, False)

    assert len(asyncio.run(inside_loop())) == 3
