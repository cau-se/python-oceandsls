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

from model.declaration_model import DeclarationModel

from test_utils import AbstractTestGeneratorConfigurationVisitor

class TestGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    def test_visitConfigurationModel_plain(self):
        model = self.parse_declaration_code("model eval")
        self.assertEqual(model.name, "eval", "Name not set")

        model = self.parse_code("configuration test : eval", model)
        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")

    def test_visitConfigurationModel_group(self):
        model = self.parse_declaration_code("""
                model eval
                    group example : "description" {
                        def param1 int : meter = 0
                    }
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        model:DeclarationModel = self.parse_code("configuration test : eval", model)
        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")
        self.assertEqual(len(model.groups), 1, "Wrong set of groups")
        self.assertIsNotNone(model.groups["example"], "Missing group")
        self.assertEqual(model.groups["example"].name, "example", "Wrong group name")

    def test_visitConfigurationModel_feature(self):
        model = self.parse_declaration_code("""
                model eval
                    feature Base : "description"
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        model:DeclarationModel = self.parse_code("configuration test : eval", model)
        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")
        self.assertEqual(len(model.features), 1, "Wrong set of features")
        self.assertIsNotNone(model.features["Base"], "Missing feature")
        self.assertEqual(model.features["Base"].name, "Base", "Wrong feature name")

if __name__ == '__main__':
    unittest.main()
