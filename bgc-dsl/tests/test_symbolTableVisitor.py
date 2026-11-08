''' Tests if a certain Symbol was inserted into the SymbolTable '''

__author__ = "stu90642"

#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
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

import os
import unittest

from antlr4 import CommonTokenStream, FileStream
from parameterized import parameterized

from bgclspserver.gen.python.BgcDsl.BgcDslLexer import BgcDslLexer
from bgclspserver.gen.python.BgcDsl.BgcDslParser import BgcDslParser
from bgclspserver.cst.symbol_table_visitor import SymbolTableVisitor

EXAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "input", "example1.bgc")


def prepare():
    """The symbol table of input/example1.bgc built by the SymbolTableVisitor."""
    input_stream = FileStream(EXAMPLE, encoding='utf-8')
    lexer = BgcDslLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BgcDslParser(stream)

    tree = parser.bgcModel()
    return SymbolTableVisitor('SymbolTableVisitor_1').visit(tree)


def texts(contexts):
    return [context.getText() for context in contexts]


class TestSTVisitor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.symbol_table = prepare()

    def resolve(self, name):
        symbol = self.symbol_table.resolve_sync(name)
        self.assertIsNotNone(symbol, name)
        return symbol

    @parameterized.expand([
        ("substance", "N", "mmol", "float"),
        # A substance with a simple unit
        # Input: the substance N
        # Expected Result: unit 'mmol', type float

        ("substance_with_compound_unit", "DIN", "mmolNm^-3", "float"),
        # A substance with a compound unit
        # Input: the substance DIN
        # Expected Result: unit 'mmol N m^-3', type float

        ("parameter", "Q_r_C_N", "mmolC(mmolN)^-1", "float"),
        # A model parameter with a parenthesized unit
        # Input: the parameter Q_r_C_N
        # Expected Result: unit 'mmol C (mmol N)^-1', type float

        ("parameter_with_si_unit", "T_K", "K", "float"),
        # A parameter with an SI unit
        # Input: the parameter T_K
        # Expected Result: unit 'K', type float

        ("parameter_without_unit", "criteria", "", "string"),
        # A string parameter without unit
        # Input: the parameter criteria
        # Expected Result: no unit, type string

        ("parameter_with_time_unit", "alpha", "mmolC(mgChl)^-1m^2W^-1#d^-1", "float"),
        # A unit with several factors and a time unit
        # Input: the parameter alpha
        # Expected Result: unit 'mmol C (mg Chl)^-1 m^2 W^-1 #d^-1', type float
    ])
    def test_declaration(self, test_name, name, expected_unit, expected_type):
        symbol = self.resolve(name)
        unit = ''.join(texts(symbol.value.unit().elements))
        self.assertEqual(expected_unit, unit, test_name)
        self.assertEqual(expected_type, symbol.value.type_.getText(), test_name)

    @parameterized.expand([
        ("nif", "Nif", (4, "Chl=0"), (2, "Q_u2_N_C"), (2, "theta_C"), (14, "calcPsi=max(0,Psi_max*(1-q_N_C/Q_2_N_C))"),
         (4, "updateC=phot_DIC*C-(respiration+gamma+aggregation)*C")),
        # A compartment with states, parameters, environment variables, calculations and updates
        # Input: the compartment Nif
        # Expected Result: 4 states, 2 parameters, 2 environment variables, 14 calculations and 4 updates

        ("det", "Det", (3, "C=0"), (0, None), (0, None), (6, None),
         (3, "updateC=Phy:aggregation*Phy.C+aggregation*Nif.C+MG.Phi*N*MG.C+(1-A_E)*(Phy:grazing*q_C_N+"
             "Phy:grazing*q_C_N)+Omega*Het:mortality*Het.C-degradation.C-sedimentation_C")),
        # A compartment without parameters and environment variables
        # Input: the compartment Det
        # Expected Result: 3 states, 6 calculations and 3 updates

        ("dccho", "dCCHO", (1, "C=0"), (1, "Phi_TEPC"), (0, None), (0, None),
         (1, "updateC=Phy.Psi*Phy.gamma_C*Phy.C+Nif.Psi*Nif.gamma_C*Nif.C-coagulation*C")),
        # A compartment with a single state and parameter
        # Input: the compartment dCCHO
        # Expected Result: 1 state, 1 parameter and 1 update

        ("mg", "MG", (2, "C=0"), (2, "rho"), (0, None), (0, None), (2, "updateC=coagulation*dCCHO.C-aggregation*C")),
        # A compartment without calculations
        # Input: the compartment MG
        # Expected Result: 2 states, 2 parameters and 2 updates
    ])
    def test_compartment(self, test_name, name, states, parameters, environments, calculations, updates):
        compartment = self.resolve(name).value
        # parameters are called constants and environment variables evnironments in the grammar
        actual = {
            "states": texts(compartment.states),
            "parameters": [p.name.text for p in compartment.constants],
            "environments": [e.name.text for e in compartment.evnironments],
            "calculations": texts(compartment.calculations),
            "updates": texts(compartment.updateStates),
        }
        expected = {"states": states, "parameters": parameters, "environments": environments,
                    "calculations": calculations, "updates": updates}
        for part, (count, first) in expected.items():
            self.assertEqual(count, len(actual[part]), f"{test_name}: {part}")
            if first is not None:
                self.assertEqual(first, actual[part][0], f"{test_name}: {part}")
        for parameter in compartment.constants:
            self.assertEqual("float", parameter.type_.getText(), f"{test_name}: {parameter.name.text}")

    @parameterized.expand([
        ("expression", "aggregation from Phy to Det", "Phy.Phi*Phy.N+Det.Phi*Det.N", [], None),
        # A connection with one expression for all substances
        # Input: the connection aggregation from Phy to Det
        # Expected Result: the expression, no substance expressions

        ("substance_expressions", "assimilation from Nutrients to Nif", None, ["N", "C"], "N=Nif.assim_DIP*Nif.N"),
        # A connection with an expression per substance
        # Input: the connection assimilation from Nutrients to Nif
        # Expected Result: the substances N and C with their expressions

        ("three_substances", "degradation from Det to LDOM", None, ["C", "N", "P"], "C=Det.omega_C*Det.C"),
        # A connection of three substances
        # Input: the connection degradation from Det to LDOM
        # Expected Result: the substances C, N and P

        ("same_name_other_compartments", "aggregation from MG to Det", "(MG.rho*T_f+MG.Phi*Det.N)", [], None),
        # Connections are identified by name, source and target
        # Input: the connection aggregation from MG to Det
        # Expected Result: its own expression, not the one of aggregation from Phy to Det
    ])
    def test_connection(self, test_name, name, expected_expression, expected_substances,
                        expected_first_substance_expression):
        connection = self.resolve(name).value
        expression = connection.expression.getText() if connection.expression else None
        self.assertEqual(expected_expression, expression, test_name)
        self.assertEqual(expected_substances, [s.text for s in connection.substances], test_name)
        substance_expressions = texts(connection.substanceExpressions)
        self.assertEqual(expected_first_substance_expression,
                         substance_expressions[0] if substance_expressions else None, test_name)

    @parameterized.expand([
        ("unknown_name", "nothing"),
        # A name that is not declared
        # Input: 'nothing'
        # Expected Result: no symbol

        ("reversed_connection", "aggregation from Det to Phy"),
        # The direction is part of the connection
        # Input: 'aggregation from Det to Phy'
        # Expected Result: no symbol

        ("connection_name_only", "aggregation"),
        # A connection is not found by its name alone
        # Input: 'aggregation'
        # Expected Result: no symbol
    ])
    def test_unknown_symbol(self, test_name, name):
        self.assertIsNone(self.symbol_table.resolve_sync(name), test_name)


if __name__ == '__main__':
    unittest.main()
