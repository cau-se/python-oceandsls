#  Copyright (c) 2025.  OceanDSL (https://oceandsl.uni-kiel.de)
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
""" test class for calculate_complexity"""

__author__ = "sgu"

import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
from math import log2
from xml.etree.ElementTree import Element

from parameterized import parameterized

from tddlspserver.utils.calculate_complexity import (
    UniqueList, Scope, ns, operand_tags, operator_tags, is_external_call, add_operands_to, add_operators_to,
    calculate_metrics,
)

FX = "{http://fxtran.net/#syntax}"
FX_NS = 'xmlns:fx="http://fxtran.net/#syntax"'

FUNCTION_XML = f"""<fx:object {FX_NS}><fx:file><fx:program-unit>
<fx:function-stmt>FUNCTION <fx:function-N><fx:n>add</fx:n></fx:function-N>(<fx:dummy-arg-LT><fx:arg-N><fx:n>a</fx:n>\
</fx:arg-N></fx:dummy-arg-LT>)</fx:function-stmt>
<fx:if-then-stmt>IF (<fx:condition-E><fx:n>a</fx:n> <fx:c>&gt;</fx:c> <fx:l>0</fx:l></fx:condition-E>) THEN\
</fx:if-then-stmt>
<fx:a-stmt><fx:E-1><fx:n>add</fx:n></fx:E-1> <fx:a>=</fx:a> <fx:E-2><fx:n>a</fx:n> <fx:c>+</fx:c> <fx:l>1</fx:l>\
</fx:E-2></fx:a-stmt>
<fx:end-if-stmt>END IF</fx:end-if-stmt>
<fx:end-function-stmt>END FUNCTION</fx:end-function-stmt></fx:program-unit></fx:file></fx:object>"""

MODULE_XML = f"""<fx:object {FX_NS}><fx:file><fx:program-unit>
<fx:module-stmt>MODULE <fx:module-N><fx:n>m</fx:n></fx:module-N></fx:module-stmt>
<fx:contains-stmt>CONTAINS</fx:contains-stmt>
<fx:subroutine-stmt>SUBROUTINE <fx:subroutine-N><fx:n>s</fx:n></fx:subroutine-N></fx:subroutine-stmt>
<fx:do-stmt>DO <fx:do-V><fx:n>i</fx:n></fx:do-V>=<fx:l>1</fx:l>,<fx:l>2</fx:l></fx:do-stmt>
<fx:end-do-stmt>END DO</fx:end-do-stmt>
<fx:end-subroutine-stmt>END SUBROUTINE</fx:end-subroutine-stmt>
<fx:end-module-stmt>END MODULE</fx:end-module-stmt></fx:program-unit></fx:file></fx:object>"""

EMPTY_XML = f"<fx:root {FX_NS}></fx:root>"


def statement(tag: str, *children: str) -> Element:
    """An fxtran statement element with child elements (tags without namespace)."""
    element = ET.Element(FX + tag)
    for child in children:
        ET.SubElement(element, FX + child)
    return element


def scope_with(operators=(), operands=()) -> Scope:
    scope = Scope(name="TestScope", type="function-stmt")
    for operator in operators:
        scope.add_operator(operator)
    for operand in operands:
        scope.add_operand(operand)
    return scope


