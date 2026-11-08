#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributedBaseType on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

__author__ = "reiner"

import unittest

from parameterized import parameterized

from cpdsl.model.declaration_model import DeclarationModel

from generator.visitors.test_utils import AbstractTestGeneratorConfigurationVisitor


class TestBaseGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    @parameterized.expand([
        ("plain", "model eval", "configuration test : eval", "test", [], []),
        # A configuration sets its name and keeps the model name
        # Input: the declaration 'model eval' and 'configuration test : eval'
        # Expected Result: the model eval with the configuration test, no groups and features

        ("group", """
                model eval
                    group example : "description" {
                        def param1 int : meter = 0
                    }
                """, "configuration test : eval", "test", ["example"], []),
        # The groups of the declaration are kept
        # Input: a declaration with the group example and 'configuration test : eval'
        # Expected Result: the model eval with the configuration test and the group example

        ("feature", """
                model eval
                    feature Base : "description"
                """, "configuration test : eval", "test", [], ["Base"]),
        # The features of the declaration are kept
        # Input: a declaration with the feature Base and 'configuration test : eval'
        # Expected Result: the model eval with the configuration test and the feature Base

        ("group_and_feature", """
                model eval
                    group example : "description" {
                        def param1 int : meter = 0
                    }
                    feature Base : "description"
                """, "configuration other : eval", "other", ["example"], ["Base"]),
        # Groups and features together, another configuration name
        # Input: a declaration with the group example and the feature Base, 'configuration other : eval'
        # Expected Result: the model eval with the configuration other, the group example and the feature Base
    ])
    def test_visitConfigurationModel(self, test_name, declaration, configuration, expected_configuration,
                                     expected_groups, expected_features):
        model = self.parse_declaration_code(declaration)
        self.assertEqual("eval", model.name, test_name)

        model: DeclarationModel = self.parse_code(configuration, model)

        self.assertEqual("eval", model.name, test_name)
        self.assertEqual(expected_configuration, model.configuration_name, test_name)
        self.assertEqual(expected_groups, list(model.groups), test_name)
        for name in expected_groups:
            self.assertEqual(name, model.groups[name].name, test_name)
        self.assertEqual(expected_features, list(model.features), test_name)
        for name in expected_features:
            self.assertEqual(name, model.features[name].name, test_name)


if __name__ == '__main__':
    unittest.main()
