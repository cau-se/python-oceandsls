#!/usr/bin/python

from common.unit_processing_test import TestUnitProcessionVisitor

from generator.visitors.configuration.visitor_arithmetic_test import TestArithmeticGeneratorConfigurationVisitor
from generator.visitors.configuration.visitor_base_test import TestBaseGeneratorConfigurationVisitor
from generator.visitors.configuration.visitor_feature_test import TestFeatureGeneratorConfigurationVisitor
from generator.visitors.configuration.visitor_parameter_test import TestParameterGeneratorConfigurationVisitor
from generator.visitors.configuration.visitor_units_test import TestUnitGeneratorConfigurationVisitor

from generator.visitors.declaration.visitor_arithmetic_test import TestArithmeticGeneratorDeclarationVisitor
from generator.visitors.declaration.visitor_base_test import TestBaseGeneratorDeclarationVisitor
from generator.visitors.declaration.visitor_feature_test import TestFeatureGeneratorDeclarationVisitor
from generator.visitors.declaration.visitor_parameter_test import TestParameterGeneratorDeclarationVisitor
from generator.visitors.declaration.visitor_units_test import TestUnitGeneratorDeclarationVisitor

from unittest import TestSuite, TestLoader, TextTestRunner

test_cases = (TestUnitProcessionVisitor,
              TestArithmeticGeneratorConfigurationVisitor,
              TestBaseGeneratorConfigurationVisitor,
              TestFeatureGeneratorConfigurationVisitor,
              TestParameterGeneratorConfigurationVisitor,
              TestUnitGeneratorConfigurationVisitor,
              TestArithmeticGeneratorDeclarationVisitor,
              TestBaseGeneratorDeclarationVisitor,
              TestFeatureGeneratorDeclarationVisitor,
              TestParameterGeneratorDeclarationVisitor,
              TestUnitGeneratorDeclarationVisitor)

def load_tests() -> TestSuite:
    suite = TestSuite()
    loader = TestLoader()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite

suite = load_tests()

runner = TextTestRunner(verbosity=2)
runner.run(suite)

# end