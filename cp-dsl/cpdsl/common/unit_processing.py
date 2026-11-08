"""Parse unit strings of configurations, e.g. 'kg/mm^2', 'mmol m^-3' or 'km/h', into the unit model.

Grammar (whitespace and '*' separate factors, the denominator of '/' extends to the next '/'):

    unit    := product ('/' product)*
    product := factor (['*'] factor)*
    factor  := atom ('^' ['+' | '-'] digits)?
    atom    := '(' unit ')' | symbols

A run of letters (symbols) is split into SI units with backtracking, so that the symbol 'm' is read as milli when
a unit kind follows it (mm, ms, mmol) and as meter otherwise (m, m/kg, km). Multi-letter unit symbols (mol, cd, Pa)
take precedence over a prefix followed by a unit (cd is candela, not centi day).
"""
from typing import List, Optional, Tuple, Union

from cpdsl.model.unit_model import UnitSpecification, Unit, UnitKind, UnitPrefix, SIUnit, ExponentUnit, DivisionUnit, \
    CustomUnit

import logging
_log = logging.getLogger(__name__)  # diagnostics go to logging, never to stdout

PREFIXES = {'q': UnitPrefix.Quecto,
            'r': UnitPrefix.Ronto,
            'y': UnitPrefix.Yocto,
            'z': UnitPrefix.Zepto,
            'a': UnitPrefix.Atto,
            'f': UnitPrefix.Femto,
            'p': UnitPrefix.Pico,
            'n': UnitPrefix.Nano,
            'ü': UnitPrefix.Micro,
            'µ': UnitPrefix.Micro,
            'μ': UnitPrefix.Micro,
            'm': UnitPrefix.Milli,
            'c': UnitPrefix.Centi,
            'd': UnitPrefix.Deci,
            'da': UnitPrefix.Deca,
            'h': UnitPrefix.Hecto,
            'k': UnitPrefix.Kilo,
            'M': UnitPrefix.Mega,
            'G': UnitPrefix.Giga,
            'T': UnitPrefix.Tera,
            'P': UnitPrefix.Peta,
            'E': UnitPrefix.Exa,
            'Z': UnitPrefix.Zetta,
            'Y': UnitPrefix.Yotta,
            'R': UnitPrefix.Ronna,
            'Q': UnitPrefix.Quetta
            }

KINDS = {'s': UnitKind.Second,
         'm': UnitKind.Meter,
         'g': UnitKind.Gram,
         'A': UnitKind.Ampere,
         'cd': UnitKind.Candela,
         'J': UnitKind.Joule,
         'K': UnitKind.Kelvin,
         'mol': UnitKind.Mole,
         'Pa': UnitKind.Pascal,
         'h': UnitKind.Hour,
         'd': UnitKind.Day
         }

# Longest symbols first, so that 'da' is tried before 'd' and 'mol' before 'm'
_PREFIX_SYMBOLS = sorted(PREFIXES, key=len, reverse=True)
_KIND_SYMBOLS = sorted(KINDS, key=len, reverse=True)
_OPERATORS = "()/*·."

Token = Tuple[str, Union[str, int]]  # ('symbol', text), ('exponent', value) or ('operator', character)


def parse_unit(unit: str, user_defined_units: tuple = ()) -> UnitSpecification:
    """
    Parse a unit string.

    :param unit: the unit, e.g. 'kg/mm^2'
    :param user_defined_units: names of custom units that may be used instead of SI units
    :return: a unit specification of the units; a division is one DivisionUnit in it
    """
    if unit in user_defined_units:
        return UnitSpecification([CustomUnit(unit)])
    result = _UnitParser(unit, tuple(user_defined_units)).parse()
    if isinstance(result, DivisionUnit):
        return UnitSpecification([result])
    return UnitSpecification(result)


