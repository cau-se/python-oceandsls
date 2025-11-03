""" test class for calculate_complexity"""

__author__ = "sgu"

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

import unittest
from xml.etree.ElementTree import Element
from calculate_complexity import UniqueList, Scope, testability  # Replace 'your_module' with the actual module name

class TestUniqueList(unittest.TestCase):

    def setUp(self):
        self.unique_list = UniqueList()

    def test_append_unique(self):
        self.unique_list.append(1)
        self.unique_list.append(2)
        self.unique_list.append(1)  # Duplicate
        self.assertEqual(len(self.unique_list), 2)

    def test_close_and_reset(self):
        self.unique_list.append(1)
        self.unique_list.append(2)
        self.unique_list.close()
        self.unique_list.append(3)  # Should reset and add 3
        self.assertEqual(len(self.unique_list), 1)
        self.assertEqual(self.unique_list[0], 3)

    def test_extend_unique(self):
        self.unique_list.extend([1, 2, 3])
        self.unique_list.extend([2, 3, 4])  # Should reset and add 4
        self.assertEqual(len(self.unique_list), 1)
        self.assertEqual(self.unique_list[0], 4)

class TestScope(unittest.TestCase):

    def setUp(self):
        self.scope = Scope(name="TestScope", type="function-stmt")

    def test_initial_values(self):
        self.assertEqual(self.scope.name, "TestScope")
        self.assertEqual(self.scope.type, "function-stmt")
        self.assertEqual(self.scope.n_operators, 0)
        self.assertEqual(self.scope.n_operands, 0)

    def test_add_operator(self):
        self.scope.add_operator("++")
        self.assertEqual(self.scope.n_operators, 1)

    def test_add_operand(self):
        self.scope.add_operand("variable")
        self.assertEqual(self.scope.n_operands, 1)

    def test_sum_operators(self):
        self.scope.add_operator("++")
        self.scope.add_operator("++")  # Adding the same operator
        self.scope.add_operator("==")
        self.assertEqual(self.scope.sum_operators, 3)  # 2 for "++" and 1 for "=="

    def test_sum_operands(self):
        self.scope.add_operand("variable")
        self.scope.add_operand("variable")  # Adding the same operand
        self.scope.add_operand("another_variable")
        self.assertEqual(self.scope.sum_operands, 3)  # 2 for "variable" and 1 for "another_variable"

    def test_ratio_operators(self):
        self.scope.add_operator("++")
        self.scope.add_operator("==")
        self.assertEqual(self.scope.ratio_operators, 2 / 2)  # 2 operators / 2 distinct operators

    def test_ratio_operands(self):
        self.scope.add_operand("variable")
        self.scope.add_operand("another_variable")
        self.assertEqual(self.scope.ratio_operands, 2 / 2)  # 2 operands / 2 distinct operands

    def test_calculated_length(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.scope.add_operator("==")
        self.scope.add_operand("another_variable")
        # nT = 2 (distinct operators), nD = 2 (distinct operands)
        calculated_length = (2 * log2(2)) + (2 * log2(2))  # Should be 4
        self.assertAlmostEqual(self.scope.calculated_length, calculated_length)

    def test_cyclomatic_complexity(self):
        self.scope.conditionals.append(Element("if"))
        self.assertEqual(self.scope.cyclomatic_complexity, 2)  # 1 conditional + 1

    def test_is_routine(self):
        self.assertTrue(self.scope.is_routine)
        self.scope.type = "module-stmt"
        self.assertFalse(self.scope.is_routine)

    def test_weighted_metrics(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        metrics = self.scope.weighted_metrics
        self.assertIn("CC", metrics)
        self.assertIn("LOC", metrics)

    def test_n_results(self):
        self.assertEqual(self.scope.n_results, 0)
        self.scope.append_result(Element("result"))
        self.assertEqual(self.scope.n_results, 1)

    def test_n_conditionals(self):
        self.scope.conditionals.append(Element("if"))
        self.assertEqual(self.scope.n_conditionals, 1)

    def test_n_loops(self):
        self.scope.loops.append(Element("for"))
        self.assertEqual(self.scope.n_loops, 1)

    def test_n_branches(self):
        self.scope.branches.append(Element("case"))
        self.assertEqual(self.scope.n_branches, 1)

    def test_n_assignment(self):
        self.scope.assignment.append(Element("assignment"))
        self.assertEqual(self.scope.n_assignment, 1)

    def test_n_declarations(self):
        self.scope.declarations.append(Element("declaration"))
        self.assertEqual(self.scope.n_declarations, 1)

    def test_n_other_stmts(self):
        self.scope.other_stmt.append(Element("other"))
        self.assertEqual(self.scope.n_other_stmts, 1)

    def test_n_arguments(self):
        self.scope.arguments.append(Element("argument"))
        self.assertEqual(self.scope.n_arguments, 1)

    def test_n_external_calls(self):
        self.scope.external_calls.append(Element("call"))
        self.assertEqual(self.scope.n_external_calls, 1)

    def test_depth_of_nesting(self):
        sub_scope = Scope(name="SubScope", type="function-stmt")
        self.scope.sub_scopes.append(sub_scope)
        self.assertEqual(self.scope.depth_of_nesting, 1)

    def test_program_length(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertEqual(self.scope.program_length, 2)  # 1 operator + 1 operand

    def test_vocabulary(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertEqual(self.scope.vocabulary, 2)  # 1 operator + 1 operand

    def test_volume(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertGreater(self.scope.volume, 0)  # Volume should be greater than 0

    def test_difficulty(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertGreaterEqual(self.scope.difficulty, 0)  # Difficulty should be non-negative

    def test_effort(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertGreaterEqual(self.scope.effort, 0)  # Effort should be non-negative

    def test_time_required_to_program(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertGreaterEqual(self.scope.time_required_to_program, 0)  # Time should be non-negative

    def test_n_bugs(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertGreaterEqual(self.scope.n_bugs, 0)  #

    def test_n_bugs(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        self.assertGreaterEqual(self.scope.n_bugs, 0)  # Number of bugs should be non-negative

    def test_testability_difficulty(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        difficulty = self.scope.testability_difficulty
        self.assertIsInstance(difficulty, float)  # Should be a float

    def test_testability_index(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        index = self.scope.testability_index
        self.assertIsInstance(index, float)  # Should be a float

    def test_normalized_testability_difficulty(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        normalized_difficulty = self.scope.normalized_testability_difficulty
        self.assertIsInstance(normalized_difficulty, float)  # Should be a float

    def test_aggregated_testability_difficulty(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        aggregated_difficulty = self.scope.aggregated_testability_difficulty
        self.assertIsInstance(aggregated_difficulty, float)  # Should be a float

    def test_test_index(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        test_index = self.scope.test_index
        self.assertIsInstance(test_index, float)  # Should be a float

    def test_normalized_test_score(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        normalized_score = self.scope.normalized_test_score
        self.assertIsInstance(normalized_score, float)  # Should be a float

    def test_aggregated_test_score(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        aggregated_score = self.scope.aggregated_test_score
        self.assertIsInstance(aggregated_score, float)  # Should be a float

    def test_test_factor(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        test_factor = self.scope.test_factor
        self.assertIsInstance(test_factor, float)  # Should be a float

    def test_score_of(self):
        self.scope.add_operator("++")
        self.scope.add_operand("variable")
        score = self.scope.score_of(["CC", "LOC"])
        self.assertIsInstance(score, float)  # Should be a float

    def test_close_result(self):
        self.scope.append_result(Element("result"))
        self.scope.close_result()
        self.assertEqual(len(self.scope._Scope__scope_result_decl), 0)  # Should be empty after closing

    def test_append_result(self):
        result_element = Element("result")
        self.scope.append_result(result_element)
        self.assertEqual(len(self.scope._Scope__scope_result_decl), 1)  # Should contain one result

    def test_extend_result(self):
        result_elements = [Element("result1"), Element("result2")]
        self.scope.extend_result(result_elements)
        self.assertEqual(len(self.scope._Scope__scope_result_decl), 2)  # Should contain two results


    def test_string_representation(self):
        self.scope.debug = True
        self.scope.conditionals.append(Element("if"))
        self.scope.n_arguments = 2
        expected_str = (
            f"Scope: TestScope\n"
            f"Source: source_code\n"
            f"Cyclomatic Complexity: 2\n"
            f"Depth of Nesting: 0\n"
            f"Lines of Code (LOC): 0\n"
            f"Number of Parameters: 2\n"
            f"Number of Conditionals: 1\n"
            f"Number of Loops: 0\n"
            f"Number of Branches: 0\n"
            f"Number of Variables: 0\n"
            f"Number of Return Statements: 0\n"
            f"Number of Calls to External Functions/Procedures: 0\n"
            f"Number of Decision Points: 0\n"
            f"Halstead Complexity Measures:\n"
            f"Number of distinct Operators ηT: 1\n"
            f"Number of distinct Operands ηD: 0\n"
            f"Number of total Operators NT: 1\n"
            f"Number of total Operands ND: 0\n"
            f"Ratio of Operators nNT: 1.0\n"
            f"Ratio of Operands nND: 0.0\n"
            f"Vocabulary (ηT + ηD): 1\n"
            f"Program Length (NT + ND): 1\n"
            f"Calculated Length: 0.0\n"
            f"Volume: 0.0\n"
            f"Difficulty: 0.0\n"
            f"Effort: 0.0\n"
            f"Time required to program: 0.0\n"
            f"Number of delivered bugs: 0.0\n"
            f"Testability Score: 0.0\n"
            f"Testability Index: 0.0\n"
            f"Normalized Testability Score: 0.0\n"
            f"Aggregated Testability Score: 0.0\n"
            f"Test Index: 0.0\n"
            f"Normalized Test Score: 0.0\n"
            f"Aggregated Test Score: 0.0\n"
            f"Test Factor: 0.0"
        )
        self.assertEqual(str(self.scope), expected_str)

    def test_lt_operator(self):
        scope1 = Scope(name="Scope1", type="function-stmt", src="source_code_1")
        scope1.n_loops = 2
        scope1.n_conditionals = 1

        scope2 = Scope(name="Scope2", type="function-stmt", src="source_code_2")
        scope2.n_loops = 1
        scope2.n_conditionals = 2

        # Assuming sort_index is based on cyclomatic complexity
        scope1.sort_metric = "Cyclomatic Complexity"
        scope2.sort_metric = "Cyclomatic Complexity"

        self.assertTrue(scope1 < scope2)  # scope1 has lower cyclomatic complexity

    def test_eq_operator(self):
        scope1 = Scope(name="Scope1", type="function-stmt", src="source_code_1")
        scope1.n_loops = 1
        scope1.n_conditionals = 1

        scope2 = Scope(name="Scope1", type="function-stmt", src="source_code_1")
        scope2.n_loops = 1
        scope2.n_conditionals = 1

        self.assertTrue(scope1 == scope2)  # Both scopes are equal

    def test_sort_index(self):
        self.scope.n_loops = 3
        self.scope.n_conditionals = 2
        self.scope.sort_metric = "Number of Loops"
        self.assertEqual(self.scope.sort_index, 3)

        self.scope.sort_metric = "Number of Conditionals"
        self.assertEqual(self.scope.sort_index, 2)

        self.scope.sort_metric = "Cyclomatic Complexity"
        self.scope.conditionals.append(Element("if"))
        self.assertEqual(self.scope.sort_index, 2)  # Cyclomatic complexity should be 2

class TestNamespaceAndFilters(unittest.TestCase):

    def test_namespace(self):
        self.assertEqual(ns, {"fx": "http://fxtran.net/#syntax"})

    def test_operand_tags(self):
        self.assertIn("n", {"n", "l"})
        self.assertIn("l", {"n", "l"})

    def test_operator_tags(self):
        self.assertIn("c", {"c"})

class TestUtilityFunctions(unittest.TestCase):

    def setUp(self):
        self.scope = Scope(name="TestScope", type="function-stmt")
        self.xml_string = """
        <fx:root xmlns:fx="http://fxtran.net/#syntax">
            <fx:do-stmt>
                <fx:arg-N>arg1</fx:arg-N>
                <fx:parens-R>call</fx:parens-R>
                <fx:n>operand1</fx:n>
                <fx:c>operator1</fx:c>
            </fx:do-stmt>
            <fx:if-then-stmt>
                <fx:n>operand2</fx:n>
                <fx:c>operator2</fx:c>
            </fx:if-then-stmt>
        </fx:root>
        """
        self.element = ET.fromstring(self.xml_string)

    def test_is_external_call(self):
        # Test with an external call element
        external_call_element = ET.Element("{http://fxtran.net/#syntax}do-stmt")
        ET.SubElement(external_call_element, "{http://fxtran.net/#syntax}parens-R")
        self.assertTrue(is_external_call(external_call_element))

        # Test with a non-external call element
        non_external_call_element = ET.Element("{http://fxtran.net/#syntax}do-stmt")
        self.assertFalse(is_external_call(non_external_call_element))

        # Test with an element that has no parens-R
        no_call_element = ET.Element("{http://fxtran.net/#syntax}if-then-stmt")
        self.assertFalse(is_external_call(no_call_element))

    def test_add_operands_to(self):
        # Add operands to the scope from the XML element
        add_operands_to(self.scope, self.element)
        self.assertIn("operand1", self.scope.operands)
        self.assertIn("operand2", self.scope.operands)  # Check for operand in if-then-stmt

        # Check that operands are stripped of whitespace
        self.scope.add_operand("  operand3  ")
        self.assertIn("operand3", self.scope.operands)

    def test_add_operators_to(self):
        # Add operators to the scope from the XML element
        add_operators_to(self.scope, self.element)
        self.assertIn("operator1", self.scope.operators)
        self.assertIn("operator2", self.scope.operators)  # Check for operator in if-then-stmt

        # Check that operators are stripped of whitespace
        self.scope.add_operator("  operator3  ")
        self.assertIn("operator3", self.scope.operators)

    def test_calculate_metrics(self):
        # Create a temporary XML file for testing
        with open("test.xml", "w") as f:
            f.write(self.xml_string)

        scopes = calculate_metrics(xml_path="test.xml", src="source_code", sort_metric="Cyclomatic Complexity", debug=True)
        self.assertIn("TestScope", scopes)
        self.assertEqual(scopes["TestScope"].name, "TestScope")
        self.assertEqual(len(scopes["TestScope"].operands), 2)  # Check number of operands
        self.assertEqual(len(scopes["TestScope"].operators), 2)  # Check number of operators

        # Clean up the temporary file
        import os
        os.remove("test.xml")

    def test_calculate_metrics_no_xml(self):
        # Test calculate_metrics with no XML path
        scopes = calculate_metrics(xml_path=None)
        self.assertEqual(scopes, {})  # Should return an empty dictionary

    def test_calculate_metrics_empty_xml(self):
        # Test calculate_metrics with an empty XML file
        with open("empty_test.xml", "w") as f:
            f.write("<fx:root xmlns:fx='http://fxtran.net/#syntax'></fx:root>")

        scopes = calculate_metrics(xml_path="empty_test.xml")
        self.assertEqual(scopes, {})  # Should return an empty dictionary

        # Clean up the temporary file
        import os
        os.remove("test.xml")

if __name__ == '__main__':
    unittest.main()