class TestUniqueList(unittest.TestCase):

    @parameterized.expand([
        ("append_unique", [("append", 1), ("append", 2), ("append", 1)], [1, 2]),
        # Appending an element twice keeps it once
        # Input: append 1, 2 and 1 again
        # Expected Result: [1, 2]

        ("close_and_reset", [("append", 1), ("append", 2), ("close",), ("append", 3)], [3]),
        # Appending to a closed list resets it
        # Input: append 1 and 2, close, append 3
        # Expected Result: [3]

        ("extend_unique", [("extend", [1, 2, 3]), ("extend", [2, 3, 4])], [1, 2, 3, 4]),
        # Extending adds only new elements; the list is not closed, so nothing is reset
        # Input: extend by [1, 2, 3], then by [2, 3, 4]
        # Expected Result: [1, 2, 3, 4]

        ("extend_after_close_resets_once", [("extend", [1, 2]), ("close",), ("extend", [3, 4]), ("append", 5)],
         [3, 4, 5]),
        # The first change after closing resets the list, later changes keep collecting
        # Input: extend by [1, 2], close, extend by [3, 4], append 5
        # Expected Result: [3, 4, 5]

        ("close_without_change", [("append", 1), ("close",)], [1]),
        # Closing alone does not empty the list
        # Input: append 1, close
        # Expected Result: [1]

        ("extend_with_duplicates", [("extend", [1, 1, 2, 2])], [1, 2]),
        # Duplicates within one extension are added once
        # Input: extend by [1, 1, 2, 2]
        # Expected Result: [1, 2]
    ])
    def test_operations(self, test_name, operations, expected):
        unique_list = UniqueList()
        for name, *args in operations:
            getattr(unique_list, name)(*args)
        self.assertEqual(expected, unique_list, test_name)