def tokenize(unit: str) -> List[Token]:
    """
    Split a unit string into runs of unit symbols, exponents and operators.

    :param unit: the unit string
    :return: tokens ('symbol', text), ('exponent', value) and ('operator', character)
    """
    tokens: List[Token] = []
    i = 0
    while i < len(unit):
        c = unit[i]
        if c.isspace():
            i += 1
        elif c.isalpha():
            start = i
            while i < len(unit) and unit[i].isalpha():
                i += 1
            tokens.append(("symbol", unit[start:i]))
        elif c == '^':
            start = i + 1
            i = start + 1 if start < len(unit) and unit[start] in "+-" else start
            digits = i
            while i < len(unit) and unit[i].isdigit():
                i += 1
            if i == digits:
                _log.error("Missing exponent after ^ in %s", unit)
                continue
            tokens.append(("exponent", int(unit[start:i])))
        elif c in _OPERATORS:
            tokens.append(("operator", c))
            i += 1
        else:
            _log.error("Unit symbol %s in %s not supported", c, unit)
            i += 1
    return tokens


def split_symbols(symbols: str) -> Optional[List[SIUnit]]:
    """
    Split a run of unit symbols into SI units, e.g. 'kgmm' into kg and mm.

    :param symbols: letters of one or more units without separators
    :return: the units, None if the letters are no sequence of (prefixed) unit symbols
    """
    if not symbols:
        return []
    for unit, length in _symbol_candidates(symbols):
        rest = split_symbols(symbols[length:])
        if rest is not None:
            return [unit] + rest
    return None


def _symbol_candidates(symbols: str):
    """Readings of the start of the symbols in the order of preference."""
    for kind in _KIND_SYMBOLS:
        if len(kind) > 1 and symbols.startswith(kind):
            yield SIUnit(None, KINDS[kind]), len(kind)
    for prefix in _PREFIX_SYMBOLS:
        if symbols.startswith(prefix):
            for kind in _KIND_SYMBOLS:
                if symbols.startswith(kind, len(prefix)):
                    yield SIUnit(PREFIXES[prefix], KINDS[kind]), len(prefix) + len(kind)
    for kind in _KIND_SYMBOLS:
        if len(kind) == 1 and symbols.startswith(kind):
            yield SIUnit(None, KINDS[kind]), 1


def _operand(units: Union[List[Unit], DivisionUnit]) -> Unit:
    """A single unit for a product of units or a division."""
    if isinstance(units, DivisionUnit):
        return units
    if len(units) == 1:
        return units[0]
    return UnitSpecification(units)


class _UnitParser:
    """Recursive descent parser of the grammar in the module documentation."""

    def __init__(self, unit: str, user_defined_units: tuple):
        self.unit = unit
        self.user_defined_units = user_defined_units
        self.tokens = tokenize(unit)
        self.position = 0

    def peek(self) -> Optional[Token]:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def is_operator(self, character: str) -> bool:
        return self.peek() == ("operator", character)

    def parse(self) -> Union[List[Unit], DivisionUnit]:
        result = self.parse_division()
        if self.peek() is not None:
            _log.error("Unexpected %s in unit %s", self.peek()[1], self.unit)
        return result

    def parse_division(self) -> Union[List[Unit], DivisionUnit]:
        result: Union[List[Unit], DivisionUnit] = self.parse_product()
        while self.is_operator('/'):
            self.position += 1
            result = DivisionUnit(_operand(result), _operand(self.parse_product()))
        return result

    def parse_product(self) -> List[Unit]:
        units: List[Unit] = []
        while True:
            token = self.peek()
            if token is not None and token[0] == "operator" and token[1] in "*·.":
                self.position += 1
            elif token is not None and (token[0] == "symbol" or token == ("operator", "(")):
                units.extend(self.parse_factor())
            else:
                return units

    def parse_factor(self) -> List[Unit]:
        token = self.peek()
        self.position += 1
        if token == ("operator", "("):
            units = [_operand(self.parse_division())]
            if self.is_operator(')'):
                self.position += 1
            else:
                _log.error("Missing ) in unit %s", self.unit)
        else:
            units = self.symbol_units(token[1])
        if self.peek() is not None and self.peek()[0] == "exponent":
            units[-1] = ExponentUnit(units[-1], self.peek()[1])
            self.position += 1
        return units

    def symbol_units(self, symbols: str) -> List[Unit]:
        if symbols in self.user_defined_units:
            return [CustomUnit(symbols)]
        units = split_symbols(symbols)
        if units is None:
            _log.error("Unit symbol %s in %s not supported", symbols, self.unit)
            return [CustomUnit(symbols)]
        return units
