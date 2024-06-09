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
from symboltable.symbol_table import SymbolTable, GroupSymbol, VariableSymbol, FeatureSymbol, EnumSymbol
from ..code_generator import StandardCodeGenerator


class UvicCodeGenerator(StandardCodeGenerator):
    """code generator for uvic

    Args:
        StandardCodeGenerator (_type_): _description_
    """

    def __init__(self, symbol_table: SymbolTable, output_path: str) -> None:
        super().__init__(symbol_table, output_path)
        self.template_loader = j.PackageLoader(str(self.__module__), "templates")
        self.template_environment = j.Environment(loader=self.template_loader)

    def generate(self) -> None:
        """generates uvic files
        """
        # control in template
        template_control = self.template_environment.get_template("control.in.template")
        control_path = os.path.join(self.output_path, "control.in")
        control = open(control_path, "w")
        control.write(template_control.render(symbols=self._symbol_table.children(), groupSymbol=GroupSymbol, paramSymbol=VariableSymbol,
                      featureSymbol=FeatureSymbol, isinstance=isinstance, enumSymbol=EnumSymbol, enumerate=enumerate, bool=bool))
        control.close()
        # mk in template
        template_mk = self.template_environment.get_template("mk.in.template")
        # get source_group and general group
        general_group = {}
        source_group = {}
        for element in self._symbol_table.children():
            if element.name == "general":
                for i in element.children():
                    if i.is_array:
                        general_group[i.name] = i.to_normalized_array()
                    else:
                        # could be an enum so we need the string here
                        general_group[i.name] = i.value[0] if isinstance(i.value, tuple) else i.value
            if element.name == "source_group":
                for i in element.children():
                    if i.is_array:
                        source_group[i.name] = i.to_normalized_array()
                    else:
                        general_group[i.name] = i.value[0] if isinstance(i.value, tuple) else i.value
        mkPath = os.path.join(self.output_path, "mk.in")
        mk = open(mkPath, "w")
        mk.write(template_mk.render(general=general_group, source=source_group,
                 features=self._symbol_table.get_nested_symbols_of_type_sync(FeatureSymbol), isinstance=isinstance, tuple=tuple))
        mk.close()
