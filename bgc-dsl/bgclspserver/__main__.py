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
import logging
import os
from os.path import isfile

from .server import bgc_server, did_save

logging.basicConfig( filename="bgcDSL_pygls.log", level=logging.DEBUG, filemode="w" )


def add_arguments(parser):
    parser.prog = "BGC-Language-Server"
    parser.description = "bgc-dsl server"
    parser.epilog = "BGC-DSL Language Server"

    parser.add_argument(
        "--tcp", dest="tcp", action="store_true",
        help="Use TCP server"
    )
    parser.add_argument(
        "--ws", dest="ws", action="store_true",
        help="Use WebSocket server"
    )
    parser.add_argument(
        "--host", dest="host", default="127.0.0.1",
        help="Bind to this address"
    )
    parser.add_argument(
        "--port", dest="port", type=int, default=2087,
        help="Bind to this port"
    )
    parser.add_argument(
            "-f", "--file", dest = "file", type = readable_file,
            help = "Input file for file generator"
    )


def readable_file( file_path: str ):
    """
    Check for readable file.

    :param file_path: path to file
    :return: valid readable file path
    """

    abs_file_path = os.path.join( os.getcwd( ), file_path )

    if isfile( abs_file_path ) and os.access( abs_file_path, os.R_OK ):
        return abs_file_path
    else:
        raise argparse.ArgumentTypeError( f"File {abs_file_path} doesn't exist or isn't readable." )


def main():
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    if args.file:
        # Start cli code gen with given path
        bgc_server.input_path = os.path.join( os.getcwd( ), args.file )
        did_save( bgc_server, None )
    else:
        if args.tcp:
            bgc_server.start_tcp( args.host, args.port )
        elif args.ws:
            bgc_server.start_ws( args.host, args.port )
        else:
            bgc_server.start_io()


if __name__ == "__main__":
    main()
