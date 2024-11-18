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
from unittest.mock import patch, mock_open
from parameterized import parameterized

from filewriter.file_writer import (
    difflib_merge,
    cmake_merge,
    remove_fortran_subroutine_or_function,
    fortran_merge,
    hash_file,
    file_modified,
    write_file
)

class TestPfUnitGeneratorUtils(unittest.TestCase):

    def test_difflib_merge(self):
        file_content0 = "line1\nline2\nline3"
        file_content1 = "line1\nline2 modified\nline3"
        expected_output = "line1\nline2\nline2 modified\nline3"
        result = difflib_merge(file_content0, file_content1)
        self.assertEqual(expected_output.strip(), result.strip())

    def test_cmake_merge_add_library(self):
        insert_contents = {
                "add_sut": [
                        """add_library(add_sut
  add.f90
  )""",
                        "target_include_directories(add_sut PUBLIC include)"
                ]
        }
        file_content = """...

add_library(existing_sut
  existing.f90
  )

target_include_directories(existing_sut PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
set_target_properties (existing_sut PROPERTIES
  Fortran_MODULE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

add_subdirectory(tests)"""
        expected_output = (
                """...

add_library(existing_sut
  existing.f90
  )

add_library(add_sut
  add.f90
  )

target_include_directories(existing_sut PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
target_include_directories(add_sut PUBLIC include)
set_target_properties (existing_sut add_sut PROPERTIES
  Fortran_MODULE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

add_subdirectory(tests)"""
        )
        result = cmake_merge(insert_contents, file_content)
        self.assertEqual(expected_output.strip(), result.strip())

    def test_remove_fortran_subroutine_or_function(self):
        fortran_code = """
        subroutine test_subroutine()
            ! <<Replace with SUBROUTINE body here>>
        end subroutine test_subroutine
        """
        names = ["test_subroutine"]
        expected_output = ""
        result = remove_fortran_subroutine_or_function(fortran_code, names)
        self.assertEqual(expected_output.strip(), result.strip())

    def test_fortran_merge(self):
        insert_content = {
                "test_module": [
                        "test_function",
                        "    ! Function implementation here"
                ]
        }
        file_content = """
        module test_module
        contains
        end module test_module
        """
        expected_output = """
        module test_module
        PUBLIC :: test_function
        contains
            ! Function implementation here

        end module test_module
        """
        result = fortran_merge(insert_content, file_content)
        self.assertEqual(expected_output.strip(), result.strip())

    @parameterized.expand([
            (b"data", "8d777f385d3dfec8815d20f7496026dc"),
            (b"", "d41d8cd98f00b204e9800998ecf8427e"),
            (b"a" * (10**9), "c9fad513774bd938134c288576bd93cc"),
            (b"\n\n\n", "2228e977ebea8966e27929f43e39cb67"),
            (b"line0\r\nline1\nline2\r", "cc5b4fa5fe1201bb64140e3f4da0a501"),
            (b"\x00\x01\x02\x03", "37b59afd592725f9305e484a5d7f5168")
    ])
    @patch("builtins.open", new_callable=mock_open)
    def test_hash_file(self, file_data, expected_hash, mock_file):
        path = "dummy_path"
        mock_file.return_value.read.return_value = file_data  # Set the mock file data
        result = hash_file(path)
        self.assertEqual(expected_hash, result)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_hash_file_not_found(self, mock_file):
        path = "non_existent_file"
        with self.assertRaises(ValueError) as context:
            hash_file(path)
        self.assertEqual(str(context.exception), f"File not found: {path}")

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_hash_file_io_error(self, mock_file):
        path = "restricted_file"
        with self.assertRaises(ValueError) as context:
            hash_file(path)
        self.assertEqual(str(context.exception), f"Error reading file {path}: Permission denied")

    @parameterized.expand([
            (0, "different_hash", True),  # mtime < getmtime and hash is different
            (0, "dummy_hash", True),      # mtime < getmtime
            (1, "different_hash", True),  # hash is different
            (1, "dummy_hash", False),     # mtime == getmtime and hash is the same
            (2, "dummy_hash", False),     # mtime > getmtime and hash is the same
    ])
    @patch("filewriter.file_writer.getmtime", return_value=1)
    @patch("filewriter.file_writer.hash_file", return_value="dummy_hash")
    def test_file_modified(self, mtime, file_hash, expected_result, mock_hash, mock_getmtime):
        path = "dummy_path"
        result = file_modified(path, mtime, file_hash)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
            # Test case for a new file
            ("new_file", False, True, path.join("test_dir", "test.pf"), "test content", (1234567890.0, "mocked_hash", "")),
            # Test case for an existing file that is modified
            ("existing_file_modified", True, True, path.join("test_dir", "test.pf"), "new content", (1234567890.0, "mocked_hash", "existing content")),
            # Test case for an existing file that is not modified
            ("existing_file_not_modified", True, False, path.join("test_dir", "test.pf"), "new content", (1234567890.0, "mocked_hash", "existing content")),
    ])
    @patch("builtins.open", new_callable=mock_open)
    @patch("filewriter.file_writer.exists")
    @patch("filewriter.file_writer.makedirs")
    @patch("filewriter.file_writer.isdir")
    @patch("filewriter.file_writer.file_modified")
    @patch("filewriter.file_writer.hash_file")
    @patch("filewriter.file_writer.getmtime")
    def test_write_file(self, name, file_exists, dir_exists, file_path, content, expected_result,
                        mock_getmtime, mock_hash_file, mock_file_modified, mock_isdir, mock_makedirs, mock_exists, mock_file):

        # Setup the mocks
        mock_exists.return_value = file_exists  # Simulate whether the file exists
        mock_isdir.return_value = dir_exists  # Simulate whether the directory exists
        mock_getmtime.return_value = 1234567890.0  # Mock the modification time
        mock_hash_file.return_value = "mocked_hash"  # Mock the file hash

        if file_exists:
            mock_file_modified.return_value = True  # Simulate that the file is modified
            mock_file().read.return_value = "existing content"  # Mock the existing file content
        else:
            mock_file_modified.return_value = False  # Simulate that the file is not modified

        result = write_file(file_path, content)

        # Assertions
        mock_file().write.assert_called_once_with(content)
        mock_exists.assert_called_once_with(file_path)
        mock_makedirs.assert_called_once() if not dir_exists else mock_makedirs.assert_not_called()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
