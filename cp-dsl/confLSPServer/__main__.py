"""cp-dsl LSPServer package."""

############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import argparse
import logging
from setuptools import setup, find_packages

from .server import conf_server

logging.basicConfig( filename="confDSL_pygls.log", level=logging.DEBUG, filemode="w" )


def main():
    parser = argparse.ArgumentParser(
        prog="CONF-Language-Server",
        description="A program for a language server based on the configuration ocean-dsl",
        epilog="ConfigurationDSL Language Server"
    )
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
        "--testing", dest="test", action="store_true", help="Run the tests"
    )
    args = parser.parse_args()
    if args.test:
        import test
    if args.tcp:
        conf_server.start_tcp( args.host, args.port )
    elif args.ws:
        conf_server.start_ws( args.host, args.port )
    else:
        parser.print_help()
        conf_server.start_io()


if __name__ == '__main__':
    main()