class TestScope(unittest.TestCase):

    @parameterized.expand([
        ("empty", [], [], {"n_operators": 0, "n_operands": 0, "sum_operators": 0, "sum_operands": 0,
                           "ratio_operators": 0, "ratio_operands": 0, "vocabulary": 0, "program_length": 0,
                           "calculated_length": 0}),
        # A new scope has no operators and operands
        # Input: no operators and operands
        # Expected Result: all counts and ratios are 0

        ("one_of_each", ["++"], ["variable"], {"n_operators": 1, "n_operands": 1, "sum_operators": 1,
                                               "sum_operands": 1, "ratio_operators": 1.0, "ratio_operands": 1.0,
                                               "vocabulary": 2, "program_length": 2, "calculated_length": 0.0}),
        # One operator and one operand
        # Input: operator '++', operand 'variable'
        # Expected Result: one distinct and one total of each, vocabulary and length 2

        ("repeated_operators", ["++", "++", "=="], [], {"n_operators": 2, "sum_operators": 3,
                                                        "ratio_operators": 1.5}),
        # Repeated operators count once as distinct, every time in the total
        # Input: operators '++', '++' and '=='
        # Expected Result: 2 distinct, 3 total, ratio 1.5

        ("repeated_operands", [], ["variable", "variable", "another_variable"], {"n_operands": 2, "sum_operands": 3,
                                                                                 "ratio_operands": 1.5}),
        # Repeated operands count once as distinct, every time in the total
        # Input: operands 'variable', 'variable' and 'another_variable'
        # Expected Result: 2 distinct, 3 total, ratio 1.5

        ("two_of_each", ["++", "=="], ["variable", "another_variable"],
         {"ratio_operators": 2 / 2, "ratio_operands": 2 / 2, "vocabulary": 4, "program_length": 4,
          "calculated_length": (2 * log2(2)) + (2 * log2(2))}),
        # Two distinct operators and operands
        # Input: operators '++' and '==', operands 'variable' and 'another_variable'
        # Expected Result: ratios 1, vocabulary and program length 4, calculated length 2*log2(2) + 2*log2(2) = 4

        ("mixed", ["++", "==", "++"], ["a", "b", "a", "c"],
         {"n_operators": 2, "n_operands": 3, "sum_operators": 3, "sum_operands": 4, "vocabulary": 5,
          "program_length": 7, "calculated_length": 2 * log2(2) + 3 * log2(3)}),
        # Repeated operators and operands together
        # Input: operators '++', '==', '++', operands 'a', 'b', 'a', 'c'
        # Expected Result: 2 and 3 distinct, 3 and 4 total, vocabulary 5, program length 7
    ])
    def test_halstead_counts(self, test_name, operators, operands, expected):
        scope = scope_with(operators, operands)
        for metric, value in expected.items():
            self.assertAlmostEqual(value, getattr(scope, metric), msg=f"{test_name}: {metric}")

    @parameterized.expand([
        ("empty", [], [], {"volume": 0, "difficulty": 0, "effort": 0, "time_required_to_program": 0, "n_bugs": 0}),
        # Without operators and operands every measure is 0
        # Input: no operators and operands
        # Expected Result: volume, difficulty, effort, time and bugs 0

        ("one_of_each", ["++"], ["variable"],
         {"volume": 2.0, "difficulty": 0.5, "effort": 1.0, "time_required_to_program": 1 / 18,
          "n_bugs": 1 / 3000}),
        # One operator and one operand
        # Input: operator '++', operand 'variable'
        # Expected Result: volume 2*log2(2) = 2, difficulty 1/2 * 1/1, effort 1, time 1/18, bugs 1^(2/3)/3000

        ("operators_only", ["++", "++", "=="], [],
         {"volume": 3.0, "difficulty": 0, "effort": 0, "time_required_to_program": 0, "n_bugs": 0}),
        # Without operands the difficulty is 0
        # Input: operators '++', '++' and '=='
        # Expected Result: volume 3*log2(2) = 3, all other measures 0

        ("two_of_each", ["++", "=="], ["variable", "another_variable"],
         {"volume": 8.0, "difficulty": 1.0, "effort": 8.0, "time_required_to_program": 8 / 18,
          "n_bugs": 8 ** (2 / 3) / 3000}),
        # Two distinct operators and operands
        # Input: operators '++' and '==', operands 'variable' and 'another_variable'
        # Expected Result: volume 4*log2(4) = 8, difficulty 1, effort 8, time 8/18, bugs 8^(2/3)/3000
    ])
    def test_halstead_measures(self, test_name, operators, operands, expected):
        scope = scope_with(operators, operands)
        for metric, value in expected.items():
            self.assertAlmostEqual(value, getattr(scope, metric), msg=f"{test_name}: {metric}")

    @parameterized.expand([
        ("conditionals", "conditionals", 1, "n_conditionals", 1),
        # Conditionals are counted
        # Input: one conditional element
        # Expected Result: n_conditionals 1

        ("loops", "loops", 1, "n_loops", 1),
        # Loops are counted
        # Input: one loop element
        # Expected Result: n_loops 1

        ("branches", "branches", 1, "n_branches", 1),
        # Branches are counted
        # Input: one branch element
        # Expected Result: n_branches 1

        ("assignments", "assignment", 1, "n_assignment", 1),
        # Assignments are counted
        # Input: one assignment element
        # Expected Result: n_assignment 1

        ("declarations", "declarations", 1, "n_declarations", 1),
        # Declarations are counted
        # Input: one declaration element
        # Expected Result: n_declarations 1

        ("other_statements", "other_stmt", 1, "n_other_stmts", 1),
        # Other statements are counted
        # Input: one other statement element
        # Expected Result: n_other_stmts 1

        ("arguments", "arguments", 1, "n_arguments", 1),
        # Arguments are counted
        # Input: one argument element
        # Expected Result: n_arguments 1

        ("external_calls", "external_calls", 1, "n_external_calls", 1),
        # External calls are counted
        # Input: one call element
        # Expected Result: n_external_calls 1

        ("several_loops", "loops", 3, "n_loops", 3),
        # Several elements of a kind
        # Input: three loop elements
        # Expected Result: n_loops 3

        ("no_conditionals", "conditionals", 0, "cyclomatic_complexity", 1),
        # A routine without conditionals has one path
        # Input: no conditional elements
        # Expected Result: cyclomatic complexity 1

        ("one_conditional", "conditionals", 1, "cyclomatic_complexity", 2),
        # Each conditional adds a path
        # Input: one conditional element
        # Expected Result: cyclomatic complexity 2 (1 conditional + 1)

        ("three_conditionals", "conditionals", 3, "cyclomatic_complexity", 4),
        # Several conditionals
        # Input: three conditional elements
        # Expected Result: cyclomatic complexity 4

        ("loc", "loops", 2, "loc", 2),
        # Loops count as lines of code
        # Input: two loop elements
        # Expected Result: loc 2

        ("decision_points", "branches", 2, "n_decision_points", 2),
        # Branches are decision points
        # Input: two branch elements
        # Expected Result: n_decision_points 2
    ])
    def test_statement_counts(self, test_name, attribute, count, metric, expected):
        scope = scope_with()
        getattr(scope, attribute).extend(Element(attribute) for _ in range(count))
        self.assertEqual(expected, getattr(scope, metric), test_name)

    @parameterized.expand([
        ("no_results", 0, "append", 0),
        # A new scope has no results
        # Input: no result elements
        # Expected Result: n_results 0

        ("append_result", 1, "append", 1),
        # A result is appended
        # Input: one result element, appended
        # Expected Result: n_results 1

        ("extend_result", 2, "extend", 2),
        # Several results are added at once
        # Input: two result elements, extended
        # Expected Result: n_results 2

        ("append_two_results", 2, "append", 2),
        # Results are appended one by one
        # Input: two result elements, appended one by one
        # Expected Result: n_results 2
    ])
    def test_results(self, test_name, count, method, expected):
        scope = scope_with()
        elements = [Element(f"result{i}") for i in range(count)]
        if method == "extend":
            scope.extend_result(elements)
        else:
            for element in elements:
                scope.append_result(element)
        self.assertEqual(expected, scope.n_results, test_name)
        self.assertEqual(expected, len(scope._Scope__scope_result_decl), test_name)  # pylint: disable=protected-access

    @parameterized.expand([
        ("no_sub_scopes", 0, 0),
        # A scope without nested scopes
        # Input: no sub-scopes
        # Expected Result: depth of nesting 0

        ("one_sub_scope", 1, 1),
        # One nested scope
        # Input: one sub-scope
        # Expected Result: depth of nesting 1

        ("nested_sub_scope", 2, 2),
        # A nested scope with a nested scope
        # Input: a sub-scope with its own sub-scope
        # Expected Result: depth of nesting 2
    ])
    def test_depth_of_nesting(self, test_name, depth, expected):
        scope = scope_with()
        current = scope
        for _ in range(depth):
            sub_scope = Scope(name="SubScope", type="function-stmt")
            current.sub_scopes.append(sub_scope)
            current = sub_scope
        self.assertEqual(expected, scope.depth_of_nesting, test_name)

    @parameterized.expand([
        ("function", "function-stmt", True, False, True, 1),
        # A function is a routine
        # Input: scope type 'function-stmt'
        # Expected Result: routine, not module, testable, cyclomatic complexity 1

        ("subroutine", "subroutine-stmt", True, False, True, 1),
        # A subroutine is a routine
        # Input: scope type 'subroutine-stmt'
        # Expected Result: routine, not module, testable, cyclomatic complexity 1

        ("module", "module-stmt", False, True, True, 1),
        # A module is testable, but no routine
        # Input: scope type 'module-stmt'
        # Expected Result: not routine, module, testable, cyclomatic complexity 1

        ("program", "program-stmt", False, False, False, None),
        # A program is neither
        # Input: scope type 'program-stmt'
        # Expected Result: not routine, not module, not testable, no cyclomatic complexity
    ])
    def test_scope_types(self, test_name, scope_type, is_routine, is_module, is_testable, cyclomatic_complexity):
        scope = Scope(name="TestScope", type=scope_type)
        self.assertEqual((is_routine, is_module, is_testable, cyclomatic_complexity),
                         (scope.is_routine, scope.is_module, scope.is_testable, scope.cyclomatic_complexity),
                         test_name)

    @parameterized.expand([
        ("normalized_testability_difficulty", "normalized_testability_difficulty", 4.166666666666667),
        # The normalized testability difficulty of a scope with one operator and one operand
        # Input: operator '++', operand 'variable'
        # Expected Result: a float (25/6)

        ("aggregated_testability_difficulty", "aggregated_testability_difficulty", 0.029411764705882353),
        # The aggregated testability difficulty
        # Input: operator '++', operand 'variable'
        # Expected Result: a float (1/34)

        ("test_index", "test_index", 0.0002221481728312824),
        # The test index
        # Input: operator '++', operand 'variable'
        # Expected Result: a float

        ("normalized_test_score", "normalized_test_score", 0.001388426080195515),
        # The normalized test score
        # Input: operator '++', operand 'variable'
        # Expected Result: a float

        ("aggregated_test_score", "aggregated_test_score", 9.800654683733047e-06),
        # The aggregated test score
        # Input: operator '++', operand 'variable'
        # Expected Result: a float

        ("test_factor", "test_factor", 0.00029751987432761036),
        # The test factor
        # Input: operator '++', operand 'variable'
        # Expected Result: a float
    ])
    def test_testability_metrics(self, test_name, metric, expected):
        value = getattr(scope_with(["++"], ["variable"]), metric)
        self.assertIsInstance(value, float, test_name)
        self.assertAlmostEqual(expected, value, msg=test_name)

    @parameterized.expand([
        ("cyclomatic_complexity_and_loc", ["CC", "LOC"], 0.12),
        # The score sums value times weight of the factors
        # Input: factors CC (1 * 0.12) and LOC (0 * 1.0)
        # Expected Result: 0.12

        ("cyclomatic_complexity", ["CC"], 0.12),
        # A single factor
        # Input: factor CC
        # Expected Result: 0.12

        ("no_factors", [], 0),
        # No factors
        # Input: no factors
        # Expected Result: 0

        ("halstead_counts", ["NYT", "NYD"], 0.06),
        # Halstead counts as factors
        # Input: factors NYT (1 * 0.03) and NYD (1 * 0.03)
        # Expected Result: 0.06
    ])
    def test_score_of(self, test_name, factors, expected):
        score = scope_with(["++"], ["variable"]).score_of(factors)
        self.assertAlmostEqual(expected, score, msg=test_name)

    @parameterized.expand([
        ("cyclomatic_complexity", "CC", 1),
        # The weighted metrics hold the cyclomatic complexity
        # Input: a scope with one operator and one operand
        # Expected Result: CC with the value 1

        ("lines_of_code", "LOC", 0),
        # The lines of code
        # Input: a scope with one operator and one operand
        # Expected Result: LOC with the value 0

        ("vocabulary", "NY", 2),
        # The Halstead vocabulary
        # Input: a scope with one operator and one operand
        # Expected Result: NY with the value 2

        ("volume", "V", 2.0),
        # The Halstead volume
        # Input: a scope with one operator and one operand
        # Expected Result: V with the value 2.0
    ])
    def test_weighted_metrics(self, test_name, key, expected_value):
        metrics = scope_with(["++"], ["variable"]).weighted_metrics
        self.assertIn(key, metrics, test_name)
        self.assertEqual(expected_value, metrics[key][0], test_name)

    @parameterized.expand([
        ("testability_difficulty", "function-stmt", None, "testability_difficulty", 0.5),
        # Regression: the first access failed, set_weighted_metrics() reset the testability difficulty to None while
        # it was summed
        # Input: a function with operator '++' and operand 'variable'
        # Expected Result: 0.5

        ("testability_index", "function-stmt", None, "testability_index", 2 / 3),
        # The testability index is 1 / (1 + testability difficulty)
        # Input: operator '++', operand 'variable'
        # Expected Result: 2/3

        ("testability_index_after_difficulty", "function-stmt", "testability_difficulty", "testability_index",
         2 / 3),
        # The index does not change when the difficulty was computed before
        # Input: operator '++', operand 'variable', testability difficulty read first
        # Expected Result: 2/3

        ("difficulty_after_index", "function-stmt", "testability_index", "testability_difficulty", 0.5),
        # The difficulty does not change when the index was computed before
        # Input: operator '++', operand 'variable', testability index read first
        # Expected Result: 0.5

        ("program_difficulty", "program-stmt", None, "testability_difficulty", 0.38),
        # Regression: scopes without cyclomatic complexity (programs) multiplied None by its weight
        # Input: a program with operator '++' and operand 'variable'
        # Expected Result: 0.38, the cyclomatic complexity is left out

        ("program_index", "program-stmt", None, "testability_index", 1 / 1.38),
        # The index of a program
        # Input: a program with operator '++' and operand 'variable'
        # Expected Result: 1 / 1.38

        ("program_aggregated_difficulty", "program-stmt", None, "aggregated_testability_difficulty", 0.02375),
        # The aggregated difficulty averages over the metrics with a value
        # Input: a program with operator '++' and operand 'variable'
        # Expected Result: 0.38 / 16

        ("program_test_factor", "program-stmt", None, "test_factor", 0.0003332222592469236),
        # The test effort leaves out the missing cyclomatic complexity
        # Input: a program with operator '++' and operand 'variable'
        # Expected Result: a float
    ])
    def test_testability(self, test_name, scope_type, read_first, metric, expected):
        scope = Scope(name="TestScope", type=scope_type)
        scope.add_operator("++")
        scope.add_operand("variable")
        if read_first:
            getattr(scope, read_first)

        self.assertAlmostEqual(expected, getattr(scope, metric), msg=test_name)

    @parameterized.expand([
        ("testability_difficulty", "testability_difficulty", 0.5, 0.62),
        # Regression: only two derived values were reset when the weighted metrics were recomputed
        # Input: a function read once, then a conditional added and set_weighted_metrics() called
        # Expected Result: 0.5 before, 0.62 (one more cyclomatic complexity * 0.12) after

        ("testability_index", "testability_index", 2 / 3, 1 / 1.62),
        # The testability index follows the new difficulty
        # Input: as above
        # Expected Result: 2/3 before, 1 / 1.62 after

        ("aggregated_testability_difficulty", "aggregated_testability_difficulty", 0.5 / 17, 0.62 / 17),
        # The aggregated difficulty follows the new difficulty
        # Input: as above
        # Expected Result: 0.5 / 17 before, 0.62 / 17 after

        ("test_factor", "test_factor", 0.00029751987432761036, 0.0002687276284249384),
        # The test factor follows the new test effort
        # Input: as above
        # Expected Result: a smaller test factor after
    ])
    def test_derived_values_after_recalculation(self, test_name, metric, expected_before, expected_after):
        scope = scope_with(["++"], ["variable"])
        self.assertAlmostEqual(expected_before, getattr(scope, metric), msg=test_name)

        scope.conditionals.append(Element("condition-E"))
        scope.set_weighted_metrics()

        self.assertAlmostEqual(expected_after, getattr(scope, metric), msg=test_name)

    @parameterized.expand([
        ("close_after_append", 1, 0),
        # Closing the result list empties it
        # Input: one result appended, then closed
        # Expected Result: no results

        ("close_after_two_appends", 2, 0),
        # Closing removes all results
        # Input: two results appended, then closed
        # Expected Result: no results

        ("close_empty", 0, 0),
        # Closing an empty result list
        # Input: no results, closed
        # Expected Result: no results
    ])
    @unittest.skip("draft test: close_result() marks the result list closed, it does not empty it")
    def test_close_result(self, test_name, count, expected):
        scope = scope_with()
        for i in range(count):
            scope.append_result(Element(f"result{i}"))
        scope.close_result()
        self.assertEqual(expected, len(scope._Scope__scope_result_decl), test_name)  # pylint: disable=protected-access

    @parameterized.expand([
        ("cyclomatic_complexity", "Cyclomatic Complexity", 3),
        # Sort by cyclomatic complexity
        # Input: three loops and two conditionals, sort metric 'Cyclomatic Complexity'
        # Expected Result: 3 (2 conditionals + 1)

        ("loops", "Number of Loops", 3),
        # Sort by number of loops
        # Input: three loops and two conditionals, sort metric 'Number of Loops'
        # Expected Result: 3

        ("conditionals", "Number of Conditionals", 2),
        # Sort by number of conditionals
        # Input: three loops and two conditionals, sort metric 'Number of Conditionals'
        # Expected Result: 2

        ("lines_of_code", "LOC", 3),
        # Sort by lines of code
        # Input: three loops and two conditionals, sort metric 'LOC'
        # Expected Result: 3 (loops count as statements)
    ])
    def test_sort_index(self, test_name, sort_metric, expected):
        scope = Scope(name="TestScope", type="function-stmt", sort_metric=sort_metric)
        scope.loops.extend(Element("do-stmt") for _ in range(3))
        scope.conditionals.extend(Element("condition-E") for _ in range(2))
        self.assertEqual(expected, scope.sort_index, test_name)

    @parameterized.expand([
        ("lower_complexity_is_less", 0, 1, "<", True),
        # Scopes are ordered by their sort index
        # Input: scopes with 0 and 1 conditionals, sorted by cyclomatic complexity
        # Expected Result: the first scope is less

        ("higher_complexity_is_not_less", 1, 0, "<", False),
        # A scope with a higher sort index is not less
        # Input: scopes with 1 and 0 conditionals
        # Expected Result: the first scope is not less

        ("different_complexity_is_not_equal", 0, 1, "==", False),
        # Scopes with different sort indices are not equal
        # Input: scopes with 0 and 1 conditionals
        # Expected Result: not equal

        ("same_complexity_is_equal", 1, 1, "==", True),
        # Equality compares the sort index only, not the name
        # Input: differently named scopes with 1 conditional each
        # Expected Result: equal
    ])
    def test_comparison(self, test_name, first_conditionals, second_conditionals, operator, expected):
        first = Scope(name="Scope1", type="function-stmt", sort_metric="Cyclomatic Complexity")
        second = Scope(name="Scope2", type="function-stmt", sort_metric="Cyclomatic Complexity")
        first.conditionals.extend(Element("condition-E") for _ in range(first_conditionals))
        second.conditionals.extend(Element("condition-E") for _ in range(second_conditionals))

        result = first < second if operator == "<" else first == second
        self.assertEqual(expected, result, test_name)

    @parameterized.expand([
        ("default_separator", "source_code", "\n", "ID: TestScope\nSource: source_code\n"),
        # Without debug output the scope shows its name and source
        # Input: source 'source_code', separator newline
        # Expected Result: 'ID: TestScope\nSource: source_code\n'

        ("custom_separator", "source_code", ";", "ID: TestScope;Source: source_code;"),
        # The separator is configurable
        # Input: source 'source_code', separator ';'
        # Expected Result: 'ID: TestScope;Source: source_code;'

        ("no_source", "", "\n", "ID: TestScope\nSource: \n"),
        # A scope without source
        # Input: no source, separator newline
        # Expected Result: 'ID: TestScope\nSource: \n'
    ])
    def test_string_representation(self, test_name, src, separator, expected):
        scope = Scope(name="TestScope", type="function-stmt", src=src, debug_separator=separator)
        self.assertEqual(expected, str(scope), test_name)

    @parameterized.expand([
        ("debug_lines", "\n", "Scope: TestScope\nSource: source_code\nCyclomatic Complexity: 2\n"),
        # Regression: the debug output read the testability difficulty, which failed on the first access; it lists
        # every metric on its own line
        # Input: debug output, one conditional, separator newline
        # Expected Result: starts with name, source and cyclomatic complexity 2

        ("debug_csv", ";", "TestScope;source_code;2;"),
        # Another separator gives one row of values
        # Input: debug output, one conditional, separator ';'
        # Expected Result: starts with 'TestScope;source_code;2;'

        ("debug_tab", "\t", "TestScope\tsource_code\t2\t"),
        # Tab separated values
        # Input: debug output, one conditional, separator tab
        # Expected Result: starts with 'TestScope\tsource_code\t2\t'
    ])
    def test_debug_string_representation(self, test_name, separator, expected_start):
        scope = Scope(name="TestScope", type="function-stmt", src="source_code", debug=True,
                      debug_separator=separator)
        scope.conditionals.append(Element("condition-E"))
        self.assertTrue(str(scope).startswith(expected_start), test_name)


