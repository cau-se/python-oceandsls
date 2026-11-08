#  Copyright (c) 2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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
"""End-to-end tests of the generator command line (cp_dsl_generate, python -m cpdsl.generator)."""

import pathlib
import tempfile
import unittest
from unittest.mock import patch

from parameterized import parameterized

from cpdsl.common.configuration import CompileFlags
from cpdsl.common.logger import GeneratorLogger
from cpdsl.generator import __main__ as generator_main
from cpdsl.model.declaration_model import DeclarationModel

from generator.visitors.test_utils import describe_expression

DECLARATION = """model eval

types
    enum Color { red, green, blue }

feature general : "general feature" {
    group settings : "settings" {
        def color Color : "color" = green
        def steps int : "number of steps" = 2 * 3 + 4
    }
}

group common : "common parameters" {
    def size float : "size" = 1.5 * 2
    def label string : "label"
    def verbose boolean : "verbose output" = false
    def kinds Color[3] : "array of enumerals"
    def scale ( SMALL, LARGE ) : "inline enumeration" = SMALL
}
"""

CONFIGURATION = """configuration test : eval

activate general
"""

ENTRIES = CONFIGURATION + """
feature general {
    group settings {
        color : blue
        steps : 7
    }
}
group common {
    scale : LARGE
    verbose : true
    kinds : [ red, blue, green ]
}
"""

INVALID = """configuration test : eval

include other.settings

feature general {
    group settings {
        color : purple
    }
}

group common {
    size : unknown_name
}
"""


