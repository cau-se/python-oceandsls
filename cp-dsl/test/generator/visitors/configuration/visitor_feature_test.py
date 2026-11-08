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

TOP_LEVEL = """
        model eval
            feature Base : "description"
            feature Other : "description2"
        """

NESTED = """
        model eval
            feature Base : "description" {
                sub multiple
                    feature inner : "description inner"
                    feature inner2 : "description inner2"
            }
        """


class TestFeatureGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    @parameterized.expand([
        ("top_level", TOP_LEVEL, "feature Base { }", {"Base": True, "Other": False}),
        # A configured feature is activated, the others are not
        # Input: the features Base and Other, 'feature Base { }'
        # Expected Result: Base activated, Other not

        ("other_top_level", TOP_LEVEL, "feature Other { }", {"Base": False, "Other": True}),
        # Only the configured feature is activated
        # Input: the features Base and Other, 'feature Other { }'
        # Expected Result: Other activated, Base not

        ("nested_simple", NESTED, "feature Base {\n activate inner, !inner2\n }",
         {"Base": True, "Base.inner": True, "Base.inner2": False}),
        # Sub-features are activated and deactivated by an activate list
        # Input: 'feature Base { activate inner, !inner2 }'
        # Expected Result: Base and inner activated, inner2 not

        ("nested_complex1", NESTED, "feature Base {\n activate !inner2\n feature inner {}\n }",
         {"Base": True, "Base.inner": True, "Base.inner2": False}),
        # A configured sub-feature is activated
        # Input: 'feature Base { activate !inner2 feature inner {} }'
        # Expected Result: Base and inner activated, inner2 not

        ("nested_complex2", NESTED, "feature Base {\n feature inner {}\n }",
         {"Base": True, "Base.inner": True, "Base.inner2": False}),
        # A sub-feature that is not configured is not activated
        # Input: 'feature Base { feature inner {} }'
        # Expected Result: Base and inner activated, inner2 not

        ("nested_activate_only", NESTED, "feature Base {\n activate inner2\n }",
         {"Base": True, "Base.inner": False, "Base.inner2": True}),
        # Activating one sub-feature
        # Input: 'feature Base { activate inner2 }'
        # Expected Result: Base and inner2 activated, inner not
    ])
    def test_visitFeatureConfiguration(self, test_name, declaration, configuration, expected_activation):
        model = self.parse_declaration_code(declaration)
        self.assertEqual("eval", model.name, test_name)

        model: DeclarationModel = self.parse_code(f"configuration test : eval\n {configuration}", model)

        self.assertEqual("eval", model.name, test_name)
        self.assertEqual("test", model.configuration_name, test_name)
        self.assertEqual([path for path in expected_activation if "." not in path], list(model.features), test_name)
        for path, expected in expected_activation.items():
            names = path.split(".")
            feature = model.features[names[0]]
            for name in names[1:]:
                feature = feature.resolve_feature(name)
            self.assertIsNotNone(feature, f"{test_name}: {path}")
            self.assertEqual(names[-1], feature.name, f"{test_name}: {path}")
            self.assertEqual(expected, feature.is_activated, f"{test_name}: {path}")


if __name__ == '__main__':
    unittest.main()
