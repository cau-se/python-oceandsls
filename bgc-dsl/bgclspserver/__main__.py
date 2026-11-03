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
"""Command line of the BGC-DSL language server (``python -m bgclspserver``)."""

from odsllib.lsp.cli import run_server, server_argument_parser

from .server import bgc_server, did_save


def generate(path: str) -> None:
    """Run the file generator for a BGC-DSL file (-f/--file)."""
    bgc_server.input_path = path
    did_save(bgc_server, None)


def main():
    parser = server_argument_parser("BGC-Language-Server", "bgc-dsl server", epilog="BGC-DSL Language Server",
                                    file_help="Input file for file generator")
    run_server(bgc_server, parser, on_file=generate)


if __name__ == "__main__":
    main()
