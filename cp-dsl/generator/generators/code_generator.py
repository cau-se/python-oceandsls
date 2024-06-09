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

__author__ = 'stu222808'

# Relative imports
from model.symbol_table import SymbolTable
from model.model import GroupSymbol, ParameterSymbol, FeatureSymbol, EnumSymbol


class StandardCodeGenerator():
    """
    a simple code generator representing a simple structure and helpful functions
    """

    def __init__(self, symbol_table: SymbolTable, output_path: str, template_path="") -> None:
        self._symbol_table: SymbolTable = symbol_table
        self.output_path = output_path
        if not template_path == "":
            self.template_loader = j.PackageLoader(str(self.__module__), template_path)
            self.template_environment = j.Environment(loader=self.template_loader)

    def write_file(self, content: str, filename: str):
        """method to write content to a file inside the output folder

        Args:
            content (str): string to write into the file
            filename (str): filename specified
        """
        path = os.path.join(self.output_path, filename)
        f = open(path, "w")
        f.write(content)
        f.close()

    def generate(self) -> None:
        """generate method that uses jinja templates to write files into output path
        """
        print("GIVE THE GENERATOR A TEMPLATE AND DATA TO WORK WITH")
