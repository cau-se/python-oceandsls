"""Logging factory"""

__author__ = "sgu"


#  Copyright (c) 2024.  OceanDSL (https://oceandsl.uni-kiel.de)
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

# Example usage
#
# from utils.logger_factory import LoggerFactory
# logger = LoggerFactory.build_logger(
#     name=__name__,
#     file_level=DEBUG,                   # optional
#     console_level=INFO,                 # optional
#     log_dir="custom_logs",              # optional
#     log_file="custom_log_{time}.log"    # optional
# )
# logger.log_imports()  # optional log imports at top of file
# import some_module
# ... Module code ...
# logger.info("Application started successfully.")

# public interface
from os import getcwd, environ, path, makedirs
from sys import stdout, executable, version, path as sys_path, meta_path
from importlib.machinery import PathFinder
from logging import DEBUG, FileHandler, Formatter, INFO, StreamHandler, Logger
from datetime import datetime

class ImportLogger(PathFinder):
    """Logger for tracking module imports."""
    
    def __init__(self, logger):
        self.logger = logger

    def find_spec(self, fullname, path=None, target=None):
        """
        Find the specification for a module.

        This method is called to find the module specification for the given
        module name. It logs the import attempt.

        Args:
            fullname (str): The name of the module to find.
            path (list, optional): The search path for the module.
            target (object, optional): The target for the import.

        Returns:
            ModuleSpec: The module specification.

        Source: https://docs.python.org/3/library/importlib.html#importlib.machinery.PathFinder.find_spec
        """
        self.logger.info(f"Importing: {fullname} | Path: {path} | Target: {target}")
        return super().find_spec(fullname, path, target)

class LoggerWithImports(Logger):
    """
    Logger that logs import paths and environment variables.
    
    Source: https://docs.python.org/3/library/logging.html#logging.Logger
    """
    
    def log_imports(self):
        """
        Log environment variables and module search paths.
        """
        info = [
            f"Current Directory: {getcwd()}",
            f"Python Executable: {executable}",
            f"Python Version: {version}",
            f"PYTHONPATH: {environ.get('PYTHONPATH', 'Not Set')}",
            f"PATH: {environ.get('PATH', 'Not Set')}",
            "Module Search Paths:\n" + "\n".join(f" - {p}" for p in sys_path)
        ]
        self.info("\n".join(info))
        # Hook logger into import mechanism
        meta_path.insert(0, ImportLogger(self))

class LoggerFactory:
    """Factory for creating loggers with specific configurations."""
    
    log_dir = "logs"
    log_file = "app_{time}.log"
    log_format = Formatter(fmt="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S")

    @classmethod
    def buildLogger(cls, name: str, file_level: int = DEBUG, console_level: int = INFO):
        """
        Create a logger with file and console handlers.

        Args:
            name (str): The name of the logger.
            file_level (int): The logging level for the file handler.
            console_level (int): The logging level for the console handler.

        Returns:
            Logger: The configured logger instance.

        Source: https://docs.python.org/3/library/logging.html#logging.Logger
        """
        if not path.exists(cls.log_dir):
            makedirs(cls.log_dir)

        timestamp = datetime.now().strftime('%d-%m-%y_%H%M')
        log_path = path.join(cls.log_dir, cls.log_file.format(time=timestamp))

        logger = LoggerWithImports(name)
        logger.setLevel(min(file_level, console_level))

        file_handler = FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(cls.log_format)
        logger.addHandler(file_handler)

        console_handler = StreamHandler(stdout)
        console_handler.setLevel(console_level)
        console_handler.setFormatter(cls.log_format)
        logger.addHandler(console_handler)

        return logger
