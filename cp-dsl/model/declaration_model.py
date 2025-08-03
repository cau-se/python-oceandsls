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

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Coroutine, TypeVar, List, Dict

# Antlr4
from antlr4.tree.Tree import ParseTree

from model.symbols import Scope, NamedElement
from model.type_system import NamedType
from model.unit_model import UnitSpecification
from model.arithmetic_model import AbstractExpression

#
# Model elements of the DSL
#
# These include
# - user types
# - Parameter Groups
# - Parameter
# - Features Sets
# - Feature
# - Expressions

#
# Declaration Model
#


class DeclarationModel(Scope):

    def __init__(self, name: str = None):
        super().__init__(parent=None)  # DeclarationModel has no parent
        self.name:str = name
        self.configuration_name:str = None
        self.groups:dict[str,ParameterGroup] = {}
        self.features:dict[str, Feature] = {}
        self.types:dict[str,NamedType] = {}

    def add_new_type(self, type: NamedType) -> None:
        self.types[type.name] = type

    def resolve_type(self, name: str) -> NamedType:
        return self.types.get(name, None)

    def resolve_feature(self, name:str) -> Feature:
        return self.features.get(name, None)

    def resolve_parameter_group(self, name:str) -> ParameterGroup:
        return self.groups.get(name, None)

    def resolve_symbol(self, name: str) -> NamedElement:
        feature = self.features.get(name, None)
        if feature is None:
            return self.groups.get(name, None)
        else:
            return feature

#
# Parameter Groups
#
@dataclass
class Selector:
    lower_bound:int
    upper_bound:int

@dataclass
class SelectorExpression:
    selectors : List[Selector]
    expression : AbstractExpression

class Parameter(NamedElement):

    type: NamedType
    unit: UnitSpecification
    description: str
    default_value: AbstractExpression = None
    value = None

    def __init__(self, name: str, type: NamedType, unit: UnitSpecification, description: str, parent:Scope) -> None:
        super().__init__(name, parent)
        self.type = type
        self.unit = unit
        self.description = description
        self.default_value = None # declaration value spec
        self.value = None # computed value
        self.entries:list[SelectorExpression] = [] # entries for the computed value


class ParameterGroup(NamedElement):

    description: str
    parameters: Dict[str, Parameter]

    def __init__(self, name: str, description: str, parent: Scope):
        super().__init__(name, parent)
        self.description = description
        self.parameters = {}

    def resolve_parameters(self, name: str) -> Parameter:
        return self.parameters.get(name)

    def resolve_symbol(self, name:str) -> Parameter:
        return self.resolve_parameters(name)

#
# Features
#


class EKind(Enum):
    ALTERNATIVE = 0
    MULTIPLE = 1


class FeatureGroup(Scope):

    kind:EKind
    features:Dict[str, Feature]

    def __init__(self, kind:EKind, parent: Scope):
        super().__init__(parent)
        self.kind = kind
        self.features = {}

    def resolve_symbol(self, name: str) -> Feature:
        return self.features.get(name, None)

class Feature(NamedElement):

    is_activated: bool = False  # set if the feature is activated
    required: bool = False
    description: str = None
    requires: List[Feature]
    excludes: List[Feature]

    groups:Dict[str, ParameterGroup]
    feature_sets:List[FeatureGroup]

    def __init__(self, name: str, description: str, parent: Scope):
        super().__init__(name, parent)
        self.description = description
        self.groups = {}
        self.requires = []
        self.excludes = []
        self.feature_sets = []

    def resolve_feature(self, name: str) -> Feature:
        for group in self.feature_sets:
            feature = group.features.get(name, None)
            if feature != None:
                return feature
        return None

    def resolve_parameter_group(self, name:str):
        return self.groups.get(name, None)

    def resolve_symbol(self, name: str) -> ParameterGroup|FeatureGroup:
        result = self.groups.get(name, None)
        if result is None:
            for feature_set in self.feature_sets:
                feature = feature_set.features.get(name, None)
                if feature is not None:
                    return feature
            return None
        else:
            return result
