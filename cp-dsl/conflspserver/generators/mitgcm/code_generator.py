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
from symboltable.symbol_table import SymbolTable, GroupSymbol, VariableSymbol, FeatureSymbol, EnumSymbol
from ..code_generator import StandardCodeGenerator

class MitGcmCodeGenerator(StandardCodeGenerator):
    """a generator for mitgcm

    Args:
        StandardCodeGenerator (_type_): _description_
    """

    def __init__(self, symbolTable: SymbolTable, outputPath: str) -> None:
        super().__init__(symbolTable, outputPath)
        self.template_loader = j.PackageLoader(str(self.__module__), "jinja-templates/mitgcm")
        self.template_environment = j.Environment(loader=self.template_loader)

    def isConfigurated(self, elem: FeatureSymbol) -> bool:
        """function to lookup if any parameter in elem was configurated

        Args:
            elem (FeatureSymbol): _description_

        Returns:
            bool: if one parameter was configurated
        """
        groupSymbol = elem.get_nested_symbols_of_type_sync(GroupSymbol)
        for param in groupSymbol:
            if len(param.configuration) > 0:
                return True
        return False

    def firstNotNoneElem(self, elem, type) -> int:
        """function for jinja template to avoid ',' behind last element

        Args:
            elem (_type_): the element to search inside for
            type (_type_): the type to search for

        Returns:
            int: returns the index of last element
        """
        index = 0
        for param in elem.get_nested_symbols_of_type_sync(type):
            if param.value is None:
                index += 1
            else:
                return index

    def generate(self) -> None:
        """generates files for mitgcm
        """
        # need groups, feature list
        groupList = {}
        featureList = {}
        activatedList = []
        layer_size = False
        alreadyDone = {
            "EEPARMS": [
                False, "eedata"], "MNC": [
                False, "data.mnc"], "GMRedi": [
                False, "data.gmredi"], "RBCS": [
                    False, "data.rbcs"], "Layers": [
                        False, "data.layers"], "PTRACERS": [
                            False, "data.ptracers"], "Shap": [
                                False, "data.shap"], "obcs": [
                                    False, "data.obcs"], "GCHEM": [
                                        False, "data.gchem"], "offline": [
                                            False, "data.offline"]}
        featureTemplate = self.template_environment.get_template("data.feature.template")

        def checkFeature(elem):
            """a function to check if the givben feature is activated -> write the mitgcm file

            Args:
                elem (GroupSymbol, FeatureSymbol): a feature from mitgcm
            """
            try:
                if elem.is_activated:
                    if elem.name == "diagnostics":
                        activatedList.append("Diagnostics")
                    else:
                        activatedList.append(elem.name)
                dataList = alreadyDone[elem.name]
                if dataList[0]:
                    return
                if elem.name == "EEPARMS":
                    eeparmsTemplate = self.template_environment.get_template("eedata.template")
                    self.writeFile(
                        eeparmsTemplate.render(
                            group=elem,
                            isinstance=isinstance,
                            variableSymbol=VariableSymbol,
                            float=float,
                            int=int,
                            bool=bool,
                            groupSymbol=GroupSymbol,
                            none=None,
                            str=str,
                            enumerate=enumerate,
                            firstNotNoneElem=self.firstNotNoneElem),
                        "eedata")
                    return
                if not elem.is_activated:
                    return
                fileName = dataList[1]
                alreadyDone[elem.name] = [True, fileName]
                self.writeFile(featureTemplate.render(feature=elem, isinstance=isinstance, variableSymbol=VariableSymbol, float=float, int=int,
                               bool=bool, groupSymbol=GroupSymbol, none=None, str=str, enumerate=enumerate, firstNotNoneElem=self.firstNotNoneElem), fileName)
            except IndexError:
                pass

        for elem in self._symbol_table.getAllNestedSymbolsSync():
            if isinstance(elem, GroupSymbol):
                groupList[elem.name] = elem
            if isinstance(elem, FeatureSymbol):
                featureList[elem.name] = elem
            # check and use template for group(EEPARMS), feature(MNC, GMRedi, RBCS, Layers, PTRACERS, Shap, obcs, GCHEM, offline)
            checkFeature(elem)
            if elem.name == "layers_size":
                layer_size = True

        # give group for eedata, feature for data.mnc, data.gmredi, data.rbcs, data.layers, data.ptracers, data.shap, data.obcs, data.gchem, data.off all same
        # template for every feature give to data.pkg + check for feature diagnostic
        dataPkgTemplate = self.template_environment.get_template("data.pkg.template")
        self.writeFile(dataPkgTemplate.render(actData=activatedList, enumerate=enumerate), "data.pkg")

        # layer_size template only if group layer_size exists (LAYERS_SIZE.h)
        if layer_size:
            # TODO: still buggy
            layerSizeTemplate = self.template_environment.get_template("layer_size.template")
            self.writeFile(layerSizeTemplate.render(groups=groupList, variableSymbol=VariableSymbol, groupSymbol=GroupSymbol,
                           none=None, str=str, enumerate=enumerate, firstNotNoneElem=self.firstNotNoneElem), "LAYERS_SIZE.h")

        # packages.conf check for feature diagnostics
        packagesTemplate = self.template_environment.get_template("packages.conf.template")
        try:
            activatedList.remove("EEPARMS")
        except ValueError:
            pass
        self.writeFile(packagesTemplate.render(features=activatedList), "packages.conf")

        dataTemplate = self.template_environment.get_template("data.template")
        self.writeFile(dataTemplate.render(groups=groupList, isinstance=isinstance, variableSymbol=VariableSymbol, float=float, int=int,
                       bool=bool, groupSymbol=GroupSymbol, none=None, str=str, enumerate=enumerate, firstNotNoneElem=self.firstNotNoneElem), "data")

        sizeTemplate = self.template_environment.get_template("size.template")
        self.writeFile(sizeTemplate.render(groups=groupList, variableSymbol=VariableSymbol, groupSymbol=GroupSymbol,
                       none=None, str=str, enumerate=enumerate, firstNotNoneElem=self.firstNotNoneElem), "SIZE.h")

        for elem in self._symbol_table.getAllNestedSymbolsSync("tRef"):
            print(elem.name, elem.value, type(elem))
