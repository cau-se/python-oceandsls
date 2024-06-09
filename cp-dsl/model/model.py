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
from typing import Optional, Coroutine, TypeVar, List

# Antlr4
from antlr4.tree.Tree import ParseTree

from symbol_table import ScopedSymbol, Symbol, UnitSymbol
from typesystem import Type, TypeKind
from units import UnitSpecification

T = TypeVar("T", bound=Symbol)

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
# Types
#

class EnumSymbol(Symbol):
    '''
    a class for enums of cp-dsl language
    '''

    def __init__(self, name: str = "", enums=None):
        super().__init__(name)
        self.enums = enums


class RangeSymbol(Symbol):
    '''
    a class for ranges in cp-dsl
    '''

    def __init__(self, name, type, minimum, maximum):
        super().__init__(name)
        self.type = type
        self.minimum = minimum
        self.maximum = maximum

#
# Parameter
#

class GroupSymbol(ScopedSymbol):
    """
    A Class for Group Declarations
    """
    description: Optional[str]
    group_type: Optional[T]

    def __init__(self, name: str, groupType: T, description: str = ""):
        super().__init__(name)
        self.description = description
        self.group_type = groupType

    def get_group_variables(self, localOnly=True) -> Coroutine[List[T]]:
        return self.get_symbols_of_type(self.group_type)



class VariableSymbol(Symbol):
    """a class for parameter of cp-dsl

    Args:
        Symbol (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, name: str, description: str = "", value=None, unit_specification: UnitSpecification = None, type=None):
        super().__init__(name)
        self.description = description
        self.unit = unit_specification
        self.is_tree = isinstance(value, ParseTree)
        self.val = value if value else None
        if type == "float":
            value = 0.0
        if type == "int":
            value = 0
        self.type = type
        self.is_array = False

    @property
    def value(self):
        return self.val

#
# Feature
#

class FeatureSymbol(ScopedSymbol):
    """
    A standalone function/procedure/rule.
    """
    return_type: Optional[Type]  # Can be null if result is void.
    is_activated: bool = False  # set if the feature is activated

    def __init__(self, name: str, description: str = "", returnType: Type = None):
        super().__init__(name)
        self.return_type = returnType
        self.is_activated = False
        self.description = description

    def get_variables(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync(VariableSymbol)

    def get_parameters(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync(VariableSymbol)

    def get_units(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync(UnitSymbol)

    def get_features(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync(FeatureSymbol)


#
# Expression
#


class ArraySymbol(VariableSymbol):
    """
    a class representing a n-dimensional array
    Array Representation:
    i[2:7] = {0,1,2,3,4,5}
    => [2,3,4,5,6,7][0,1,2,3,4,5]
    i[5][9] = 8
    => [5][ArraySymbol([9][8])]
    """

    def __init__(self, name: str = "", upper_bound=0, lower_bound=0):
        super().__init__(name)
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.is_array = True
        self.vectors = []
        self.array_value = []

    @property
    def value(self):
        return self.to_normalized_array()

    # !!!!EXPERIMENTAL!!!!
    def add(self, vector, val) -> None:
        """
        adds a value in the array
        :vector: the index of the value
        :val: the value to save in the array
        """
        # n Dimension Support
        if len(vector) >= 2:
            if isinstance(self.get(vector[0]), ArraySymbol):
                newArray = self.get(vector[0])
            else:
                newArray = ArraySymbol()
            newArray.add(vector[1:], val)
            self.add([vector[0]], newArray)
        else:
            # check if vector already in array
            if vector[0] in self.vectors:
                i = self.vectors.index(vector[0])
                self.array_value[i] = val
                return
            if self.upper_bound == 0 and self.lower_bound == 0:
                self.vectors.append(vector[0])
                self.array_value.append(val)
            else:
                # Check for the bounds
                if self.lower_bound <= vector[0] and self.upper_bound >= vector[0] or self.upper_bound == 0:
                    self.vectors.append(vector[0])
                    self.array_value.append(val)
                else:
                    print("ERROR: Array", self.name, "out of bound error for index", vector)

    def get(self, index) -> T:
        """
        get a value out of the list, None if not available
        :index: the index of the value to return
        :return: the value on given index
        """
        try:
            if isinstance(index, list):
                return self.array_value[self.vectors.index(index[0])]
            return self.array_value[self.vectors.index(index)]
        except IndexError or ValueError:
            return None

    def getVector(self, vector) -> T:
        """
        get a value out of the list recursive given by a vector
        :vector: the vector
        :return: the value on the vector
        """
        if len(vector) >= 2:
            currArray = self
            try:
                for i in vector:
                    index = self.vectors.index(i)
                    currArray = currArray.value[index]
                return currArray
            except IndexError or ValueError:
                # return the last value reached
                return currArray
        else:
            return self.get(vector[0])

    def remove(self, index) -> T:
        """
        removes and returns the value places at index
        :index: the index of the value to remove
        :return: the value removed
        """
        i = self.vectors.index(index)
        self.vectors.pop(i)
        return self.array_value.pop(i)

    def removeVal(self, val) -> None:
        """
        removes a given value from the array (first elem found)
        :val: the value to remove
        """
        i = self.array_value.index(val)
        self.vectors.pop(i)
        self.array_value.pop(i)

    def toArray(self, recursive=True) -> list:
        """
        converts the array in a pyton list
        :recursive: convert also arrays in arrays
        :return: the generated python list
        """
        returnVal = []
        for i in range(len(self)):
            if i in self.vectors:
                if not recursive:
                    returnVal.append(self.get(i))
                else:
                    elem = self.get(i)
                    if isinstance(elem, ArraySymbol):
                        returnVal.append(elem.toArray())
                    else:
                        returnVal.append(elem)
            else:
                returnVal.append(None)
        return returnVal

    def to_normalized_array(self, recursive=True) -> list:
        """
        converts the array in a pyton list without nones
        :recursive: convert also arrays in arrays
        :return: the generated python list
        """
        return_value = []
        for i in range(len(self)):
            if i in self.vectors:
                if not recursive:
                    return_value.append(self.get(i[0])) if isinstance(self.get(i), tuple) else return_value.append(self.get(i))
                else:
                    elem = self.get(i)
                    if isinstance(elem, ArraySymbol):
                        return_value.append(elem.to_normalized_array())
                    else:
                        return_value.append(elem[0]) if isinstance(elem, tuple) else return_value.append(elem)
        return return_value

    def clear(self) -> None:
        '''
        removes all values from the array
        '''
        self.vectors = []
        self.array_value = []

    def __len__(self):
        if len(self.vectors) == 0:
            return 0
        return max(self.vectors) + 1

    def __str__(self):
        return str(self.toArray()).replace("None, ", "")
