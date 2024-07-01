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

    def __init__(self, mode:CompileFlags) -> None:
        self.mode = mode
        basicConfig()
        self.logger = getLogger("cpc")
        self.logger.setLevel(INFO)
        self.warning = 0
        self.error = 0

    def relax(self, context, message:str):
        if (self.mode == CompileFlags.RELAX):
            self.logger.warn(f"[{self.basename(context.start.source[1].fileName)}:{context.start.line}] {message}")
            self.warning = self.warning + 1
        elif (self.mode == CompileFlags.STRICT):
            self.logger.error(f"[{self.basename(context.start.source[1].fileName)}:{context.start.line}] {message}")
            self.error = self.error + 1

    def strict(self, context, message:str):
        self.logger.error(f"[{self.basename(context.start.source[1].fileName)}:{context.start.line}] {message}")

    def basename(self, fileName:str):
        return os.path.basename(fileName)




