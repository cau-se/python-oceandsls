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

from model.declaration_model import DeclarationModel, Feature

from gen.visitors.test_utils import AbstractTestGeneratorConfigurationVisitor

class TestFeatureGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    def test_visitFeatureConfiguration(self):
        model = self.parse_declaration_code("""
                model eval
                    feature Base : "description"
                    feature Other : "description2"
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        model:DeclarationModel = self.parse_code("""
                configuration test : eval
                    feature Base { }
                """, model)
        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")
        self.assertEqual(len(model.features), 2, "Wrong set of features")

        self.assertIsNotNone(model.features["Base"], "Missing 'Base' feature")
        self.assertEqual(model.features["Base"].name, "Base", "'Base' expected as feature name")
        self.assertEqual(model.features["Base"].is_activated, True, "'base' must be set")

        self.assertIsNotNone(model.features["Other"], "Missing 'Other' feature")
        self.assertEqual(model.features["Other"].name, "Other", "'Other' expected as feature name")
        self.assertEqual(model.features["Other"].is_activated, False, "'Other' must be set")

    def test_visitFeatureConfiguration_nested_simple(self):
        model = self.parse_declaration_code("""
                model eval
                    feature Base : "description" {
                        sub multiple
                            feature inner : "description inner"
                            feature inner2 : "description inner2"
                    }
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        model:DeclarationModel = self.parse_code("""
                configuration test : eval
                    feature Base {
                        activate inner, !inner2
                    }
                """, model)

        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")
        self.assertEqual(len(model.features), 1, "Wrong set of features")

        base:Feature = model.features["Base"]

        self.assertIsNotNone(base, "Missing 'Base' feature")
        self.assertEqual(base.name, "Base", "'Base' expected as feature name")
        self.assertEqual(base.is_activated, True, "'Base' must be set to true")

        inner = base.resolve_feature("inner")

        self.assertIsNotNone(inner, "Missing 'inner' feature")
        self.assertEqual(inner.name, "inner", "'inner' expected as feature name")
        self.assertEqual(inner.is_activated, True, "'inner' must be set to true")

        inner2 = base.resolve_feature("inner2")

        self.assertIsNotNone(inner2, "Missing 'inner2' feature")
        self.assertEqual(inner2.name, "inner2", "'inner2' expected as feature name")
        self.assertEqual(inner2.is_activated, False, "'inner2' must be set to false")

    def test_visitFeatureConfiguration_nested_complex1(self):
        model = self.parse_declaration_code("""
                model eval
                    feature Base : "description" {
                        sub multiple
                            feature inner : "description inner"
                            feature inner2 : "description inner2"
                    }
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        model:DeclarationModel = self.parse_code("""
                configuration test : eval
                    feature Base {
                        activate !inner2
                        feature inner {}
                    }
                """, model)

        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")
        self.assertEqual(len(model.features), 1, "Wrong set of features")

        base:Feature = model.features["Base"]

        self.assertIsNotNone(base, "Missing 'Base' feature")
        self.assertEqual(base.name, "Base", "'Base' expected as feature name")
        self.assertEqual(base.is_activated, True, "'Base' must be set to true")

        inner = base.resolve_feature("inner")

        self.assertIsNotNone(inner, "Missing 'inner' feature")
        self.assertEqual(inner.name, "inner", "'inner' expected as feature name")
        self.assertEqual(inner.is_activated, True, "'inner' must be set to true")

        inner2 = base.resolve_feature("inner2")

        self.assertIsNotNone(inner2, "Missing 'inner2' feature")
        self.assertEqual(inner2.name, "inner2", "'inner2' expected as feature name")
        self.assertEqual(inner2.is_activated, False, "'inner2' must be set to false")

    def test_visitFeatureConfiguration_nested_complex2(self):
        model = self.parse_declaration_code("""
                model eval
                    feature Base : "description" {
                        sub multiple
                            feature inner : "description inner"
                            feature inner2 : "description inner2"
                    }
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        model:DeclarationModel = self.parse_code("""
                configuration test : eval
                    feature Base {
                        feature inner {}
                    }
                """, model)

        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")
        self.assertEqual(len(model.features), 1, "Wrong set of features")

        base:Feature = model.features["Base"]

        self.assertIsNotNone(base, "Missing 'Base' feature")
        self.assertEqual(base.name, "Base", "'Base' expected as feature name")
        self.assertEqual(base.is_activated, True, "'Base' must be set to true")

        inner = base.resolve_feature("inner")

        self.assertIsNotNone(inner, "Missing 'inner' feature")
        self.assertEqual(inner.name, "inner", "'inner' expected as feature name")
        self.assertEqual(inner.is_activated, True, "'inner' must be set to true")

        inner2 = base.resolve_feature("inner2")

        self.assertIsNotNone(inner2, "Missing 'inner2' feature")
        self.assertEqual(inner2.name, "inner2", "'inner2' expected as feature name")
        self.assertEqual(inner2.is_activated, False, "'inner2' must be set to false")

if __name__ == '__main__':
    unittest.main()
