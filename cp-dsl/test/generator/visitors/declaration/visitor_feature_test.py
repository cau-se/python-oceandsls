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

from cpdsl.model.declaration_model import Feature, EKind
from cpdsl.model.type_system import BaseType

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags

from generator.visitors.test_utils import AbstractTestGeneratorDeclarationVisitor

PARAMETER_MODEL = """
    model eval
        required feature Base : "Base description" {
            group TestParams : "Parameter group description" {
                def p1 int : meter , "p1 description" = 0
                def p2 float : meter = 2.5
                def p3 int : meter = 7
            }
        }
"""

RELATIONS_MODEL = """
    model eval
        required feature Base : "Base description" {
            sub alternative
                feature Feat1 : "Feature one"
                feature Feat2 : "Feature two"
        }
        feature Second : "Second description" {
            requires Base
        }
        feature Alternate : "Alternate description" {
            requires Base, Second
            excludes Base.Feat2
        }
"""

FEATURE_SET_MODEL = """
    model eval
        required feature Base : "Base description" {
            sub %s
                feature Feat1 : "Feature one"
                feature Feat2 : "Feature two"
        }
        feature Optional : "Optional description"
"""


def find_feature(model, path):
    """A top-level feature by name or a sub-feature of the first feature set as 'Feature.SubFeature'."""
    names = path.split(".")
    feature = model.features.get(names[0])
    for name in names[1:]:
        feature = feature.feature_sets[0].features.get(name)
    return feature


class TestFeatureGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    @parameterized.expand([
        ("int_parameter_with_description", "p1", BaseType("int"), 0, "p1 description"),
        # Parameters of a group belong to the group of their feature; the description is unquoted
        # Input: 'def p1 int : meter , "p1 description" = 0' in the group TestParams of the feature Base
        # Expected Result: p1 of type int with the default value 0 and the description p1 description

        ("float_parameter", "p2", BaseType("float"), 2.5, ""),
        # A parameter without description
        # Input: 'def p2 float : meter = 2.5'
        # Expected Result: p2 of type float with the default value 2.5

        ("last_parameter", "p3", BaseType("int"), 7, ""),
        # The last parameter of the group
        # Input: 'def p3 int : meter = 7'
        # Expected Result: p3 of type int with the default value 7
    ])
    def test_visitFeatureAssignStat_parameter(self, test_name, name, expected_type, expected_value,
                                              expected_description):
        model = self.parse_code(PARAMETER_MODEL)

        base_feature: Feature = model.features.get("Base")
        self.assertEqual(["Base"], list(model.features), test_name)
        self.assertEqual(["TestParams"], list(base_feature.groups), test_name)
        group = base_feature.groups["TestParams"]
        self.assertEqual("Parameter group description", group.description, test_name)
        self.assertEqual(["p1", "p2", "p3"], list(group.parameters), test_name)
        parameter = group.parameters[name]
        self.assertEqual(expected_type, parameter.type, test_name)
        self.assertEqual(expected_value, parameter.default_value.value, test_name)
        self.assertEqual(expected_description, parameter.description, test_name)

    @parameterized.expand([
        ("no_relations", "Base", [], []),
        # A feature without requires and excludes
        # Input: the feature Base
        # Expected Result: no required and no excluded features

        ("requires_one", "Second", ["Base"], []),
        # A feature requiring another feature
        # Input: 'requires Base'
        # Expected Result: the feature Base is required

        ("requires_two_excludes_sub_feature", "Alternate", ["Base", "Second"], ["Base.Feat2"]),
        # Several required features and an excluded sub-feature
        # Input: 'requires Base, Second' and 'excludes Base.Feat2'
        # Expected Result: Base and Second are required, Feat2 of Base is excluded
    ])
    def test_visitFeatureAssignStat_requires_excludes(self, test_name, feature_name, expected_requires,
                                                      expected_excludes):
        model = self.parse_code(RELATIONS_MODEL)

        feature: Feature = model.features.get(feature_name)

        self.assertIsInstance(feature, Feature, test_name)
        self.assertEqual(feature_name, feature.name, test_name)
        self.assertEqual(len(expected_requires), len(feature.requires), test_name)
        for required, path in zip(feature.requires, expected_requires):
            self.assertIs(find_feature(model, path), required, f"{test_name}: {path}")
        self.assertEqual(len(expected_excludes), len(feature.excludes), test_name)
        for excluded, path in zip(feature.excludes, expected_excludes):
            self.assertIs(find_feature(model, path), excluded, f"{test_name}: {path}")

    @parameterized.expand([
        ("required_feature", "alternative", "Base", "Base description", True, [EKind.ALTERNATIVE]),
        # A required feature with a feature set
        # Input: 'required feature Base : "Base description" { sub alternative ... }'
        # Expected Result: the required feature Base with one alternative feature set of Feat1 and Feat2

        ("multiple_feature_set", "multiple", "Base", "Base description", True, [EKind.MULTIPLE]),
        # A feature set of which several features may be selected
        # Input: 'required feature Base : "Base description" { sub multiple ... }'
        # Expected Result: the required feature Base with one multiple feature set of Feat1 and Feat2

        ("first_sub_feature", "alternative", "Base.Feat1", "Feature one", False, []),
        # The first feature of the feature set
        # Input: 'feature Feat1 : "Feature one"'
        # Expected Result: the optional feature Feat1 without feature sets

        ("second_sub_feature", "alternative", "Base.Feat2", "Feature two", False, []),
        # The second feature of the feature set
        # Input: 'feature Feat2 : "Feature two"'
        # Expected Result: the optional feature Feat2 without feature sets

        ("optional_feature", "multiple", "Optional", "Optional description", False, []),
        # A feature without 'required' and body
        # Input: 'feature Optional : "Optional description"'
        # Expected Result: the optional feature Optional without feature sets
    ])
    def test_visitFeatureGroupAssignStat_base(self, test_name, kind, path, expected_description, expected_required,
                                              expected_kinds):
        model = self.parse_code(FEATURE_SET_MODEL % kind)

        feature: Feature = find_feature(model, path)

        self.assertIsInstance(feature, Feature, test_name)
        self.assertEqual(path.split(".")[-1], feature.name, test_name)
        self.assertEqual(expected_description, feature.description, test_name)
        self.assertEqual(expected_required, feature.required, test_name)
        self.assertEqual(expected_kinds, [feature_set.kind for feature_set in feature.feature_sets], test_name)
        for feature_set in feature.feature_sets:
            self.assertEqual(["Feat1", "Feat2"], list(feature_set.features), test_name)

    @parameterized.expand([
        ("alternative", "alternative", EKind.ALTERNATIVE),
        # The alternative token
        # Input: an EKind context with the token alternative
        # Expected Result: EKind.ALTERNATIVE

        ("multiple", "multiple", EKind.MULTIPLE),
        # The multiple token
        # Input: an EKind context with the token multiple
        # Expected Result: EKind.MULTIPLE

        ("no_kind", None, None),
        # A context without kind is an internal error
        # Input: an EKind context without token
        # Expected Result: None
    ])
    def test_visitEKind(self, test_name, token, expected_kind):
        kind_ctx = DeclarationParser.EKindContext(parent=None, parser=None)
        if token is not None:
            setattr(kind_ctx, token, self.set_token(token))

        result = self.make_visitor().visitEKind(kind_ctx)

        self.assertEqual(expected_kind, result, test_name)


if __name__ == '__main__':
    unittest.main()
