#  Copyright (c) 2023-2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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
"""Unit checks and conversions of configured values (with cfunits through odsllib.units)."""

from typing import Iterator, Optional

from odsllib.units import CompositeUnit, UnitError, unavailable_reason

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.units import to_composite_unit
from cpdsl.model.arithmetic_model import AbstractExpression, AbstractTypedValue, FloatValue, IntValue
from cpdsl.model.declaration_model import DeclarationModel, Feature, Parameter, SelectorExpression
from cpdsl.model.unit_model import Unit


def unit_of(expression: AbstractExpression) -> Optional[Unit]:
    """The unit of a value: the unit written with it or, for a reference, the unit of the referenced parameter.

    Units of composed expressions are not derived yet; their explicit unit applies to the whole expression.
    """
    if isinstance(expression, Parameter):
        return expression.unit
    return getattr(expression, "unit", None)


def parameters_with_entries(model: DeclarationModel) -> Iterator[Parameter]:
    """All parameters with configured values, of the model's groups and of its activated features."""
    def from_feature(feature: Feature):
        if feature.is_activated:
            for group in feature.groups.values():
                yield from group.parameters.values()
            for feature_set in feature.feature_sets:
                for child in feature_set.features.values():
                    yield from from_feature(child)

    for group in model.groups.values():
        yield from group.parameters.values()
    for feature in model.features.values():
        yield from from_feature(feature)


class UnitCalculator:
    """Checks that values are given in units compatible with the declared units and converts them."""

    def __init__(self, logger: GeneratorLogger):
        self.logger = logger
        self.unavailable_reported = False

    def composite(self, unit: Optional[Unit], context) -> Optional[CompositeUnit]:
        """The unit for checks, None if there is none or it cannot be represented (reported)."""
        try:
            return to_composite_unit(unit)
        except UnitError as error:
            self.logger.strict(context, f"Invalid unit: {error}")
            return None

    def check(self, target: Optional[Unit], source: Optional[Unit], parameter: Parameter, context=None) -> bool:
        """Whether a value in unit *source* may be assigned to *parameter* with unit *target*; reports problems.

        Values without unit are taken to be in the declared unit. If cfunits is not installed, only custom units
        are compared and the check is reported once as skipped.
        """
        context = context if context is not None else getattr(parameter, "ctx", None)
        target_unit, source_unit = self.composite(target, context), self.composite(source, context)
        if target_unit is None or source_unit is None:
            return True
        for unit in (target_unit, source_unit):
            if unit.is_valid() is False:
                self.logger.strict(context, f"Unit {unit} is not known to UDUNITS-2")
                return False
        equivalent = source_unit.equivalent(target_unit)
        if equivalent is None:
            if not self.unavailable_reported:
                self.logger.logger.info("%s", unavailable_reason())
                self.unavailable_reported = True
            return True
        if not equivalent:
            self.logger.strict(context, f"Unit {source_unit} of the value is not compatible with unit {target_unit} "
                                        f"of parameter {parameter.name}")
        return equivalent

    def check_parameter(self, parameter: Parameter) -> bool:
        """Check the units of the default value and of all configured values of a parameter."""
        values = [parameter.default_value] if parameter.default_value is not None else []
        values += [entry.expression if isinstance(entry, SelectorExpression) else entry for entry in parameter.entries]
        results = [self.check(parameter.unit, unit_of(value), parameter, getattr(value, "ctx", None))
                   for value in values]
        return all(results)

    def check_model(self, model: DeclarationModel) -> bool:
        """Check the units of all parameters with values, of groups and activated features."""
        results = [self.check_parameter(parameter) for parameter in parameters_with_entries(model)]
        return all(results)

    def convert(self, value: AbstractTypedValue, source: Optional[Unit], target: Optional[Unit],
                parameter: Parameter) -> AbstractTypedValue:
        """The numeric value converted from unit *source* to unit *target* (unchanged if no conversion is needed)."""
        if not isinstance(value, (IntValue, FloatValue)) or source is None or target is None:
            return value
        context = getattr(value, "ctx", None)
        source_unit, target_unit = self.composite(source, context), self.composite(target, context)
        if source_unit is None or target_unit is None or source_unit == target_unit:
            return value
        if source_unit.equivalent(target_unit) is False:
            return value  # incompatible units are reported by check()
        try:
            converted = source_unit.convert(value.value, target_unit)
        except UnitError as error:
            self.logger.strict(context, f"Value of parameter {parameter.name} not converted: {error}")
            return value
        return FloatValue(ctx=value.ctx, unit=target, type=value.type, value=converted)
