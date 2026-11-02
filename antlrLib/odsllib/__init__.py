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
"""odsllib: shared functionality of the OceanDSL languages.

* :mod:`odsllib.code_completion_core` -- Python port of antlr4-c3 (grammar based completion candidates)
* :mod:`odsllib.lsp` -- language server infrastructure (parsing, diagnostics, completion, base server)
"""

from importlib.metadata import PackageNotFoundError, version as _version

try:
    __version__ = _version("odsllib")
except PackageNotFoundError:  # pragma: no cover - running from a source checkout
    __version__ = "0.0.0"

from .code_completion_core import CandidatesCollection, CodeCompletionCore

__all__ = ["CandidatesCollection", "CodeCompletionCore", "__version__"]
