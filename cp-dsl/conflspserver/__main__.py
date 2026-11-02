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

import argparse
import logging
import os
from os.path import isfile

from .server import did_save, conf_server


def add_arguments(parser):
    parser.prog = "conflspserver"
    parser.description = "Language server for CP-DSL configuration files (*.oconf)"
    parser.epilog = "Without --tcp/--ws the server communicates over stdin/stdout."

    parser.add_argument("--tcp", dest="tcp", action="store_true", help="Use TCP server")
    parser.add_argument("--ws", dest="ws", action="store_true", help="Use WebSocket server")
    parser.add_argument("--host", dest="host", default="127.0.0.1", help="Bind to this address")
    parser.add_argument("--port", dest="port", type=int, default=2087, help="Bind to this port")
    parser.add_argument("-f", "--file", dest="file", type=readable_file,
                        help="Check a file from the command line and report its problems")
    parser.add_argument("--log-file", dest="log_file", default=None, help="Write the log to this file")
    parser.add_argument("--debug", action="store_true", help="Log debug output")


def readable_file(file_path: str):
    """
    Check for readable file.

    :param file_path: path to file
    :return: valid readable file path
    """
    abs_file_path = os.path.join(os.getcwd(), file_path)
    if isfile(abs_file_path) and os.access(abs_file_path, os.R_OK):
        return abs_file_path
    else:
        raise argparse.ArgumentTypeError(f"File {abs_file_path} doesn't exist or isn't readable.")


def main():
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    # Log to stderr (stdout carries the JSON-RPC stream in stdio mode) or to a file with --log-file
    logging.basicConfig(filename=args.log_file, level=logging.DEBUG if args.debug else logging.INFO)

    if args.file:
        conf_server.input_path = args.file
        did_save(conf_server, None)
    elif args.tcp:
        conf_server.start_tcp(args.host, args.port)
    elif args.ws:
        conf_server.start_ws(args.host, args.port)
    else:
        conf_server.start_io()


if __name__ == "__main__":
    main()
