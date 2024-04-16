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

import jinja2 as j
import os

__author__ = 'Reiner Jung'

# Relative imports
from conflspserver.symboltable.symbol_table import SymbolTable, GroupSymbol, VariableSymbol, FeatureSymbol, EnumSymbol
from ..code_generator import StandardCodeGenerator


class EvalCodeGenerator(StandardCodeGenerator):
    """a generator to test data model constructions

    Args:
        StandardCodeGenerator (_type_): _description_
    """

    def __init__(self, symbol_table: SymbolTable, output_path: str) -> None:
        super().__init__(symbol_table, output_path)
        self.template_loader = j.PackageLoader(str(self.__module__), "templates")
        self.template_environment = j.Environment(loader=self.template_loader)

    def generate(self) -> None:
        pass