class TestGeneratorCommandLine(unittest.TestCase):

    def setUp(self):
        directory = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(directory.cleanup)
        self.tmp_path = pathlib.Path(directory.name)
        # main() and build_model() replace the module logger; restore it after each test
        logger_patch = patch.object(generator_main, "logger", GeneratorLogger(CompileFlags.RELAX), create=True)
        logger_patch.start()
        self.addCleanup(logger_patch.stop)

    def write_model(self, configuration=CONFIGURATION):
        (self.tmp_path / "eval.decl").write_text(DECLARATION, encoding="utf-8")
        path = self.tmp_path / "test.oconf"
        path.write_text(configuration, encoding="utf-8")
        return path

    def run_main(self, *args):
        with patch("sys.argv", ["cp_dsl_generate", *args]):
            generator_main.main()

    def build_model(self, configuration=CONFIGURATION) -> DeclarationModel:
        """Run the steps of main() up to the integrity check and return the model."""
        path = self.write_model(configuration)
        model = generator_main.make_declaration_model(DeclarationModel(), str(path.parent / "eval.decl"))
        model = generator_main.make_configuration_model(model, str(path))
        generator_main.check_model_integrity(model)
        return model

    def parameter(self, model, location, name):
        """A parameter of a group ('common') or of a group of a feature ('general.settings')."""
        names = location.split(".")
        scope = model.features[names[0]].groups[names[1]] if len(names) == 2 else model.groups[names[0]]
        return scope.parameters[name]

    @parameterized.expand([
        ("explicit_output", "test.oconf", "out", None, "out"),
        # main() computes the defaults and runs the generator
        # Input: '-i test.oconf -o out'
        # Expected Result: the directory out, no errors

        ("default_output", "test.oconf", None, None, "gen"),
        # Without -o the output is written into gen next to the configuration
        # Input: '-i test.oconf'
        # Expected Result: the directory gen next to the configuration

        ("missing_configuration", "missing.oconf", None, 1, None),
        # A missing configuration is rejected
        # Input: '-i missing.oconf'
        # Expected Result: exit code 1
    ])
    def test_main(self, test_name, configuration, output, expected_exit_code, expected_directory):
        self.write_model()
        args = ["-i", str(self.tmp_path / configuration)] + (["-o", str(self.tmp_path / output)] if output else [])

        if expected_exit_code is None:
            self.run_main(*args)
            self.assertEqual(0, generator_main.logger.error_count, test_name)
        else:
            with self.assertRaises(SystemExit) as exit_info:
                self.run_main(*args)
            self.assertEqual(expected_exit_code, exit_info.exception.code, test_name)

        if expected_directory:
            self.assertTrue((self.tmp_path / expected_directory).is_dir(), test_name)

    @parameterized.expand([
        ("expression", "general.settings", "steps", ("int", 10)),
        # The calculator stores the computed default values
        # Input: 'def steps int : "number of steps" = 2 * 3 + 4'
        # Expected Result: the value 10

        ("enumeral", "general.settings", "color", ("enum", "green", 1)),
        # An enumeral default value
        # Input: 'def color Color : "color" = green'
        # Expected Result: the enumeral green

        ("float_expression", "common", "size", ("float", 3.0)),
        # A float expression
        # Input: 'def size float : "size" = 1.5 * 2'
        # Expected Result: the value 3.0

        ("no_default_value", "common", "label", None),
        # A parameter without default value
        # Input: 'def label string : "label"'
        # Expected Result: no value

        ("inline_enumeral", "common", "scale", ("enum", "SMALL", 0)),
        # An inline enumeration default value
        # Input: 'def scale ( SMALL, LARGE ) : "inline enumeration" = SMALL'
        # Expected Result: the enumeral SMALL

        ("boolean", "common", "verbose", ("bool", False)),
        # A boolean default value
        # Input: 'def verbose boolean : "verbose output" = false'
        # Expected Result: the value False
    ])
    def test_calculator_stores_the_computed_default_values(self, test_name, location, name, expected):
        model = self.build_model()
        generator_main.ConfigurationCalculator(model, generator_main.logger).calculate()

        self.assertEqual(expected, describe_expression(self.parameter(model, location, name).value), test_name)

    @parameterized.expand([
        ("enumeral", "general.settings", "color", [("enum", "blue", 2)]),
        # Entries of activated features are checked
        # Input: 'color : blue' in the group settings of the activated feature general
        # Expected Result: one entry, the enumeral blue

        ("int", "general.settings", "steps", [("int", 7)]),
        # A value entry of an activated feature
        # Input: 'steps : 7'
        # Expected Result: the entry 7

        ("inline_enumeral", "common", "scale", [("enum", "LARGE", 1)]),
        # An enumeral of an inline enumeration
        # Input: 'scale : LARGE'
        # Expected Result: the enumeral LARGE

        ("boolean", "common", "verbose", [("bool", True)]),
        # A boolean entry
        # Input: 'verbose : true'
        # Expected Result: the entry True

        ("enumeral_array", "common", "kinds", [("array", [("enum", "red", 0), ("enum", "blue", 2),
                                                          ("enum", "green", 1)])]),
        # The enumerals of an array are inferred from the element type
        # Input: 'kinds : [ red, blue, green ]'
        # Expected Result: an array of the enumerals red, blue and green
    ])
    def test_integrity_check_handles_entries_of_activated_features(self, test_name, location, name, expected):
        model = self.build_model(ENTRIES)

        self.assertEqual(0, generator_main.logger.error_count, test_name)
        entries = self.parameter(model, location, name).entries
        self.assertEqual(expected, [describe_expression(entry) for entry in entries], test_name)

    @parameterized.expand([
        ("include", "Include of other.settings is not supported"),
        # Includes are not supported
        # Input: 'include other.settings'
        # Expected Result: an error about the include

        ("unknown_name", "Invalid value for parameter size"),
        # A value that refers to nothing
        # Input: 'size : unknown_name'
        # Expected Result: an error about the value of size

        ("unknown_enumeral", "Symbol purple does not refer to an enumeral"),
        # A symbol that is no enumeral of the parameter type
        # Input: 'color : purple'
        # Expected Result: an error about purple

        ("invalid_enumeral_value", "Invalid value for parameter color"),
        # The value of the enumeration parameter is invalid as well
        # Input: 'color : purple'
        # Expected Result: an error about the value of color
    ])
    def test_invalid_values_and_includes_are_reported(self, test_name, expected_message):
        self.build_model(INVALID)

        messages = [message for _, _, message in generator_main.logger.messages]
        self.assertTrue(any(expected_message in message for message in messages), f"{test_name}: {messages}")


if __name__ == '__main__':
    unittest.main()
