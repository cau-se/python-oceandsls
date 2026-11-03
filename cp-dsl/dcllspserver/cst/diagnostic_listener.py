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

"""Deprecated re-export of :mod:`odsllib.lsp.diagnostic_listener` (shared implementation in odsllib).

Import :mod:`odsllib.lsp.diagnostic_listener` instead; this module will be removed in a future version.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,unused-import
import warnings

from odsllib.lsp.diagnostic_listener import *  # noqa: F401,F403
from odsllib.lsp.diagnostic_listener import (  # noqa: F401
    DiagnosticListener,
)

warnings.warn(f"{__name__} is deprecated, import odsllib.lsp.diagnostic_listener instead",
              DeprecationWarning, stacklevel=2)