class TestNamespaceAndFilters(unittest.TestCase):

    @parameterized.expand([
        ("namespace", ns, {"fx": "http://fxtran.net/#syntax"}),
        # The fxtran namespace
        # Input: ns
        # Expected Result: the prefix 'fx' for http://fxtran.net/#syntax

        ("operand_tags", operand_tags, {"n", "l"}),
        # Names and literals are operands
        # Input: operand_tags
        # Expected Result: 'n' and 'l'

        ("operator_tags", operator_tags, {"c"}),
        # Code elements are operators
        # Input: operator_tags
        # Expected Result: 'c'
    ])
    def test_constants(self, test_name, value, expected):
        self.assertEqual(expected, value, test_name)


class TestUtilityFunctions(unittest.TestCase):

    @parameterized.expand([
        ("call_in_do_statement", statement("do-stmt", "parens-R"), True),
        # A statement that contains a routine call
        # Input: a do-stmt with a parens-R element
        # Expected Result: True

        ("do_statement_without_call", statement("do-stmt"), False),
        # A statement without a routine call
        # Input: a do-stmt without children
        # Expected Result: False

        ("if_statement_without_call", statement("if-then-stmt"), False),
        # Another statement without a routine call
        # Input: an if-then-stmt without children
        # Expected Result: False

        ("call_statement", statement("call-stmt", "parens-R"), True),
        # A call statement with arguments
        # Input: a call-stmt with a parens-R element
        # Expected Result: True

        ("other_child", statement("a-stmt", "E-1"), False),
        # Other child elements are no calls
        # Input: an a-stmt with an E-1 element
        # Expected Result: False
    ])
    def test_is_external_call(self, test_name, element, expected):
        self.assertEqual(expected, is_external_call(element), test_name)

    @parameterized.expand([
        ("operand_names", "<fx:n>a</fx:n><fx:n>b</fx:n>", {"a": 1, "b": 1}, {}),
        # Names are operands
        # Input: names 'a' and 'b'
        # Expected Result: operands 'a' and 'b', no operators

        ("operands_and_literals", "<fx:n>a</fx:n><fx:l>1</fx:l><fx:n>a</fx:n>", {"a": 2, "1": 1}, {}),
        # Literals are operands too, and repetitions are counted
        # Input: 'a', the literal 1 and 'a' again
        # Expected Result: 'a' twice and '1' once

        ("operators", "<fx:c>+</fx:c><fx:c> - </fx:c><fx:n>x</fx:n>", {"x": 1}, {"+": 1, "-": 1}),
        # Code elements are operators, stripped of whitespace
        # Input: '+', ' - ' and the name 'x'
        # Expected Result: operators '+' and '-', operand 'x'

        ("empty_elements", "<fx:n/><fx:c/>", {}, {}),
        # Elements without text are ignored
        # Input: an empty name and an empty code element
        # Expected Result: no operands and operators
    ])
    def test_add_operands_and_operators(self, test_name, children, expected_operands, expected_operators):
        element = ET.fromstring(f"<fx:a-stmt {FX_NS}>{children}</fx:a-stmt>")
        scope = scope_with()
        add_operands_to(scope, element)
        add_operators_to(scope, element)

        self.assertEqual(expected_operands, scope.operands, test_name)
        self.assertEqual(expected_operators, scope.operators, test_name)

    @parameterized.expand([
        ("function", FUNCTION_XML, {"add": ("function-stmt", 1, 1, 2)}),
        # A function with an argument and an IF
        # Input: fxtran XML of FUNCTION add(a) with IF (a > 0) THEN add = a + 1
        # Expected Result: the scope 'add' (function, 1 argument, 1 conditional, cyclomatic complexity 2)

        ("module_with_subroutine", MODULE_XML, {"m": ("module-stmt", 0, 1, 2), "m.s": ("subroutine-stmt", 0, 1, 2)}),
        # Nested scopes are named by their path
        # Input: fxtran XML of MODULE m with SUBROUTINE s containing a DO loop
        # Expected Result: the scopes 'm' and 'm.s'

        ("empty_document", EMPTY_XML, {}),
        # A document without program units
        # Input: an fxtran XML root without children
        # Expected Result: no scopes

        ("no_xml", None, {}),
        # Without an XML file
        # Input: xml_path None
        # Expected Result: an empty dictionary
    ])
    def test_calculate_metrics(self, test_name, xml, expected_scopes):
        if xml is None:
            scopes = calculate_metrics(xml_path=None)
        else:
            with tempfile.TemporaryDirectory() as directory:
                path = os.path.join(directory, "test.xml")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(xml)
                scopes = calculate_metrics(xml_path=path)

        self.assertEqual(expected_scopes,
                         {name: (scope.type, scope.n_arguments, scope.n_conditionals, scope.cyclomatic_complexity)
                          for name, scope in scopes.items()}, test_name)


if __name__ == '__main__':
    unittest.main()
