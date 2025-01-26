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

from antlr4 import InputStream, CommonTokenStream, FileStream
import argparse
import os
from common.configuration import CompileFlags

# relative imports
from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from dcllspserver.gen.python.Declaration.DeclarationLexer import DeclarationLexer
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser
from generator.visitors.configuration_visitor import GeneratorConfigurationVisitor
from generator.visitors.declaration_visitor import GeneratorDeclarationVisitor
from generator.calculator.calculator import ConfigurationCalculator
from generator.calculator.calculator_dec import DeclarationCalculator
from generator.generators.uvic.code_generator import UvicCodeGenerator
from generator.generators.mitgcm.code_generator import MitGcmCodeGenerator
from generator.generators.eval.code_generator import EvalCodeGenerator
from model.declaration_model import DeclarationModel
from common.logger import GeneratorLogger

logger: GeneratorLogger


def parse_configuration_file(configuration_path: str) -> ConfigurationParser:
    input_stream = FileStream(configuration_path, "utf-8")
    lexer = ConfigurationLexer(input_stream)
    stream = CommonTokenStream(lexer)

    return ConfigurationParser(stream)

def make_configuration_model(model: DeclarationModel, input_path: str):
    configuration_tree = parse_configuration_file(input_configuration_path)
    print(f"Parse configuration model {input_path}")
    GeneratorConfigurationVisitor(model, logger).visit(configuration_tree.configurationModel())

    return model

def parse_declaration_file(declaration_path: str) -> DeclarationParser:
    input_stream = FileStream(declaration_path, "utf-8")
    lexer = DeclarationLexer(input_stream)
    stream = CommonTokenStream(lexer)

    return DeclarationParser(stream)


def make_declaration_model(model: DeclarationModel, input_path: str):
    tree = parse_declaration_file(input_path)
    print(f"Parse declaration model {input_path}")
    GeneratorDeclarationVisitor(model, logger).visit(tree.declarationModel())

    return model


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

    logger = GeneratorLogger(compile_mode)

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
    output_path = args.output_path if args.output_path else os.path.join(estimated_working_directory, "gen")
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # 1 read CONF file
    print(f"parse {input_configuration_path}")
    configuration_tree = parse_configuration_file(input_configuration_path)
    # 2 identify declaration file
    used_declaration_model = configuration_tree.configurationModel().declarationModel.text
    print(f"Model {used_declaration_model}")
    # 3 read declaration file
    input_declaration_path = os.path.join(input_directory_path, f"{used_declaration_model}.decl")
    print(f"declaration model {input_declaration_path}")

    # 4 process declaration model
    model = make_declaration_model(DeclarationModel(), input_declaration_path)

    if model is None:
        print("Declaration model error")
        exit(1)

    # 5 process configuration model
    model = make_configuration_model(model, input_configuration_path)

    # 6 Compute configuration
    print("Compute configuration")
    table = ConfigurationCalculator(model, logger).calculate()
    print("Completed")
    exit(2)
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
