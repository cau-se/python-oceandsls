"""Elements for Fortran statements from fxtran parsing"""

__author__ = "sgu"

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

from containment_hash_map import ContainmentHashMap


class CommonBlock:
    """ source for class CommonBlock """

    @final
    @property
    def name(self) -> str:
        return self._name

    @final
    @property
    def variables(self) -> ContainmentHashMap[str, FortranVariable]:
        return self._variables

    @final
    @property
    def node(self):
        return self._node

    @property
    def parent(self) -> object:
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def __init__(self, name, node):
        self._name = name
        self._node = node

        self._variables = ContainmentHashMap(self)
        self._parent = object()
