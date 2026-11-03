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

import sys

import pytest

from cpdsl.common.configuration import CompileFlags
from cpdsl.common.logger import GeneratorLogger
from cpdsl.generator import __main__ as generator_main
from cpdsl.model.declaration_model import DeclarationModel

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


def write_model(directory, configuration=CONFIGURATION):
    (directory / "eval.decl").write_text(DECLARATION, encoding="utf-8")
    path = directory / "test.oconf"
    path.write_text(configuration, encoding="utf-8")
    return path


def run_main(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["cp_dsl_generate", *args])
    generator_main.main()


def build_model(path, monkeypatch) -> DeclarationModel:
    """Run the steps of main() up to the integrity check and return the model."""
    monkeypatch.setattr(generator_main, "logger", GeneratorLogger(CompileFlags.RELAX), raising=False)
    model = generator_main.make_declaration_model(DeclarationModel(), str(path.parent / "eval.decl"))
    model = generator_main.make_configuration_model(model, str(path))
    generator_main.check_model_integrity(model)
    return model


def test_main_computes_the_defaults_and_runs_the_generator(tmp_path, monkeypatch):
    configuration = write_model(tmp_path)
    out = tmp_path / "out"

    run_main(monkeypatch, "-i", str(configuration), "-o", str(out))

    assert out.is_dir()
    assert generator_main.logger.error_count == 0


def test_main_writes_into_gen_next_to_the_configuration_by_default(tmp_path, monkeypatch):
    configuration = write_model(tmp_path)

    run_main(monkeypatch, "-i", str(configuration))

    assert (tmp_path / "gen").is_dir()


def test_main_rejects_a_missing_configuration(tmp_path, monkeypatch):
    with pytest.raises(SystemExit) as exit_info:
        run_main(monkeypatch, "-i", str(tmp_path / "missing.oconf"))
    assert exit_info.value.code == 1


def test_calculator_stores_the_computed_default_values(tmp_path, monkeypatch):
    model = build_model(write_model(tmp_path), monkeypatch)
    generator_main.ConfigurationCalculator(model, generator_main.logger).calculate()

    settings = model.features["general"].groups["settings"].parameters
    assert settings["steps"].value.value == 10
    assert settings["color"].value.name == "green"
    common = model.groups["common"].parameters
    assert common["size"].value.value == 3.0
    assert common["label"].value is None  # no default value
    assert common["scale"].value.name == "SMALL"
    assert common["verbose"].value.value is False


def test_integrity_check_handles_entries_of_activated_features(tmp_path, monkeypatch):
    configuration = write_model(tmp_path, CONFIGURATION + """
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
""")
    model = build_model(configuration, monkeypatch)

    assert generator_main.logger.error_count == 0
    settings = model.features["general"].groups["settings"].parameters
    assert len(settings["color"].entries) == 1 and settings["color"].entries[0].name == "blue"
    assert model.groups["common"].parameters["scale"].entries[0].name == "LARGE"
    assert model.groups["common"].parameters["verbose"].entries[0].value is True
    kinds = model.groups["common"].parameters["kinds"].entries[0]  # enumerals inferred from the element type
    assert [element.name for element in kinds.elements] == ["red", "blue", "green"]


def test_invalid_values_and_includes_are_reported(tmp_path, monkeypatch):
    configuration = write_model(tmp_path, """configuration test : eval

include other.settings

feature general {
    group settings {
        color : purple
    }
}

group common {
    size : unknown_name
}
""")
    build_model(configuration, monkeypatch)

    messages = [message for _, _, message in generator_main.logger.messages]
    assert any("Include of other.settings is not supported" in m for m in messages)
    assert any("Invalid value for parameter size" in m for m in messages)
    assert any("Symbol purple does not refer to an enumeral" in m for m in messages)
    assert any("Invalid value for parameter color" in m for m in messages)
