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

import argparse
from logging import basicConfig, DEBUG
from os import access, getcwd, R_OK
from os.path import isfile, join, isdir, dirname, abspath
from subprocess import check_output, STDOUT, CalledProcessError, run
from sys import executable

# Package imports
from .server import did_save, recommend_software_under_test, tdd_server

basicConfig(level=DEBUG)


def add_arguments(parser):
    parser.prog = "TDD-Language-Server"
    parser.description = "A program for a language server based on the test driven development ocean-dsl"
    parser.epilog = "TDD-DSL Language Server"

    parser.add_argument(
        "--tcp", dest="tcp", action="store_true", help="Use TCP server"
    )
    parser.add_argument(
        "--ws", dest="ws", action="store_true", help="Use WebSocket server"
    )
    parser.add_argument(
        "--host", dest="host", default="127.0.0.1", help="Bind to this address"
    )
    parser.add_argument(
        "--port", dest="port", type=int, default=2087, help="Bind to this port"
    )
    parser.add_argument(
        "-fx", "--fxtran", dest="fxtran", type=fxtran_executable, default="fxtran", help="Path to fxtran"
    )

    parser.add_argument(
        "-m", "--metric", dest="metric", default="Test Index", help="Metric to sort SuT recommendations, e.g. Testability Factor"
    )

    parser.add_argument(
        "-f", "--file", dest="file", type=readable_file, help="TDD-File input file for pFUnit generator"
    )

    parser.add_argument(
        "-s", "--source", dest="source", type=readable_directory, help="Path of source code to analyse"
    )

    parser.add_argument(
        "-d", "--descending", action="store_true", help="Sort the list in descending order"
    )


def readable_file(file_path: str):
    """
    Check for an existing and readable file.

    :param file_path: path to file
    :return: valid readable file path
    """

    abs_file_path = join(getcwd(), file_path)

    if isfile(abs_file_path) and access(abs_file_path, R_OK):
        return abs_file_path
    else:
        raise argparse.ArgumentTypeError(f"File {abs_file_path} doesn't exist or isn't readable.")


def readable_directory(dir_path: str):
    """
    Check for an existing and readable directory.

    :param dir_path: path to directory
    :return: valid readable directory path
    """

    abs_dir_path = join(getcwd(), dir_path)

    if isdir(abs_dir_path) and access(abs_dir_path, R_OK):
        return abs_dir_path
    else:
        raise argparse.ArgumentTypeError(f"Directory {abs_dir_path} doesn't exist or isn't readable.")


def fxtran_executable(path: str):
    """
    Check for valid fxtran path.

    :param path: readable path to fxtran executable
    :return: valid path
    """
    # Add help argument to succeed.
    cmd: str = " ".join([path, "-help"])

    try:
        # Call "fxtran -help" via subprocess
        check_output(cmd, shell=True, stderr=STDOUT)
    except CalledProcessError as e:
        raise argparse.ArgumentTypeError(
            f"Did not found fxtran. Command '{e.cmd}' returned error (code {e.returncode}): {e.output}. Provide valid path via -fx PATH or add to system PATH."
        )

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
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    # Sort the list based on the descending flag
    tdd_server.descending_sort = args.descending

    if args.fxtran:
        # Add fxtran path
        tdd_server.fxtran_path = args.fxtran

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

        if args.tcp:
            # Start server via tcp
            tdd_server.start_tcp(args.host, args.port)
        elif args.ws:
            # Start server via WebSocket
            tdd_server.start_ws(args.host, args.port)
        else:
            # Start server via IO
            tdd_server.start_io()


if __name__ == "__main__":
    main()
