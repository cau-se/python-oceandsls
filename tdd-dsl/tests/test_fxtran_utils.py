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
"""Tests of the fxtran utils (tddlspserver.fxca.util.fxtran_utils)."""

import os
import subprocess
import tempfile
import unittest
from os import path
from unittest.mock import patch, MagicMock

from parameterized import parameterized

from tddlspserver.fxca.util.fxtran_utils import (
    filter_xml,
    get_files,
    get_subdirectories,
    write_decorate_src_xml,
    logger
)


class TestFxtranUtils(unittest.TestCase):
    # Define constants for the test cases
    TEST_XML_PATH = "test.xml"
    TEST_DIR = "test_dir"
    TEST_PATTERN = "*.[fF]90"
    TEST_OUTPUT_DIR = "out"
    FXTRAN_PATH = "~/bin/fxtran"
    TEST_FILES = [("test_dir", "test1.f90"), ("test_dir", "test2.f90")]
    TEST_SUBDIRS = ["subdir1", "subdir2"]
    TEST_XML_CONTENT = "<root></root>"  # Minimal XML content for testing

    MODULE_MOCK = MagicMock(spec='ModuleSymbol')
    MODULE_MOCK.name = 'moduleMock'  # Set the name attribute

    @parameterized.expand([
        ("filter_xml_test_empty", TEST_XML_PATH, False, [], {}, ([], [])),
        # Test case for filtering XML with no modules and an empty XML file
        # Input: An empty XML structure
        # Expected Result: The function should return empty lists for variables and scopes.

        ("filter_xml_test_with_modules", TEST_XML_PATH, True, [MODULE_MOCK], {}, ([], [])),
        # Test case for filtering XML with modules
        # Input: A valid XML path and a list of modules
        # Expected Result: The function should process the XML and return the expected results.

        ("filter_xml_test_with_public_elements", TEST_XML_PATH, True, [MODULE_MOCK], {}, ([], [])),
        # Test case for filtering XML with public elements
        # Input: A valid XML path and a list of modules with public elements
        # Expected Result: The function should process the XML and return the expected results.
    ])
    @patch("tddlspserver.fxca.util.fxtran_utils.ET.parse")
    @patch("tddlspserver.fxca.util.fxtran_utils.PublicObj")
    def test_filter_xml(self, test_name, xml_path, need_public, modules, files, expected_result, mock_public_obj,
                        mock_et_parse):
        # Set up the mocks
        mock_tree = mock_et_parse.return_value
        mock_tree.getroot.return_value.iter.return_value = []  # Mocking an empty XML structure

        result = filter_xml(xml_path, need_public, modules, files)

        # Assertions
        self.assertEqual(expected_result, result, test_name)
        mock_et_parse.assert_called_once_with(xml_path)
        mock_public_obj.assert_called_once_with(need_public=need_public)

    @parameterized.expand([
        ("get_files_test", TEST_DIR, TEST_PATTERN, TEST_FILES),
        # Test case for retrieving files matching a pattern
        # Input: A directory and a file pattern that matches existing files
        # Expected Result: The function should return a list of matching files.

        ("get_files_test_no_matches", TEST_DIR, TEST_PATTERN, []),
        # Test case for retrieving files with no matches
        # Input: A directory and a file pattern that matches no files
        # Expected Result: The function should return an empty list.

        ("get_files_test_with_subdirectories", TEST_DIR, TEST_PATTERN, [("subdir", "test3.f90")]),
        # Test case for retrieving files in subdirectories
        # Input: A directory with files in subdirectories
        # Expected Result: The function should return a list of matching files from subdirectories.
    ])
    @patch("tddlspserver.fxca.util.fxtran_utils.os.walk")
    def test_get_files(self, test_name, test_path, pattern, expected_files, mock_os_walk):
        # Set up the mock
        if expected_files:
            # Create a structure for os.walk based on expected_files
            mock_walk_output = []
            seen_dirs = set()

            for dir_name, file_name in expected_files:
                if dir_name not in seen_dirs:
                    # Add the directory to the mock output
                    mock_walk_output.append((test_path, [dir_name], []))
                    seen_dirs.add(dir_name)
                # Add the file to the corresponding directory
                mock_walk_output.append((dir_name, [], [file_name]))

            mock_os_walk.return_value = mock_walk_output
        else:
            mock_os_walk.return_value = [(test_path, [], [])]  # No files

        result = get_files(test_path, pattern)

        # Assertions
        self.assertEqual(expected_files, result, test_name)

    @parameterized.expand([
        ("fortran_files", ["a.f90", "B.F90", "c.F90"], "*.[fF]90", ["a.f90", "B.F90", "c.F90"]),
        # The default pattern matches both cases of the extension
        # Input: a.f90, B.F90 and c.F90, pattern '*.[fF]90'
        # Expected Result: all three files

        ("other_files_filtered", ["a.f90", "notes.txt", "b.f"], "*.[fF]90", ["a.f90"]),
        # Files with other extensions are skipped
        # Input: a.f90, notes.txt and b.f
        # Expected Result: a.f90

        ("custom_pattern", ["a.f90", "suite.tdd"], "*.tdd", ["suite.tdd"]),
        # Other patterns are supported
        # Input: a.f90 and suite.tdd, pattern '*.tdd'
        # Expected Result: suite.tdd
    ])
    @patch("tddlspserver.fxca.util.fxtran_utils.os.walk")
    def test_get_files_pattern(self, test_name, file_names, pattern, expected_names, mock_os_walk):
        mock_os_walk.return_value = [(self.TEST_DIR, [], file_names)]

        result = get_files(self.TEST_DIR, pattern)

        self.assertEqual([(self.TEST_DIR, name) for name in expected_names], result, test_name)

    @parameterized.expand([
        ("get_subdirectories_test", TEST_DIR, [(name, True) for name in TEST_SUBDIRS], TEST_SUBDIRS),
        # Test case for retrieving subdirectories
        # Input: A directory with subdirectories
        # Expected Result: The function should return a list of subdirectory paths.

        ("get_subdirectories_test_no_subdirs", TEST_DIR, [], []),
        # Test case for retrieving subdirectories when none exist
        # Input: A directory with no subdirectories
        # Expected Result: The function should return an empty list.

        ("get_subdirectories_test_hidden", TEST_DIR, [(".git", True), ("subdir1", True)], ["subdir1"]),
        # Test case for skipping hidden directories
        # Input: A directory with the hidden directory .git and subdir1
        # Expected Result: The function should return subdir1 only.

        ("get_subdirectories_test_files", TEST_DIR, [("test1.f90", False), ("subdir1", True)], ["subdir1"]),
        # Test case for skipping files
        # Input: A directory with the file test1.f90 and subdir1
        # Expected Result: The function should return subdir1 only.
    ])
    @patch("tddlspserver.fxca.util.fxtran_utils.os.scandir")
    def test_get_subdirectories(self, test_name, test_path, entries, expected_subdirs, mock_os_scandir):
        # Set up the mock
        mock_entries = []
        for name, is_dir in entries:
            entry = MagicMock()
            entry.name = name
            entry.path = path.join(test_path, name)
            entry.is_dir.return_value = is_dir
            mock_entries.append(entry)
        mock_os_scandir.return_value = mock_entries

        result = get_subdirectories(test_path, False)

        # Assertions
        expected_full_paths = [path.join(test_path, subdir) for subdir in expected_subdirs]
        self.assertEqual(expected_full_paths, result, test_name)

    @parameterized.expand([
        ("get_subdirectories_test_recursive", ["subdir1", "subdir2"], ["subdir1", "subdir2"]),
        # Test case for retrieving subdirectories recursively
        # Input: A directory with two subdirectories
        # Expected Result: The function should return both subdirectories.

        ("get_subdirectories_test_nested", ["a", os.path.join("a", "b"), os.path.join("a", "b", "c")],
         ["a", os.path.join("a", "b"), os.path.join("a", "b", "c")]),
        # Test case for retrieving nested subdirectories
        # Input: A directory with the nested directories a/b/c
        # Expected Result: The function should return a, a/b and a/b/c.

        ("get_subdirectories_test_recursive_hidden", ["a", os.path.join("a", ".hidden"), os.path.join("a", "b")],
         ["a", os.path.join("a", "b")]),
        # Test case for skipping nested hidden directories
        # Input: A directory with a, a/.hidden and a/b
        # Expected Result: The function should return a and a/b.
    ])
    def test_get_subdirectories_recursive(self, test_name, directories, expected_subdirs):
        with tempfile.TemporaryDirectory() as root:
            for directory in directories:
                os.makedirs(os.path.join(root, directory))

            result = get_subdirectories(root, True)

        self.assertEqual(sorted(os.path.join(root, subdir) for subdir in expected_subdirs), sorted(result),
                         test_name)

    @parameterized.expand([
        ("write_decorate_src_xml_test", TEST_FILES, TEST_DIR, TEST_OUTPUT_DIR, FXTRAN_PATH, 2),
        # Test case for writing and decorating source XML
        # Input: A directory with Fortran files and an output directory
        # Expected Result: The function should create the output directory and process the files.

        ("write_decorate_src_xml_test_no_files", [], TEST_DIR, TEST_OUTPUT_DIR, FXTRAN_PATH, 0),
        # Test case for writing and decorating source XML with no Fortran files
        # Input: A directory with no Fortran files
        # Expected Result: The function should not attempt to create directories or run the fxtran command.

        ("write_decorate_src_xml_test_single_file", [("test_dir", "test1.f90")], TEST_DIR, TEST_OUTPUT_DIR,
         FXTRAN_PATH, 1),
        # Test case for writing and decorating a single source file
        # Input: A directory with one Fortran file
        # Expected Result: The function should create the output directory and run fxtran once.
    ])
    @patch("tddlspserver.fxca.util.fxtran_utils.get_files")
    @patch("tddlspserver.fxca.util.fxtran_utils.pathlib.Path.mkdir")
    @patch("tddlspserver.fxca.util.fxtran_utils.subprocess.check_output")
    def test_write_decorate_src_xml(self, test_name, test_files, src_dir, out_dir, fxtran_path, expected_calls,
                                    mock_check_output, mock_mkdir, mock_get_files):
        # Set up the mocks
        mock_get_files.return_value = test_files
        mock_check_output.return_value = b"Success"  # Simulate successful command execution

        write_decorate_src_xml(src_dir, out_dir, fxtran_path)  # writes files, returns nothing

        # Assertions
        mock_get_files.assert_called_once_with(src_dir, "*.[fF]90")
        self.assertEqual(expected_calls, mock_mkdir.call_count, test_name)
        self.assertEqual(expected_calls, mock_check_output.call_count, test_name)
        for (filepath, filename), call in zip(test_files, mock_check_output.call_args_list):
            self.assertTrue(call.args[0].startswith(f"{fxtran_path} -no-cpp -name-attr -code-tag -o "), test_name)
            self.assertTrue(call.args[0].endswith(f"{path.join(out_dir, filename)}.xml {filename}"), test_name)
            self.assertEqual(filepath, call.kwargs["cwd"], test_name)

    @parameterized.expand([
        ("write_decorate_src_xml_permission_error", PermissionError("Permission denied"), None, RuntimeError,
         "Permission denied for output directory"),
        # Test case for handling permission error when creating output directory
        # Input: A directory with Fortran files and an output directory where permission is denied
        # Expected Result: The function should raise a RuntimeError with a permission denied message.

        ("write_decorate_src_xml_fxtran_permission_error", None, PermissionError("Permission denied"), RuntimeError,
         "Permission denied for calling fxtran parser"),
        # Test case for handling permission error when executing the fxtran command
        # Input: A directory with Fortran files and an fxtran binary that may not be executed
        # Expected Result: The function should raise a RuntimeError naming the fxtran parser.

        ("write_decorate_src_xml_os_error", OSError("Disk full"), None, OSError, "Disk full"),
        # Test case for other errors when creating the output directory
        # Input: A directory with Fortran files and an output directory that cannot be created
        # Expected Result: The function should pass the OSError on.
    ])
    @patch("tddlspserver.fxca.util.fxtran_utils.get_files")
    @patch("tddlspserver.fxca.util.fxtran_utils.pathlib.Path.mkdir")
    @patch("tddlspserver.fxca.util.fxtran_utils.subprocess.check_output")
    def test_write_decorate_src_xml_errors(self, test_name, mkdir_error, fxtran_error, expected_error, expected_message,
                                           mock_check_output, mock_mkdir, mock_get_files):
        # Set up the mocks
        mock_get_files.return_value = self.TEST_FILES
        mock_mkdir.side_effect = mkdir_error
        mock_check_output.side_effect = fxtran_error

        with self.assertRaises(expected_error) as context:
            write_decorate_src_xml(self.TEST_DIR, self.TEST_OUTPUT_DIR, self.FXTRAN_PATH)

        # Assertions
        self.assertIn(expected_message, str(context.exception), test_name)

    @parameterized.expand([
        ("write_decorate_src_xml_fxtran_error", TEST_FILES, 2),
        # Test case for handling error when executing the fxtran command
        # Input: A directory with Fortran files and a valid output directory
        # Expected Result: The function should log a warning for each file when the fxtran command fails.

        ("write_decorate_src_xml_fxtran_error_single_file", [("test_dir", "test1.f90")], 1),
        # Test case for handling error when executing the fxtran command for one file
        # Input: A directory with one Fortran file
        # Expected Result: The function should log one warning.

        ("write_decorate_src_xml_fxtran_error_nested", [("test_dir", "test1.f90"), ("test_dir/sub", "test2.f90"),
                                                        ("test_dir/sub", "test3.f90")], 3),
        # Test case for handling errors in subdirectories
        # Input: Fortran files in the source directory and a subdirectory
        # Expected Result: The function should continue with the next file and log a warning for each file.
    ])
    @patch("tddlspserver.fxca.util.fxtran_utils.get_files")
    @patch("tddlspserver.fxca.util.fxtran_utils.pathlib.Path.mkdir")
    @patch("tddlspserver.fxca.util.fxtran_utils.subprocess.check_output")
    def test_write_decorate_src_xml_fxtran_error(self, test_name, test_files, expected_warnings, mock_check_output,
                                                 mock_mkdir, mock_get_files):
        # Set up the mocks
        mock_get_files.return_value = test_files
        mock_mkdir.return_value = None
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'fxtran', output=b'Error occurred')

        with self.assertLogs(logger, level='WARNING') as log:
            write_decorate_src_xml(self.TEST_DIR, self.TEST_OUTPUT_DIR, self.FXTRAN_PATH)

        # Assertions
        self.assertEqual(expected_warnings, len(log.output), test_name)
        self.assertIn('command "fxtran" return with error', log.output[0], test_name)


if __name__ == "__main__":
    unittest.main()
