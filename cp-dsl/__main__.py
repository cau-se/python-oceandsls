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

from antlr4 import InputStream, CommonTokenStream
import argparse
import os

# relative imports
from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from conflspserver.cst.symbol_table_visitor import SymbolTableVisitor
from conflspserver.utils.calc import DeclarationCalculator, ConfigurationCalculator
from conflspserver.generators.uvic.code_generator import UvicCodeGenerator
from conflspserver.generators.mitgcm.code_generator import MitGcmCodeGenerator
from conflspserver.generators.eval.code_generator import EvalCodeGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="CP-DSL Compiler",
        description="A compiler for the CP-DSL",
        epilog="CP-DomainSpecificLanguage Compiler"
    )
    parser.add_argument(
        "-f", "--File", dest="path", help="path to the main configuration file"
    )
    parser.add_argument(
        "-o", "--out", dest="out", help="path to generated files"
    )
    args = parser.parse_args()
    if not args.path:
        print("ERROR: Please give a configuration file as argument!")
        parser.print_help()
    else:
        current_path = args.path if os.path.isabs(args.path) else os.path.join(os.getcwd(), args.path)
        if not os.path.exists(current_path) and os.path.isfile(current_path):
            print("ERROR: whether no file or no correct path given!")
        estimated_working_directory = ""
        for i in current_path.split(os.sep):
            if i and not i.endswith(".oconf"):
                estimated_working_directory += os.sep
                estimated_working_directory += i
        configuration_visitor = SymbolTableVisitor("user_conf_1", estimated_working_directory)
        output_path = args.out if args.out else os.path.join(estimated_working_directory, "gen")
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        with open(current_path) as conf_file:
            # 1 read CONF file
            # 2 identify declaration file
            # 3 read declaration file
            # 4 compute model
            # 5 provide model to generator

            #
            # 1 read CONF file
            data = conf_file.read()
            input_stream = InputStream(data)
            lexer = ConfigurationLexer(input_stream)
            stream = CommonTokenStream(lexer)
            dcl_parsed = ConfigurationParser(stream).configurationModel()

            print("bla")
            print(dcl_parsed.declarationModel.text)

            # What is the purpose of this here
            configuration_visitor.visit(dcl_parsed)

            #
            # 2 indentify declaration file

            #
            # 3 read declaration file
            
            #
            # 4 compute model
            try:
                declaration_calculator = DeclarationCalculator(configuration_visitor.symbol_table)
            except AttributeError as e:
                print("ERROR: Could not parse Declaration-File correctly")
                print(e)
            
            declaration_result = declaration_calculator.calculate()
            table = ConfigurationCalculator(declaration_result, configuration_visitor.configuration_list).calculate()

            #
            # 5 provide model to generator
            if configuration_visitor.generator_selector == 'uvic':
                try:
                    generator = UvicCodeGenerator(table, output_path)
                    generator.generate()
                except AttributeError as e:
                    print("ERROR: Could not generate uvic files")
                    print(e)
            elif configuration_visitor.generator_selector == 'mitgcm':
                try:
                    generator = MitGcmCodeGenerator(table, output_path)
                    generator.generate()
                except AttributeError as e:
                    print("ERROR: could not generate mitgcm files")
                    print(e)
            elif configuration_visitor.generator_selector == 'eval':
                try:
                    generator = EvalCodeGenerator(table, output_path)
                    generator.generate()
                except AttributeError as e:
                    print("ERROR: could not generate eval files")
                    print(e)
