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

"""Command line of the CP-DSL language server for declaration files (*.decl) (``python -m dcllspserver``)."""

from odsllib.lsp.cli import run_server, server_argument_parser

from .server import did_save, dcl_server


def check(path: str) -> None:
    """Check a file from the command line (-f/--file) and report its problems."""
    dcl_server.input_path = path
    did_save(dcl_server, None)


def main():
    parser = server_argument_parser("dcllspserver", "Language server for CP-DSL declaration files (*.decl)")
    run_server(dcl_server, parser, on_file=check)


if __name__ == "__main__":
    main()
