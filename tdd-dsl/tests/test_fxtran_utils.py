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

import unittest
from os import path
from unittest.mock import patch, mock_open, MagicMock
from parameterized import parameterized
import subprocess

from fxca.util.fxtran_utils import (
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

    MODULE_MOCK = MagicMock( spec= 'ModuleSymbol' )
    MODULE_MOCK.name = 'moduleMock'  # Set the name attribute

    @parameterized.expand([
            ("filter_xml_test_empty", TEST_XML_PATH, False, [], {}, ([], [])),
            # Test case for filtering XML with no modules and an empty XML file
            # Input: An empty XML structure
            # Expected Result: The function should return empty lists for variables and scopes.

            ("filter_xml_test_with_modules", TEST_XML_PATH, True, [ MODULE_MOCK ], {}, ([], [])),
            # Test case for filtering XML with modules
            # Input: A valid XML path and a list of modules
            # Expected Result: The function should process the XML and return the expected results.

            ("filter_xml_test_with_public_elements", TEST_XML_PATH, True, [ MODULE_MOCK ], {}, ([], [])),
            # Test case for filtering XML with public elements
            # Input: A valid XML path and a list of modules with public elements
            # Expected Result: The function should process the XML and return the expected results.
    ])
    @patch("fxca.util.fxtran_utils.ET.parse")
    @patch("fxca.util.fxtran_utils.PublicObj")
    def test_filter_xml(self, test_name, xml_path, need_public, modules, files, expected_result, mock_public_obj, mock_et_parse):
        # Setup the mocks
        mock_tree = mock_et_parse.return_value
        mock_tree.getroot.return_value.iter.return_value = []  # Mocking an empty XML structure

        result = filter_xml(xml_path, need_public, modules, files)

        # Assertions
        self.assertEqual(expected_result, result)

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
    @patch("fxca.util.fxtran_utils.os.walk")
    def test_get_files( self, test_name, test_path, pattern, expected_files, mock_os_walk ):
        # Setup the mock
        if expected_files:
            # Create a structure for os.walk based on expected_files
            mock_walk_output = []
            seen_dirs = set()

            for dir_name, file_name in expected_files:
                if dir_name not in seen_dirs:
                    # Add the directory to the mock output
                    mock_walk_output.append( (test_path, [ dir_name ], []) )
                    seen_dirs.add(dir_name)
                # Add the file to the corresponding directory
                mock_walk_output.append( ( dir_name, [], [ file_name ]) )

            # Add the main directory entry if there are no subdirectories
            if not seen_dirs:
                mock_walk_output.append( (test_path, [], [ file_name for _, file_name in expected_files ]) )

            mock_os_walk.return_value = mock_walk_output
        else:
            mock_os_walk.return_value = [ (test_path, [], []) ]  # No files

        result = get_files( test_path, pattern )

        # Assertions
        self.assertEqual(result, expected_files)

    @parameterized.expand([
            ("get_subdirectories_test", TEST_DIR, False, TEST_SUBDIRS),
            # Test case for retrieving subdirectories
            # Input: A directory with subdirectories
            # Expected Result: The function should return a list of subdirectory names.

            ("get_subdirectories_test_no_subdirs", TEST_DIR, False, []),
            # Test case for retrieving subdirectories when none exist
            # Input: A directory with no subdirectories
            # Expected Result: The function should return an empty list.

            # ("get_subdirectories_test_recursive", TEST_DIR, True, TEST_SUBDIRS),
            # # Test case for retrieving subdirectories recursively
            # # Input: A directory with nested subdirectories
            # # Expected Result: The function should return a list of all subdirectory names.
    ])
    @patch("fxca.util.fxtran_utils.os.scandir")
    def test_get_subdirectories(self, test_name, test_path, recursive, expected_subdirs, mock_os_scandir):
        # Setup the mock
        if expected_subdirs:
            mock_entries = [MagicMock() for _ in expected_subdirs]
            mock_os_scandir.return_value = mock_entries
            for entry, subdir in zip(mock_os_scandir.return_value, expected_subdirs):
                entry.name = subdir
                entry.path = path.join(test_path, subdir)
                entry.is_dir.return_value = True
        else:
            mock_os_scandir.return_value = []  # No subdirectories

        result = get_subdirectories(test_path, recursive)

        # Assertions
        expected_full_paths = [path.join(test_path, subdir) for subdir in expected_subdirs]
        self.assertEqual(expected_full_paths, result)

    @parameterized.expand([
            ("write_decorate_src_xml_test",TEST_FILES, TEST_DIR, TEST_OUTPUT_DIR, FXTRAN_PATH),
            # Test case for writing and decorating source XML
            # Input: A directory with Fortran files and an output directory
            # Expected Result: The function should create the output directory and process the files.

            ("write_decorate_src_xml_test_no_files",TEST_FILES, TEST_DIR, TEST_OUTPUT_DIR, FXTRAN_PATH),
            # Test case for writing and decorating source XML with no Fortran files
            # Input: A directory with no Fortran files
            # Expected Result: The function should not attempt to create directories or run the fxtran command.
    ])
    @patch("fxca.util.fxtran_utils.get_files")
    @patch("fxca.util.fxtran_utils.pathlib.Path.mkdir")
    @patch("fxca.util.fxtran_utils.subprocess.check_output")
    def test_write_decorate_src_xml(self, test_name, test_files, src_dir, out_dir, fxtran_path, mock_check_output, mock_mkdir, mock_get_files):
        # Setup the mocks
        if test_name == "write_decorate_src_xml_test":
            mock_get_files.return_value = test_files
            mock_check_output.return_value = b"Success"  # Simulate successful command execution
        else:
            mock_get_files.return_value = []  # No files

        result = write_decorate_src_xml(src_dir, out_dir, fxtran_path)

        # Assertions
        mock_get_files.assert_called_once_with(src_dir, "*.[fF]90")
        if test_name == "write_decorate_src_xml_test":
            mock_mkdir.assert_called()  # Check if mkdir was called
            self.assertIsNone(result)  # Assuming the function does not return anything
        else:
            mock_mkdir.assert_not_called()  # No mkdir should be called if there are no files
            self.assertIsNone(result)  # Assuming the function does not return anything

    @parameterized.expand([
            ("write_decorate_src_xml_permission_error",TEST_FILES, TEST_DIR, TEST_OUTPUT_DIR, FXTRAN_PATH),
            # Test case for handling permission error when creating output directory
            # Input: A directory with Fortran files and an output directory where permission is denied
            # Expected Result: The function should raise a RuntimeError with a permission denied message.
    ])
    @patch("fxca.util.fxtran_utils.get_files")
    @patch("fxca.util.fxtran_utils.pathlib.Path.mkdir")
    @patch("fxca.util.fxtran_utils.subprocess.check_output")
    def test_write_decorate_src_xml_permission_error(self, test_name, test_files, src_dir, out_dir, fxtran_path, mock_check_output, mock_mkdir, mock_get_files):
        # Setup the mocks
        mock_get_files.return_value = test_files
        mock_mkdir.side_effect = PermissionError("Permission denied")

        with self.assertRaises(RuntimeError) as context:
            write_decorate_src_xml(src_dir, out_dir, fxtran_path)

        # Assertions
        self.assertIn("Permission denied for output directory", str(context.exception))

    @parameterized.expand([
            ("write_decorate_src_xml_fxtran_error",TEST_FILES, TEST_DIR, TEST_OUTPUT_DIR, FXTRAN_PATH),
            # Test case for handling error when executing the fxtran command
            # Input: A directory with Fortran files and a valid output directory
            # Expected Result: The function should log a warning when the fxtran command fails.
    ])
    @patch("fxca.util.fxtran_utils.get_files")
    @patch("fxca.util.fxtran_utils.pathlib.Path.mkdir")
    @patch("fxca.util.fxtran_utils.subprocess.check_output")
    def test_write_decorate_src_xml_fxtran_error(self, test_name, test_files, src_dir, out_dir, fxtran_path, mock_check_output, mock_mkdir, mock_get_files):
        # Setup the mocks
        mock_get_files.return_value = test_files
        mock_mkdir.return_value = None
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'fxtran', output=b'Error occurred')

        with self.assertLogs(logger, level='WARNING') as log:
            write_decorate_src_xml(src_dir, out_dir, fxtran_path)

        # Assertions
        self.assertIn('command "fxtran" return with error', log.output[0])

if __name__ == "__main__":
    unittest.main()
