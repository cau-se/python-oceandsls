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
"""Command line of the language servers: transport options, logging and start of the server.

A DSL's ``__main__`` creates the parser with :func:`server_argument_parser`, adds its own options and calls
:func:`run_server`::

    parser = server_argument_parser("dcllspserver", "Language server for CP-DSL declaration files (*.decl)")
    run_server(dcl_server, parser, on_file=check_file)
"""

import argparse
import logging
import os
from typing import Callable, Optional, Sequence

__all__ = ["DEFAULT_EPILOG", "readable_file", "readable_directory", "server_argument_parser", "configure_logging",
           "start_server", "run_server"]

DEFAULT_EPILOG = "Without --tcp/--ws the server communicates over stdin/stdout."


def readable_file(file_path: str) -> str:
    """Argument type: an existing, readable file (relative to the working directory); returns its absolute path."""
    path = os.path.join(os.getcwd(), file_path)
    if os.path.isfile(path) and os.access(path, os.R_OK):
        return path
    raise argparse.ArgumentTypeError(f"File {path} doesn't exist or isn't readable.")


def readable_directory(dir_path: str) -> str:
    """Argument type: an existing, readable directory (relative to the working directory); returns its absolute path."""
    path = os.path.join(os.getcwd(), dir_path)
    if os.path.isdir(path) and os.access(path, os.R_OK):
        return path
    raise argparse.ArgumentTypeError(f"Directory {path} doesn't exist or isn't readable.")


def server_argument_parser(prog: str, description: str, epilog: str = DEFAULT_EPILOG,
                           file_help: Optional[str] = "Check a file from the command line and report its problems",
                           log_file: bool = True, debug_help: str = "Log debug output") -> argparse.ArgumentParser:
    """Parser with the common options: --tcp, --ws, --host, --port, -f/--file, --log-file and --debug.

    Pass ``file_help=None`` to leave out -f/--file and ``log_file=False`` to leave out --log-file.
    """
    parser = argparse.ArgumentParser(prog=prog, description=description, epilog=epilog)
    parser.add_argument("--tcp", dest="tcp", action="store_true", help="Use TCP server")
    parser.add_argument("--ws", dest="ws", action="store_true", help="Use WebSocket server")
    parser.add_argument("--host", dest="host", default="127.0.0.1", help="Bind to this address")
    parser.add_argument("--port", dest="port", type=int, default=2087, help="Bind to this port")
    if file_help is not None:
        parser.add_argument("-f", "--file", dest="file", type=readable_file, help=file_help)
    if log_file:
        parser.add_argument("--log-file", dest="log_file", default=None, help="Write the log to this file")
    parser.add_argument("--debug", action="store_true", help=debug_help)
    return parser


def configure_logging(args: argparse.Namespace) -> None:
    """Log to stderr (stdout carries the JSON-RPC stream in stdio mode) or to the --log-file."""
    logging.basicConfig(filename=getattr(args, "log_file", None), level=logging.DEBUG if args.debug else logging.INFO)


def start_server(server, args: argparse.Namespace) -> None:
    """Start the pygls ``server`` over TCP (--tcp), WebSocket (--ws) or stdin/stdout."""
    if args.tcp:
        server.start_tcp(args.host, args.port)
    elif args.ws:
        server.start_ws(args.host, args.port)
    else:
        server.start_io()


def run_server(server, parser: argparse.ArgumentParser, on_file: Optional[Callable[[str], None]] = None,
               argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse the command line, configure logging and either process -f/--file with ``on_file`` or start the server.

    :return: the parsed arguments
    """
    args = parser.parse_args(argv)
    configure_logging(args)
    if on_file is not None and getattr(args, "file", None):
        on_file(args.file)
    else:
        start_server(server, args)
    return args
