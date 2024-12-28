from model.unit_model import UnitSpecification, Unit, UnitKind, UnitPrefix, SIUnit, ExponentUnit, DivisionUnit, CustomUnit
from typing import List

prefix = { 'q': UnitPrefix.Quecto,
            'r': UnitPrefix.Ronto,
            'y': UnitPrefix.Yocto,
            'z': UnitPrefix.Zepto,
            'a': UnitPrefix.Atto,
            'f': UnitPrefix.Femto,
            'p': UnitPrefix.Pico,
            'n': UnitPrefix.Nano,
            'ü': UnitPrefix.Micro,
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

kind = { 's': UnitKind.Second,
        'm': UnitKind.Meter,
        'g': UnitKind.Gram,
        'A': UnitKind.Ampere,
        'cd': UnitKind.Candela,
        'J': UnitKind.Joule,
        'K': UnitKind.Kelvin,
        'mol': UnitKind.Mole,
        'Pa': UnitKind.Pascal
        }

def parse_unit(unit : str, user_defined_units:list = []) -> UnitSpecification:
    for u in user_defined_units:
        if unit == u:
            return UnitSpecification([CustomUnit(unit)])

    token_list = tokenize(unit)
    token_list = resolve(token_list)
    token_list = process_tokens(token_list)
    return process_divisions(token_list)

def make_operand(collection:list):
    if len(collection) == 1:
        return collection[0]
    else:
        return UnitSpecification(collection)

def process_divisions(token_list):
    collection = []
    mode = 0
    numerator = None
    for token in token_list:
        if token == '/' and mode == 0:
            numerator = make_operand(collection)
            collection = []
            mode = 1
        elif token == '/' and mode == 1:
            d2 = make_operand(collection)
            collection = []
            numerator = DivisionUnit(numerator,d2)
        else:
            collection.append(token)

    if numerator is not None:
        denominator = make_operand(collection)
        return UnitSpecification([DivisionUnit(numerator,denominator)])
    else:
        return UnitSpecification(collection)


def process_level(level: list):
    units = []
    prefix = None
    for item in level:
        if isinstance(item, UnitPrefix):
            prefix = item
        elif isinstance(item, UnitKind):
            units.append(SIUnit(prefix, item))
            prefix = None
        elif isinstance(item, int):
            last = units.pop()
            units.append(ExponentUnit(last, item))

    return UnitSpecification(units)

def process_tokens(token_list: list):
    level = []
    stack = []
    for token in token_list:
        if token == '(':
            stack.append(level)
            level = []
        elif token == ')':
            unit = process_level(level)
            level = stack.pop()
            level.append(unit)
        elif isinstance(token, UnitKind):
            if len(level) > 0:
                previous = level.pop()
                if isinstance(previous, UnitPrefix):
                    level.append(SIUnit(previous, token))
                elif isinstance(previous, Unit):
                    level.append(previous)
                    level.append(token)
                else:
                    level.append(SIUnit(None, previous))
                    level.append(token)
            else:
                level.append(SIUnit(None, token))
        elif isinstance(token, int):
            previous = level.pop()
            level.append(ExponentUnit(previous, token))
        else:
            level.append(token)

    return level

def resolve(token_list: list):
    i = 0
    while i < len(token_list):
        token = token_list[i]
        if isinstance(token, list):
            if i+1 < len(token_list):
                next = token_list[i+1]
                if isinstance(next,UnitPrefix):
                    token_list[i] = token[1]
                elif next == '*':
                    token_list[i] = token[1]
                elif isinstance(next, list):
                    token_list[i] = token[0]
                elif isinstance(next, int):
                    token_list[i] = token[1]
                else:
                    token_list[i] = token[0]
        i+=1
    return token_list

def tokenize(unit: str):
    length = len(unit)
    i = 0
    tokens = []
    while i < length:
        c = unit[i]
        if c in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'm', 'c', 'd', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            if c == 'd':
                token = UnitPrefix.Deci
                if i+1 < length:
                    if unit[i+1] == 'a':
                        i+=1
                        token = UnitPrefix.Deca
            elif c == 'm':
                token = [ UnitPrefix.Milli, UnitKind.Meter ]
                if i+1 == length:
                    token = UnitKind.Meter
                if i+2 < length:
                    if unit[i+1] == 'o' and unit[i+2] == 'l':
                        token = UnitKind.Mole
                        i+=2
            elif c == 'c':
                token = UnitPrefix.Centi
                if i+1 < length:
                    if unit[i+1] == 'd':
                        token = UnitKind.Candela
                        i+=1
            elif c == 'P':
                token = UnitPrefix.Peta
                if i+1 < length:
                    if unit[i+1] == 'a':
                        i+=1
                        token = UnitKind.Pascal
            else:
                token = prefix[c]
        elif c == 's':
            token = UnitKind.Second
        elif c == 'g':
            token = UnitKind.Gram
        elif c == 'A':
            token = UnitKind.Ampere
        elif c == 'J':
            token = UnitKind.Joule
        elif c == 'K':
            token = UnitKind.Kelvin
        elif c == '^':
            if unit[i+1] == '-':
                i+=2
                o = i
                while i < length and unit[i].isdigit():
                    i+=1
                token = int(unit[o-1:i])
            elif unit[i+1] == '+':
                i+=2
                o = i
                while i < length and unit[i].isdigit():
                    i+=1
                token = int(unit[o:i])
            else:
                i+=1
                o = i
                while i < length and unit[i].isdigit():
                    i+=1
                token = int(unit[o:i])
        elif c in [ '(', ')', '/']:
            token = c
        else:
            print(f"Unit symbol {c} in {unit} not supported")
            token = c
        tokens.append(token)
        i+=1
    return tokens
