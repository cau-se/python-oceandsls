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

from antlr4 import CommonTokenStream, FileStream
import argparse
import os
import sys
from typing import Optional
from cpdsl.common.configuration import CompileFlags

# relative imports
from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from dcllspserver.gen.python.Declaration.DeclarationLexer import DeclarationLexer
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser
from cpdsl.generator.visitors.configuration_visitor import GeneratorConfigurationVisitor
from cpdsl.generator.visitors.declaration_visitor import GeneratorDeclarationVisitor
from cpdsl.generator.calculator.calculator import Calculator as ConfigurationCalculator
from cpdsl.generator.generators.uvic.code_generator import UvicCodeGenerator
from cpdsl.generator.generators.mitgcm.code_generator import MitGcmCodeGenerator
from cpdsl.generator.generators.eval.code_generator import EvalCodeGenerator
from cpdsl.model.declaration_model import DeclarationModel, Feature, ParameterGroup, Parameter, SelectorExpression
from cpdsl.model.unit_model import UnitSpecification
from cpdsl.model.arithmetic_model import AbstractExpression
from cpdsl.common.logger import GeneratorLogger
from cpdsl.generator.calculator.unit_calculator import UnitCalculator, unit_of

logger: GeneratorLogger


def parse_configuration_file(configuration_path: str) -> ConfigurationParser:
    input_stream = FileStream(configuration_path, "utf-8")
    lexer = ConfigurationLexer(input_stream)
    stream = CommonTokenStream(lexer)

    return ConfigurationParser(stream)

def make_configuration_model(model: DeclarationModel, input_path: str):
    configuration_tree = parse_configuration_file(input_path)
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

_unit_calculator: Optional[UnitCalculator] = None


def unit_calculator() -> UnitCalculator:
    """The unit calculator reporting through the current logger."""
    global _unit_calculator  # pylint: disable=global-statement
    if _unit_calculator is None or _unit_calculator.logger is not logger:
        _unit_calculator = UnitCalculator(logger)
    return _unit_calculator

def check_unit_compatibility(target_unit:UnitSpecification, source_unit:UnitSpecification, element:Parameter):
    # values must be given in a unit compatible with the declared unit (checked with cfunits, if installed)
    unit_calculator().check(target_unit, source_unit, element)

def derive_expression_unit(expression:AbstractExpression) -> UnitSpecification:
    # TODO derive the unit of composed expressions; for now the unit given with a value or of a referenced parameter
    return unit_of(expression)

def check_parameter_integrity(parameter: Parameter):
    target_unit = parameter.unit
    source_default_unit = derive_expression_unit(parameter.default_value)
    check_unit_compatibility(target_unit, source_default_unit, parameter)

    for entry in parameter.entries:
        # entries are values (expressions) or, for arrays, values with selectors
        expression = entry.expression if isinstance(entry, SelectorExpression) else entry
        source_entry_unit = derive_expression_unit(expression)
        check_unit_compatibility(target_unit, source_entry_unit, parameter)

def check_parameter_group_integrity(group: ParameterGroup):
    for parameter in group.parameters.values():
        check_parameter_integrity(parameter)

def check_feature_integrity(feature: Feature):
    if feature.is_activated:
        for r in feature.requires:
            if not r.is_activated:
                logger.logger.error("Feature missing. Feature %s requires %s, but %s is not activated.", feature.name, r.name, r.name)
        for group in feature.groups.values():
            check_parameter_group_integrity(group)

def check_all_features_integrity(model: DeclarationModel):
    for feature in model.features.values():
        check_feature_integrity(feature)

def check_all_parameters_integrity(model: DeclarationModel):
    for group in model.groups.values():
        check_parameter_group_integrity(group)

def check_model_integrity(model: DeclarationModel):
    check_all_features_integrity(model)
    check_all_parameters_integrity(model)

def main():
    global logger, input_configuration_path
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
        sys.exit(1)

    input_configuration_path = args.input_path if os.path.isabs(args.input_path) else os.path.join(os.getcwd(), args.input_path)
    if not os.path.isfile(input_configuration_path):
        print(f"ERROR: Given file {input_configuration_path} not found.")
        sys.exit(1)

    input_directory_path = os.path.dirname(input_configuration_path)

    output_path = args.output_path if args.output_path else os.path.join(input_directory_path, "gen")
    os.makedirs(output_path, exist_ok=True)

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
        sys.exit(1)

    # 5 process configuration model
    model = make_configuration_model(model, input_configuration_path)

    # 6 check model integrity (reports problems through the logger)
    check_model_integrity(model)

    # 7 compute the configured values (stored in the parameters of the model)
    print("Compute configuration")
    ConfigurationCalculator(model, logger).calculate()
    print("Completed")

    # 8 provide the model to the generator of the declaration model
    generators = {"uvic": UvicCodeGenerator, "mitgcm": MitGcmCodeGenerator, "eval": EvalCodeGenerator}
    generator_class = generators.get(used_declaration_model)
    if generator_class is None:
        print(f"No code generator for declaration model {used_declaration_model} (available: {', '.join(generators)})")
        return
    try:
        generator_class(model, output_path).generate()
    except (AttributeError, OSError, ValueError) as e:
        print(f"ERROR: could not generate {used_declaration_model} files: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
