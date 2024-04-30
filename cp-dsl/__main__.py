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
from enum import Enum

# relative imports
from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from dcllspserver.gen.python.Declaration.DeclarationLexer import DeclarationLexer
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser
from conflspserver.cst.symbol_table_visitor import ConfigurationCPVisitor, ConfigurationVisitor
from dcllspserver.cst.symbol_table_visitor_dcl import DeclarationCPVisitor
from conflspserver.utils.calc import DeclarationCalculator, ConfigurationCalculator
from conflspserver.generators.uvic.code_generator import UvicCodeGenerator
from conflspserver.generators.mitgcm.code_generator import MitGcmCodeGenerator
from conflspserver.generators.eval.code_generator import EvalCodeGenerator
from symboltable.symbol_table import SymbolTable, SymbolTableOptions

class CompileFlags(Enum):
    RELAX = "relax"
    STRICT = "strict"
    IGNORE = "ignore"

def parse_configuration_file(configuration_path:str) -> ConfigurationParser:
    with open(configuration_path) as configuration_file:
        data = configuration_file.read()
        input_stream = InputStream(data)
        lexer = ConfigurationLexer(input_stream)
        stream = CommonTokenStream(lexer)
    
        return ConfigurationParser(stream)

def parse_declaration_file(declaration_path:str) -> DeclarationParser:
    with open(declaration_path) as declaration_file:
        data = declaration_file.read()
        input_stream = InputStream(data)
        lexer = DeclarationLexer(input_stream)
        stream = CommonTokenStream(lexer)
    
        return DeclarationParser(stream)

if __name__ == '__main__':
    compile_mode: CompileFlags = CompileFlags.RELAX

    parser = argparse.ArgumentParser(
        prog="CP-DSL Compiler",
        description="A compiler for the CP-DSL",
        epilog="CP-Domain Specific Language Compiler"
    )
    parser.add_argument(
        "-i", "--input", dest="input_path", required=True, help="path to the main configuration file"
    )
    parser.add_argument(
        "-o", "--out", dest="output_path", required=False, help="path to generated files"
    )
    parser.add_argument(
        "-f", "--compile-flags", dest="flags", help="compile flags", nargs='*',
        choices=[e.value for e in CompileFlags]
    )

    args = parser.parse_args()

    if args.flags:
        for flag in args.flags:
            match flag:
                case CompileFlags.IGNORE.value:
                    compile_mode = CompileFlags.IGNORE
                case CompileFlags.RELAX.value:
                    compile_mode = CompileFlags.RELAX
                case CompileFlags.STRICT.value:
                    compile_mode = CompileFlags.STRICT

    print(f"compile mode {compile_mode.name}")

    if not args.input_path:
        print("ERROR: Please specify a configuration file as argument!")
        parser.print_help()
        exit(1)
    
    input_configuration_path = args.input_path if os.path.isabs(args.input_path) else os.path.join(os.getcwd(), args.input_path)
    if not os.path.exists(input_configuration_path) and os.path.isfile(input_configuration_path):
        print(f"ERROR: Given file {input_configuration_path} not found.")
        exit(1)

    input_directory_path = os.path.dirname(input_configuration_path)
    
    estimated_working_directory = ""
    for i in input_configuration_path.split(os.sep):
        if i and not i.endswith(".oconf"):
            estimated_working_directory += os.sep
            estimated_working_directory += i
    configuration_visitor = ConfigurationCPVisitor("user_conf_1", estimated_working_directory)
    output_path = args.output_path if args.output_path else os.path.join(estimated_working_directory, "gen")
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
        
    # 1 read CONF file
    print(f"parse {input_configuration_path}")
    configration_tree = parse_configuration_file(input_configuration_path)
    # 2 identify declaration file
    used_declaration_model = configration_tree.configurationModel().declarationModel.text
    print(f"Model {used_declaration_model}")
    # 3 read declaration file
    input_declaration_path = os.path.join(input_directory_path, f"{used_declaration_model}.decl")
    print(f"declaration model {input_declaration_path}")
    declaration_tree = parse_declaration_file(input_declaration_path)
        
    # 4 compute model
    # 4.1 creates a new symboltable with no duplicate symbols
    print("Create symbol table")
    symbol_table = SymbolTable("root_1", SymbolTableOptions(False))
    # 4.2 declaration
    print("Visit declarion model")
    declaration_visitor = DeclarationCPVisitor(symbol_table).visit(declaration_tree.declarationModel())
    print("Compute declaration")
    try:
        declaration_calculator = DeclarationCalculator(configuration_visitor.symbol_table)
    except AttributeError as e:
        print("ERROR: Could not parse Declaration-File correctly")
        print(e)

    declaration_result = declaration_calculator.calculate()
    print("Computed declaration")

    # 4.3 configuration
    print("Visit configuration")
    configuration_visitor = ConfigurationCPVisitor(symbol_table)
    configuration_visitor.visit(configration_tree.configurationModel())
    print("Compute configuration")
    table = ConfigurationCalculator(declaration_result, configuration_visitor.configuration_list).calculate()
    print("Completed")
    # 5 provide model to generator
    if used_declaration_model == 'uvic':
        try:
            generator = UvicCodeGenerator(table, output_path)
            generator.generate()
        except AttributeError as e:
            print("ERROR: Could not generate uvic files")
            print(e)
    elif used_declaration_model == 'mitgcm':
        try:
            generator = MitGcmCodeGenerator(table, output_path)
            generator.generate()
        except AttributeError as e:
            print("ERROR: could not generate mitgcm files")
            print(e)
    elif used_declaration_model == 'eval':
        try:
            generator = EvalCodeGenerator(table, output_path)
            generator.generate()
        except AttributeError as e:
            print("ERROR: could not generate eval files")
            print(e)
