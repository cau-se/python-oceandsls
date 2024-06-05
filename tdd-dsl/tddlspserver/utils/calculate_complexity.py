""" Implementation for complexity calculation"""

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

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import Enum
from math import log2
from typing import Dict, List, Optional, Set


class UniqueList(list):
    """
    List with unique elements. Resets if added to closed list.
    """
    __closed: bool = False

    def close(self):
        # Close list
        self.__closed = True

    def extend(self, elements: List):
        # Reset if closed
        if self.__closed:
            self.clear()
            __close = False

        # Add elements if not in list
        for element in elements:
            self.append(element)

    def append(self, element):
        # Reset if closed
        if self.__closed:
            self.clear()
            __close = False

        # Add element if not in list
        if not self.__contains__(element):
            super().append(element)


class testability(Enum):
    NONE = 0
    PRO = 1
    CON = 2


@dataclass
class Scope:
    """
    Scope for cyclomatic complexity
    """
    name: str = field(default="")
    type: str = field(default="")
    src: str = field(default="")
    sort_metric: str = field(default="")

    debug: bool = field(default=False)
    debug_seperator: str = field(default="\n")

    routine_types: Set = field(default_factory=lambda: {"function-stmt", "subroutine-stmt"})
    module_types: Set = field(default_factory=lambda: {"module-stmt"})

    conditionals: List[ET.Element] = field(default_factory=lambda: [])
    loops: List[ET.Element] = field(default_factory=lambda: [])
    branches: List[ET.Element] = field(default_factory=lambda: [])
    assignment: List[ET.Element] = field(default_factory=lambda: [])
    declarations: List[ET.Element] = field(default_factory=lambda: [])
    other_stmt: List[ET.Element] = field(default_factory=lambda: [])
    arguments: List[ET.Element] = field(default_factory=lambda: [])
    external_calls: List[ET.Element] = field(default_factory=lambda: [])
    sub_scopes: List = field(default_factory=lambda: [])
    scope_result_names: List[str] = field(default_factory=lambda: [])

    # List of last result declarations
    __scope_result_decl: UniqueList = field(default_factory=lambda: UniqueList())

    # List of operands, operators and their occurrences
    __operands: Dict[str, int] = field(default_factory=lambda: {})
    __operators: Dict[str, int] = field(default_factory=lambda: {})

    # Metrics
    __weighted_metrics: Dict[str, tuple] = field(default_factory=lambda: {})  # Union[tuple[int,float], tuple[float,float] ]
    __testability_difficulty: Optional[float] = field(default=None)
    __testability_index: Optional[float] = field(default=None)
    __normalized_testability_difficulty: Optional[float] = field(default=None)
    __aggregated_testability_difficulty: Optional[float] = field(default=None)
    __test_factor: Optional[float] = field(default=None)
    __testBenefit: Optional[float] = field(default=None)
    __testEffort: Optional[float] = field(default=None)
    __aggregated_test_score: Optional[float] = field(default=None)
    __normalized_test_score: Optional[float] = field(default=None)
    __test_index: Optional[float] = field(default=None)
    __test_score: Optional[float] = field(default=None)

    # Set of operators pairs
    __operator_pairs: Set = field(default_factory=lambda: {"()", "{}", "<>", "[]"})

    ###############################
    # Halstead Complexity Measures
    ###############################

    @property
    def operators(self) -> Dict[str, int]:
        # Recalc pair operator counts
        operators: Dict[str, int] = dict(self.__operators)
        for operator_pair in self.__operator_pairs:
            cnt: int = operators.get(operator_pair, None)
            if cnt:
                cnt: int = int(cnt / 2) + (cnt % 2)
                operators[operator_pair] = cnt

        for sub_scope in self.sub_scopes:
            s_operators: Dict[str, int] = sub_scope.operators

            for key, value in s_operators.items():
                operators[key] = operators.get(key, 0) + value
        return operators

    @property
    def operands(self) -> Dict[str, int]:
        operands: Dict[str, int] = dict(self.__operands)

        for sub_scope in self.sub_scopes:
            s_operands: Dict[str, int] = sub_scope.operands

            decl_elements = sub_scope.declarations
            decl_names: List[str] = []
            for decl_element in decl_elements:
                name_element = decl_element.find(f"{search_global}{name_tag}", ns)
                if name_element is not None:
                    decl_names.append(name_element.text.lower())

            for key, value in s_operands.items():
                if key in decl_names:
                    key = f"{sub_scope.name}.{key}"
                operands[key] = operands.get(key, 0) + value
        return operands

    @property
    def n_operators(self) -> int:
        """
        Number of distinct operators : ηT
        :return: ηT
        """
        return len(self.operators)

    @property
    def n_operands(self) -> int:
        """
        Number of distinct operands : ηD
        :return: ηD
        """
        return len(self.operands)

    @property
    def sum_operators(self) -> int:
        """
        Total number of operators : NT
        :return: NT
        """
        return sum(self.operators.values())

    @property
    def sum_operands(self) -> int:
        """
        Total number of operands : ND
        :return: ND
        """
        return sum(self.operands.values())

    @property
    def ratio_operators(self) -> float:
        """
        Index of operators : nNT = NT / nT
        :return: nNT
        """
        return self.sum_operators / self.n_operators if self.n_operators > 0 else 0

    @property
    def ratio_operands(self) -> float:
        """
        Index of operands : nND = ND / nD
        :return: nND
        """
        return self.sum_operands / self.n_operands if self.n_operands > 0 else 0

    @property
    def vocabulary(self) -> int:
        """
        Program vocabulary: η = ηT + ηD
        :return: η
        """
        return self.n_operators + self.n_operands

    @property
    def program_length(self) -> int:
        """
        Program length: N = NT + ND
        :return: N
        """
        return self.sum_operators + self.sum_operands

    @property
    def calculated_length(self) -> float:
        """
        Calculated estimated program length: N^ = ηT log2 ηT + ηD log2 ηD
        :return:  N^
        """
        nT: int = self.n_operators
        nD: int = self.n_operands

        operator_length: int = nT * log2(nT) if nT > 0 else 0
        operands_length: int = nD * log2(nD) if nD > 0 else 0

        return operator_length + operands_length

    @property
    def volume(self) -> float:
        """
        Volume: V = N × log2(η)
        :return: V
        """
        return self.program_length * log2(self.vocabulary) if self.vocabulary > 0 else 0

    @property
    def difficulty(self) -> float:
        """
        Difficulty : D = ηT/2 × ND/ηD
        :return: D
        """
        nT: int = self.n_operators
        nD: int = self.n_operands
        ND: int = self.sum_operands
        return (nT / 2) * (ND / nD) if nD > 0 else 0

    @property
    def effort(self) -> float:
        """
        Effort: E = D × V
        :return: E
        """
        return self.difficulty * self.volume

    @property
    def time_required_to_program(self) -> float:
        """
        Time required to program: T = E/18
        :return: T
        """
        return self.effort / 18

    @property
    def n_bugs(self) -> float:
        """
        Number of delivered bugs : B = E^{2/3}/3000
        :return: B
        """
        return self.effort ** (2 / 3) / 3000

    ###############################
    # Cyclomatic complexity
    ###############################

    @property
    def n_results(self) -> int:
        n_results: int = len(self.__scope_result_decl)
        for sub_scope in self.sub_scopes:
            n_results += sub_scope.n_results
        return n_results

    @property
    def n_conditionals(self) -> int:
        n_conditionals: int = len(self.conditionals)
        for sub_scope in self.sub_scopes:
            n_conditionals += sub_scope.n_conditionals
        return n_conditionals

    @property
    def n_loops(self) -> int:
        n_loops: int = len(self.loops)
        for sub_scope in self.sub_scopes:
            n_loops += sub_scope.n_loops
        return n_loops

    @property
    def n_branches(self) -> int:
        n_branches: int = len(self.branches)
        for sub_scope in self.sub_scopes:
            n_branches += sub_scope.n_branches
        return n_branches

    @property
    def n_assignment(self) -> int:
        n_assignment: int = len(self.assignment)
        for sub_scope in self.sub_scopes:
            n_assignment += sub_scope.n_assignment
        return n_assignment

    @property
    def n_declarations(self) -> int:
        n_declarations: int = len(self.declarations)
        for sub_scope in self.sub_scopes:
            n_declarations += sub_scope.n_declarations
        return n_declarations

    @property
    def n_other_stmts(self) -> int:
        n_other_stmts: int = len(self.other_stmt)
        for sub_scope in self.sub_scopes:
            n_other_stmts += sub_scope.n_other_stmts
        return n_other_stmts

    @property
    def n_arguments(self) -> int:
        n_arguments: int = len(self.arguments)
        for sub_scope in self.sub_scopes:
            n_arguments += sub_scope.n_arguments
        return n_arguments

    @property
    def n_external_calls(self) -> int:
        n_external_calls: int = len(self.external_calls)
        for sub_scope in self.sub_scopes:
            n_external_calls += sub_scope.n_external_calls
        return n_external_calls

    @property
    def cyclomatic_complexity(self) -> int | None:
        """
        Cyclomatic complexity (CC) function for structures with only one entry point and one exit point.
        Number of predicate variables involved in decision points ("if" statements and loops) plus one
        :return: CC
        """
        # Check structure
        if self.is_routine or self.is_module:
            # Simple structure
            return self.n_conditionals + 1
        else:
            # Unsupported structure
            return None

    @property
    def loc(self) -> int:
        """
        :return: Lines of codes in a scope as number of statements
        """
        return self.n_loops + self.n_branches + self.n_assignment + self.n_other_stmts

    @property
    def n_decision_points(self) -> int:
        """
        :return: Number of decision points in scope
        """
        return self.n_loops + self.n_branches

    @property
    def depth_of_nesting(self) -> int:
        """
        :return: Maximum depth of nesting of scope
        """
        depth_of_nesting: int = 0
        for sub_scope in self.sub_scopes:
            depth_of_nesting = max(depth_of_nesting, 1 + sub_scope.depth_of_nesting)
        return depth_of_nesting

    @property
    def is_testable(self) -> bool:
        return self.is_routine or self.is_module

    @property
    def is_routine(self) -> bool:
        return self.type in self.routine_types

    @property
    def is_module(self) -> bool:
        return self.type in self.module_types

    @property
    def get_sort_metric(self) -> str:
        return self.sort_metric

    ###############################
    # Combining measurements
    ###############################

    def set_weighted_metrics(self):
        self.__weighted_metrics["CC"] = (self.cyclomatic_complexity, self.high_coefficient, testability.CON)  # incl conditionals
        self.__weighted_metrics["LOC"] = (self.loc, self.direct_coefficient, testability.CON)
        self.__weighted_metrics["DEPTH"] = (self.depth_of_nesting, self.high_coefficient, testability.CON)
        self.__weighted_metrics["NP"] = (self.n_arguments, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["NL"] = (self.n_loops, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["NB"] = (self.n_branches, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["NV"] = (self.n_declarations, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["NR"] = (self.n_results, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["NC"] = (self.n_external_calls, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["NYT"] = (self.n_operators, self.low_coefficient, testability.CON)
        self.__weighted_metrics["NYD"] = (self.n_operands, self.low_coefficient, testability.CON)
        self.__weighted_metrics["NT"] = (self.sum_operators, self.low_coefficient, testability.CON)
        self.__weighted_metrics["ND"] = (self.sum_operands, self.low_coefficient, testability.CON)
        self.__weighted_metrics["nNT"] = (self.ratio_operators, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["nND"] = (self.ratio_operands, self.mid_coefficient, testability.CON)
        self.__weighted_metrics["NY"] = (self.vocabulary, self.low_coefficient, testability.CON)
        self.__weighted_metrics["N"] = (self.program_length, self.low_coefficient, testability.CON)
        self.__weighted_metrics["NHAT"] = (self.calculated_length, self.no_coefficient, testability.NONE)
        self.__weighted_metrics["V"] = (self.volume, self.no_coefficient, testability.NONE)
        self.__weighted_metrics["D"] = (self.difficulty, self.no_coefficient, testability.NONE)
        self.__weighted_metrics["E"] = (self.effort, self.no_coefficient, testability.NONE)
        self.__weighted_metrics["T"] = (self.time_required_to_program, self.no_coefficient, testability.NONE)
        self.__weighted_metrics["B"] = (self.n_bugs, self.direct_coefficient, testability.NONE)

        # Reset TAS
        self.__testability_difficulty = None
        self.__test_factor = None

    @property
    def weighted_metrics(self) -> dict[str, tuple]:
        """WM = a * A"""
        if not self.__weighted_metrics:
            self.set_weighted_metrics()

        return self.__weighted_metrics

    @property
    def testability_difficulty(self) -> float:
        """TAS = sum(WM)"""
        if self.__testability_difficulty is None:
            self.__testability_difficulty = 0
            for metric in self.weighted_metrics.values():
                match metric[2]:
                    case testability.CON:
                        self.__testability_difficulty += metric[0] * metric[1]

        return self.__testability_difficulty

    @property
    def testability_index(self) -> float:
        """TAI = 1/ (1 + TAS) ... """
        if self.__testability_difficulty is None or self.__testability_index is None:
            self.__testability_index = 1 / (1 + self.testability_difficulty)

        return self.__testability_index

    @property
    def normalized_testability_difficulty(self) -> float:
        """NTAS = (TAS - min(WM)) / (max(WM) - min(WM))"""
        if self.__testability_difficulty is None or self.__normalized_testability_difficulty is None:
            minWSM: float = 0.0
            maxWSM: float = 0.0
            for metric in self.weighted_metrics.values():
                match metric[2]:
                    case testability.CON:
                        weighted_metric: float = metric[0] * metric[1]
                        minWSM = weighted_metric if weighted_metric < minWSM else minWSM
                        maxWSM = weighted_metric if maxWSM < weighted_metric else maxWSM

            self.__normalized_testability_difficulty = (self.testability_difficulty - minWSM) / (maxWSM - minWSM) if (maxWSM - minWSM) > 0 else 0

        return self.__normalized_testability_difficulty

    @property
    def aggregated_testability_difficulty(self) -> float:
        """ATAS = 1 / n TAS"""
        if self.__testability_difficulty is None or self.__aggregated_testability_difficulty is None:
            n: int = 0

            for metric in self.weighted_metrics.values():
                match metric[2]:
                    case testability.CON:
                        n += 1

            self.__aggregated_testability_difficulty = 1 / n * self.testability_difficulty

        return self.__aggregated_testability_difficulty

    @property
    def test_index(self) -> float:
        """TI = b * TAI """
        if self.__test_index is None:
            self.__test_index = self.test_Benefit * self.testability_index

        return self.__test_index

    @property
    def normalized_test_score(self) -> float:
        """NTS = b * NTAS"""
        if self.__normalized_test_score is None:
            self.__normalized_test_score = self.test_Benefit * self.normalized_testability_difficulty

        return self.__normalized_test_score

    @property
    def aggregated_test_score(self) -> float:
        """ATS = b * ATAS"""
        if self.__aggregated_test_score is None:
            self.__aggregated_test_score = self.test_Benefit * self.aggregated_testability_difficulty

        return self.__aggregated_test_score

    @property
    def test_factor(self) -> float:
        """TF = 1 (g Bugs) / (1 + a CC + b LOC + c Depth + d Parameters + e Branches + f Calls + g Results)"""
        if self.__test_factor is None:
            self.__test_factor = 1 * self.test_Benefit / (1 + self.test_Effort)

        return self.__test_factor

    @property
    def test_Benefit(self):
        if self.__testBenefit is None:
            self.__testBenefit: float = (1 - 1 / (1 + self.score_of(["B"])))

        return self.__testBenefit

    @property
    def test_Effort(self):
        if self.__testEffort is None:
            self.__testEffort: float = self.score_of(["CC", "LOC", "DEPTH", "NP", "NB", "NC", "NR"])

        return self.__testEffort

    ###############################
    # Coefficients
    ###############################

    @property
    def no_coefficient(self) -> float:
        """0.02-0.04"""
        return 0.00

    @property
    def low_coefficient(self) -> float:
        """0.02-0.04"""
        return 0.03

    @property
    def mid_coefficient(self) -> float:
        """0.05-0.09"""
        return 0.07

    @property
    def high_coefficient(self) -> float:
        """0.1-0.15"""
        return 0.12

    @property
    def direct_coefficient(self) -> float:
        """1.0"""
        return 1.00

    ###############################
    # Utils
    ###############################

    def score_of(self, factors: List[str]) -> float:
        score: float = 0
        for factor in factors:
            metric: tuple = self.weighted_metrics[factor]
            score += metric[0] * metric[1]
        return score

    def close_result(self):
        self.__scope_result_decl.close()

    def extend_result(self, elements):
        for element in elements:
            self.append_result(element)

    def append_result(self, element):
        name_element = element.find(f"{search_global}{name_tag}", ns)
        name_element = name_element.text if name_element is not None else None
        if self.is_routine and (name_element in self.scope_result_names or not self.scope_result_names):
            self.__scope_result_decl.append(element)

    def add_operand(self, operand: str):
        operand = operand.lower()
        self.__operands[operand] = self.__operands.get(operand, 0) + 1

    def add_operator(self, operator: str):
        operator = operator.lower()
        for operator_pair in self.__operator_pairs:
            if operator in operator_pair:
                operator = operator_pair
                break

        self.__operators[operator] = self.__operators.get(operator, 0) + 1

    def __str__(self):
        """ toString method """

        if not self.debug:
            return (f"ID: {self.name}{self.debug_seperator}"
                    f"Source: {self.src}{self.debug_seperator}"
                    )
        elif self.debug_seperator is "\n":
            return (f"Scope: {self.name}{self.debug_seperator}"
                    f"Source: {self.src}{self.debug_seperator}"
                    f"Cyclomatic Complexity: {self.cyclomatic_complexity}{self.debug_seperator}"
                    f"Depth of Nesting: {self.depth_of_nesting}{self.debug_seperator}"
                    f"Lines of Code (LOC): {self.loc}{self.debug_seperator}"
                    f"Number of Parameters: {self.n_arguments}{self.debug_seperator}"
                    f"Number of Conditionals: {self.n_conditionals}{self.debug_seperator}"
                    f"Number of Loops: {self.n_loops}{self.debug_seperator}"
                    f"Number of Branches: {self.n_branches}{self.debug_seperator}"
                    f"Number of Variables: {self.n_declarations}{self.debug_seperator}"
                    f"Number of Return Statements: {self.n_results}{self.debug_seperator}"
                    f"Number of Calls to External Functions/Procedures: {self.n_external_calls}{self.debug_seperator}"
                    f"Number of Decision Points: {self.n_decision_points}{self.debug_seperator}"
                    f"Halstead Complexity Measures:{self.debug_seperator}"
                    f"Number of distinct Operators ηT: {self.n_operators}{self.debug_seperator}"
                    f"Number of distinct Operands ηD: {self.n_operands}{self.debug_seperator}"
                    f"Number of total Operators NT: {self.sum_operators}{self.debug_seperator}"
                    f"Number of total Operands ND: {self.sum_operands}{self.debug_seperator}"
                    f"Ratio of Operators nNT: {self.ratio_operators}{self.debug_seperator}"
                    f"Ratio of Operands nND: {self.ratio_operands}{self.debug_seperator}"
                    f"Vocabulary (ηT + ηD): {self.vocabulary}{self.debug_seperator}"
                    f"Program Length (NT + ND): {self.program_length}{self.debug_seperator}"
                    f"Calculated Length: {self.calculated_length}{self.debug_seperator}"
                    f"Volume: {self.volume}{self.debug_seperator}"
                    f"Difficulty: {self.difficulty}{self.debug_seperator}"
                    f"Effort: {self.effort}{self.debug_seperator}"
                    f"Time required to program: {self.time_required_to_program}{self.debug_seperator}"
                    f"Number of delivered bugs: {self.n_bugs}{self.debug_seperator}"
                    # f"Distinct Operators: {self.operators}{self.debug_seperator}"
                    # f"Distinct Operands: {self.operands}{self.debug_seperator}"
                    f"Test Score:{self.debug_seperator}"
                    f"Testability Score: {self.testability_difficulty}{self.debug_seperator}"
                    f"Testability Index: {self.testability_index}{self.debug_seperator}"
                    f"Normalized Testability Score: {self.normalized_testability_difficulty}{self.debug_seperator}"
                    f"Aggregated Testability Score: {self.aggregated_testability_difficulty}{self.debug_seperator}"
                    f"Test Index: {self.test_index}{self.debug_seperator}"
                    f"Normalized Test Score: {self.normalized_test_score}{self.debug_seperator}"
                    f"Aggregated Test Score: {self.aggregated_test_score}{self.debug_seperator}"
                    f"Test Factor: {self.test_factor}"
                    )
        else:
            return (self.debug_seperator.join(str(x) for x in [self.name,
                                                               self.src,
                                                               self.cyclomatic_complexity,
                                                               self.depth_of_nesting,
                                                               self.loc,
                                                               self.n_arguments,
                                                               self.n_conditionals,
                                                               self.n_loops,
                                                               self.n_branches,
                                                               self.n_declarations,
                                                               self.n_results,
                                                               self.n_external_calls,
                                                               self.n_decision_points,
                                                               "",
                                                               self.n_operators,
                                                               self.n_operands,
                                                               self.sum_operators,
                                                               self.sum_operands,
                                                               self.ratio_operators,
                                                               self.ratio_operands,
                                                               self.vocabulary,
                                                               self.program_length,
                                                               self.calculated_length,
                                                               self.volume,
                                                               self.difficulty,
                                                               self.effort,
                                                               self.time_required_to_program,
                                                               self.n_bugs,
                                                               "",
                                                               self.testability_difficulty,
                                                               self.testability_index,
                                                               self.normalized_testability_difficulty,
                                                               self.aggregated_testability_difficulty,
                                                               self.test_index,
                                                               self.normalized_test_score,
                                                               self.aggregated_test_score,
                                                               self.test_factor]))

    ###############################
    # Sort utils
    ###############################

    def __lt__(self, obj):
        return self.sort_index < obj.sort_index

    def __eq__(self, obj):
        return self.sort_index == obj.sort_index

    @property
    def sort_index(self):
        match self.get_sort_metric:
            case "Cyclomatic Complexity":
                return self.cyclomatic_complexity
            case "Depth of Nesting":
                return self.depth_of_nesting
            case "Lines of Code":
                return self.loc
            case "LOC":
                return self.loc
            case "Number of Parameters":
                return self.n_arguments
            case "Number of Conditionals":
                return self.n_conditionals
            case "Number of Loops":
                return self.n_loops
            case "Number of Branches":
                return self.n_branches
            case "Number of Variables":
                return self.n_declarations
            case "Number of Return Statements":
                return self.n_results
            case "Number of Calls":
                return self.n_external_calls
            case "Number of Decision Points":
                return self.n_decision_points
            case "Number of distinct Operators":
                return self.n_operators
            case "Number of distinct Operands":
                return self.n_operands
            case "Number of total Operators":
                return self.sum_operators
            case "Number of total Operands":
                return self.sum_operands
            case "Operator Index":
                return self.ratio_operators
            case "Operands Index":
                return self.ratio_operands
            case "Vocabulary":
                return self.vocabulary
            case "Program Length":
                return self.program_length
            case "Calculated Length":
                return self.calculated_length
            case "Volume":
                return self.volume
            case "Difficulty":
                return self.difficulty
            case "Effort":
                return self.effort
            case "Time required to program":
                return self.time_required_to_program
            case "Number of delivered bugs":
                return self.n_bugs
            case "Testability Difficulty":
                return self.testability_difficulty
            case "Testability Index":
                return self.testability_index
            case "Normalized Testability Difficulty":
                return self.normalized_testability_difficulty
            case "Aggregated Testability Difficulty":
                return self.aggregated_testability_difficulty
            case "Test Index":
                return self.test_index
            case "Normalized Test Score":
                return self.normalized_test_score
            case "Aggregated Test Score":
                return self.aggregated_test_score
            case "Test Factor":
                return self.test_factor
            case _:
                return self.test_factor


# Set the namespace as Fxtran for XPath expressions
ns = {"fx": "http://fxtran.net/#syntax"}

# Filters
name_tag: str = "n"
literal_tag: str = "l"
code_tag: str = "c"
external_paren_tag = "parens-R"
parameter_tag: str = "arg-N"
result_tag: str = "result-spec"
name_element_tag: str = "named-E"
operand_element_tag: str = "op-E"
operand_tags: Set = {name_tag, literal_tag}
operator_tags: Set = {code_tag}

search_global: str = ".//fx:"
search_local: str = "./fx:"


def is_external_call(a_stmt_element: ET.Element):
    # check if an element contains a routine call
    return a_stmt_element.find(path=f"{search_global}{external_paren_tag}", namespaces=ns) is not None


def add_operands_to(scope: Scope, element: ET.Element):
    for tag in operand_tags:
        operands = element.findall(path=f"{search_global}{tag}", namespaces=ns)
        for operand in operands:
            if operand.text:
                scope.add_operand(operand.text.strip())


def add_operators_to(scope: Scope, element: ET.Element):
    for tag in operator_tags:
        operators = element.findall(path=f"{search_local}{tag}", namespaces=ns)
        for operator in operators:
            if operator.text:
                scope.add_operator(operator.text.strip())


def calculate_metrics(xml_path: str = None, src: str = None, sort_metric=None, debug: bool = False, debug_seperator: str = "\n") -> dict[str, Scope]:
    """
    Calculate cyclomatic complexity and halstead complexity measures from fxtran formatted xml file for Fortran code
    :param xml_path: Path to fxtran xml files
    :param src: Optional path to Fortran source files
    :param sort_metric: Optional sort metric
    :param debug: Optional debug output
    :param debug_seperator: Optional seperator for debug output
    :return: None
    """

    if xml_path is None:
        return {}
    # Get the root element
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Filters
    conditional_elements: Set = {"condition-E", "test-E", "do-V"}
    loop_elements: Set = {"do-stmt"}
    branch_elements: Set = {"if-then-stmt", "else-stmt"}
    branch_end_elements: Set = {"end-if-stmt"}
    assignment_elements: Set = {"a-stmt"}
    declaration_elements: Set = {"EN-decl"}
    other_stmt_elements: Set = {"-stmt"}

    # Dynamically extracted scope-changing elements
    dyn_scope_elements = set()
    dyn_end_scope_elements = set()
    # Stack to track the current scope
    scope_stack = []
    # Routines defined in scope
    scopes: Dict[str, Scope] = {}

    for element in root.iter():
        # Check if element is scope-changing by searching for scope-ending element

        # Extract the tag name without the namespace
        tag = element.tag.rsplit(sep="}", maxsplit=1)[-1]

        if tag.endswith("-stmt"):
            # Extract the statement name
            stmt_name = tag.rsplit(sep="-", maxsplit=1)[0]
            # Find scope name element
            name_element = element.find(path=f"{search_global}{stmt_name}-N", namespaces=ns)

            if tag not in dyn_scope_elements and name_element is not None:
                end_tag = "end-" + tag
                if root.find(path=f"{search_global}{end_tag}", namespaces=ns) is not None:
                    dyn_scope_elements.add(tag)
                    dyn_end_scope_elements.add(end_tag)

        # Set scope
        current_scope: Scope = scope_stack[-1] if scope_stack else None

        # Reduce the scope stack when leaving scopes
        if tag in tuple(dyn_end_scope_elements):

            name = ".".join(list(map(lambda scope: scope.name, scope_stack)))

            scopes[name] = scope_stack.pop()

            if current_scope:
                # Check for operators
                add_operators_to(current_scope, element)

        # Extend the scope stack when entering scopes
        elif tag in tuple(dyn_scope_elements):

            # Extract scope name
            scope_name = name_element.find(path=f"{search_global}{name_tag}", namespaces=ns)
            scope_name = scope_name.text if scope_name is not None else ""

            # Extract scope type
            scope_type = element.tag.split(ns["fx"] + "}", maxsplit=1)[1]

            # Extract scope parameters
            scope_arguments = element.findall(path=f"{search_global}{parameter_tag}", namespaces=ns)

            # Extract names of scope return statements in scope declaration
            scope_result_elements = element.findall(path=f"{search_global}{result_tag}", namespaces=ns)
            scope_results: List[str] = []
            for result_element in scope_result_elements:
                scope_results.extend(list(map(lambda element: element.text, result_element.findall(f"{search_global}{name_tag}", namespaces=ns))))

            # Build new scope
            new_scope = Scope(
                name=scope_name,
                type=scope_type,
                arguments=scope_arguments,
                scope_result_names=scope_results,
                src=src,
                sort_metric=sort_metric,
                debug=debug,
                debug_seperator=debug_seperator)

            # Add scope to parent
            if current_scope:
                current_scope.sub_scopes.append(new_scope)

            # Update scope stack
            scope_stack.append(new_scope)

            # Check new scope for operators
            add_operators_to(new_scope, element)

        else:
            # Non-scope elements

            if current_scope:
                # Check for operators
                add_operators_to(current_scope, element)

            # Extract conditional statements
            if element.tag.endswith(tuple(conditional_elements)):

                # Check if operand elements exist
                operand_elements: List[ET.Element] = element.findall(path=f"{search_global}{operand_element_tag}", namespaces=ns)
                if operand_elements:
                    # Add only leaf operand elements
                    for operand_element in operand_elements:
                        sub_operand_elements: List[ET.Element] = operand_element.findall(path=f"{search_global}{operand_element_tag}", namespaces=ns)
                        if not sub_operand_elements:
                            current_scope.conditionals.append(operand_element)
                else:
                    # Add one element if no operand is found
                    current_scope.conditionals.append(element)

            # Extract loop statements
            elif element.tag.endswith(tuple(loop_elements)):
                current_scope.loops.append(element)

            # Extract branching statements
            elif element.tag.endswith(tuple(branch_end_elements)):
                current_scope.close_result()

            # Extract branching statements
            elif element.tag.endswith(tuple(branch_elements)):
                current_scope.branches.append(element)

            # Extract assignment statements
            elif element.tag.endswith(tuple(assignment_elements)):
                current_scope.assignment.append(element)

                # Add as result statement if it is the last call of the return statement
                current_scope.append_result(element)

                # Check for external calls
                named_elements = element.findall(path=f"{search_global}{name_element_tag}", namespaces=ns)
                for named_element in named_elements:
                    if is_external_call(named_element):
                        current_scope.external_calls.append(named_element)

                # Check for operands
                add_operands_to(current_scope, element)
            # Extract declaration statements
            elif element.tag.endswith(tuple(declaration_elements)):
                current_scope.declarations.append(element)

                # Check for operands
                add_operands_to(current_scope, element)

            # Extract other statements
            elif element.tag.endswith(tuple(other_stmt_elements)):
                current_scope.other_stmt.append(element)

    return scopes
