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

from logging import INFO, basicConfig, getLogger
from .configuration import CompileFlags
import os


class GeneratorLogger:
    """Reports problems found while processing CP-DSL models.

    Besides logging, every report is kept in :attr:`messages` as ``(severity, context, message)`` with severity
    ``"warning"`` or ``"error"``, so tools such as the language servers can present them, e.g. as diagnostics.
    """

    def __init__(self, mode: CompileFlags) -> None:
        self.mode = mode
        basicConfig()
        self.logger = getLogger("cpc")
        self.logger.setLevel(INFO)
        self.warning_count = 0
        self.error_count = 0
        self.messages: list[tuple[str, object, str]] = []

    def relax(self, context, message: str):
        if (self.mode == CompileFlags.RELAX):
            self.logger.warning("[%s] %s", self.location(context), message)
            self.warning_count = self.warning_count + 1
            self.messages.append(("warning", context, message))
        elif (self.mode == CompileFlags.STRICT):
            self.logger.error("[%s] %s", self.location(context), message)
            self.error_count = self.error_count + 1
            self.messages.append(("error", context, message))

    def strict(self, context, message: str):
        self.logger.error("[%s] %s", self.location(context), message)
        self.error_count = self.error_count + 1
        self.messages.append(("error", context, message))

    def error(self, *args):
        """Report an error: ``error(message)`` or ``error(context, message)``."""
        context, message = (None, args[0]) if len(args) == 1 else args[:2]
        self.logger.error(f"[{self.location(context)}] {message}" if context is not None else message)
        self.error_count = self.error_count + 1
        self.messages.append(("error", context, message))

    def warning(self, *args):
        """Report a warning: ``warning(message)`` or ``warning(context, message)``."""
        context, message = (None, args[0]) if len(args) == 1 else args[:2]
        self.logger.warning(f"[{self.location(context)}] {message}" if context is not None else message)
        self.warning_count = self.warning_count + 1
        self.messages.append(("warning", context, message))

    def location(self, context) -> str:
        """Return 'file:line' of a parser rule context (in-memory streams have no file name)."""
        start = getattr(context, "start", None)
        if start is None:
            return "?"
        stream = start.source[1] if start.source else None
        file_name = getattr(stream, "fileName", None)
        return f"{self.basename(file_name) if file_name else '<input>'}:{start.line}"

    def basename(self, fileName: str):
        return os.path.basename(fileName)
