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

from .type_system import Type
from dataclasses import dataclass
from antlr4.ParserRuleContext import ParserRuleContext

@dataclass
class AbstractExpression:

    ctx: ParserRuleContext

class ArithmeticExpression(AbstractExpression):

    def __init__(self) -> None:
        pass

@dataclass
class Value(AbstractExpression):

    value: int
    type: Type

