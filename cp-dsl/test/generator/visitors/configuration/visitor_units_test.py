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

from model.declaration_model import DeclarationModel

from test_utils import AbstractTestGeneratorConfigurationVisitor

class TestGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    def test_visit_unitSpecification(self):
        model = self.parse_declaration_code("""
                model eval
                    group my_group : "description" {
                        def param int : meter / kilo gram
                    }
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        model = self.parse_code("""
                configuration test : eval

                group my_group {
                    param: 4 m/kg
                }

                """)

if __name__ == '__main__':
    unittest.main()
