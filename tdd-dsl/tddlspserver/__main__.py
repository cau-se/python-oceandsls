"""exampleLSPServer package."""

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

from argparse import ArgumentTypeError
from logging import getLogger
from shutil import which
from os import getcwd
from os.path import join, dirname, abspath
from subprocess import check_output, STDOUT, CalledProcessError
from sys import executable

from odsllib.lsp.cli import configure_logging, readable_directory, readable_file, server_argument_parser, start_server

# Package imports
from .server import did_save, recommend_software_under_test, tdd_server


def make_parser():
    """Parser with the common server options (odsllib.lsp.cli) and the options of TDD-DSL."""
    parser = server_argument_parser(
        "TDD-Language-Server", "A program for a language server based on the test driven development ocean-dsl",
        epilog="TDD-DSL Language Server", file_help="TDD-File input file for pFUnit generator", log_file=False,
        debug_help="Log debug output (stderr) and write metric tables to files")
    parser.add_argument(
        # No default: argparse would validate a string default with type=..., and the server could not start at all
        # without fxtran. fxtran is only required to analyse the SUT (content assist and generation use it if present).
        "-fx", "--fxtran", dest="fxtran", type=fxtran_executable, default=None,
        help="Path to fxtran (default: fxtran on PATH)"
    )
    parser.add_argument(
        "-m", "--metric", dest="metric", default="Test Index",
        help="Metric to sort SuT recommendations, e.g. Testability Factor"
    )
    parser.add_argument(
        "-s", "--source", dest="source", type=readable_directory, help="Path of source code to analyse"
    )
    parser.add_argument(
        "-d", "--descending", action="store_true", help="Sort the list in descending order"
    )
    return parser


def fxtran_executable(path: str):
    """
    Check for valid fxtran path.

    :param path: readable path to fxtran executable
    :return: valid path
    """
    try:
        # Call "fxtran -help"
        check_output([path, "-help"], stderr=STDOUT)
    except CalledProcessError as e:
        raise ArgumentTypeError(
            f"Did not find fxtran. Command '{e.cmd}' returned error (code {e.returncode}): {e.output}. "
            "Provide a valid path via -fx PATH or add fxtran to the system PATH."
        ) from e
    except OSError as e:
        raise ArgumentTypeError(
            f"Did not find fxtran at {path} ({e}). Provide a valid path via -fx PATH or add fxtran to the system PATH."
        ) from e

    return path


def process_recommended_metrics(metrics_path):
    """Process the recommended metrics passed from __main__.py."""

    # Check for metrics
    if not metrics_path:
        print("No recommended metrics available.")
        return
    readable_file(metrics_path)

    # Get the current script's directory
    current_dir = dirname(abspath(__file__))

    # Define the path to llm main
    llm_main_path = join(current_dir, "llm")

    # Define the arguments to pass to llm
    args = ["--contextOnly", metrics_path]

    print(f"{[executable, '-m', 'llm'] + args}\tcwd:{llm_main_path}")

    # # Run the llm __main__.py file with arguments
    # result = run([executable, "-m", "llm"] + args, cwd=llm_main_path)
    #
    # # Check the result
    # if result.returncode != 0:
    #     print("llm execution failed.")
    # else:
    #     print("llm executed successfully.")


def main():
    args = make_parser().parse_args()

    # Logging goes to stderr: stdout carries the JSON-RPC stream when the server runs over stdio
    configure_logging(args)
    tdd_server.SHOW_DEBUG_OUTPUT = args.debug

    # Sort the list based on the descending flag
    tdd_server.descending_sort = args.descending

    if args.fxtran:
        # Add fxtran path
        tdd_server.fxtran_path = args.fxtran
    elif which("fxtran") is None:
        getLogger(__name__).warning(
            "fxtran not found: symbols of the system under test are not available. Provide it via -fx PATH."
        )

    if args.metric:
        # Add sort metric
        tdd_server.sort_metric = args.metric

    if args.file:
        # Start cli code gen for input path
        tdd_server.input_path = join(getcwd(), args.file)
        did_save(tdd_server, None)
    elif args.source:
        # Start cli code analysis for input path
        tdd_server.input_path = join(getcwd(), args.source)
        metrics_path = recommend_software_under_test(tdd_server)
        # Pass the recommended metrics to the llm analyzer
        process_recommended_metrics(metrics_path)
    else:
        start_server(tdd_server, args)


if __name__ == "__main__":
    main()
