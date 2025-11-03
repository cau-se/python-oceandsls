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

    # Define constants for the write file test case
    TEST_DIR = "test_dir"
    FILE_NAME = "test.pf"
    FILE_PATH = path.join(TEST_DIR, FILE_NAME)
    NEW_CONTENT = "new content"
    MOD_CONTENT = "mod content"
    EMPTY_CONTENT = ""
    EXISTING_CONTENT = "existing content"
    MOCKED_HASH = "mocked_hash"
    MODIFIED_TIME = 1234567890.0

    # Define boolean constants for clarity
    FILE_DOES_NOT_EXIST = False
    FILE_EXISTS = True
    DIR_DOES_NOT_EXIST = False
    DIR_EXISTS = True
    FILE_MODIFIED = True
    FILE_NOT_MODIFIED = False
    SHOULD_INSERT = True
    SHOULD_NOT_INSERT = False

    @parameterized.expand([
            # Test case for a new file
            # Input: A file that does not exist (file_exists is False), the content to write, and the expected result.
            # Expected Result: The function should create the file and write the content.
            ("new_file", FILE_DOES_NOT_EXIST, DIR_EXISTS, FILE_NOT_MODIFIED,SHOULD_INSERT, FILE_PATH, NEW_CONTENT, MOD_CONTENT ,EXISTING_CONTENT, MODIFIED_TIME, MOCKED_HASH, NEW_CONTENT, (MODIFIED_TIME, MOCKED_HASH, EMPTY_CONTENT)),
            # Test case for an existing file that is modified
            # Input: A file that exists and has been modified (file_exists is True and file_modified returns True), along with new content.
            # Expected Result: The function should overwrite the existing content with the new content.
            ("existing_file_modified", FILE_EXISTS, DIR_EXISTS, FILE_MODIFIED,SHOULD_INSERT, FILE_PATH, NEW_CONTENT,  MOD_CONTENT, EXISTING_CONTENT,MODIFIED_TIME, MOCKED_HASH,  f"{NEW_CONTENT}\n{MOD_CONTENT}", (MODIFIED_TIME, MOCKED_HASH, MOD_CONTENT)),
            # Test case for an existing file that is not modified
            # Input: A file that exists but has not been modified (file_exists is True and file_modified returns False), along with new content.
            # Expected Result: The function should not overwrite the existing content.
            ("existing_file_not_modified", FILE_EXISTS, DIR_EXISTS, FILE_NOT_MODIFIED,SHOULD_INSERT, FILE_PATH, NEW_CONTENT, MOD_CONTENT, EXISTING_CONTENT,MODIFIED_TIME, MOCKED_HASH,  f"{NEW_CONTENT}\n{EXISTING_CONTENT}", (MODIFIED_TIME, MOCKED_HASH, EXISTING_CONTENT)),
    ])
    @patch("builtins.open", new_callable=mock_open)
    @patch("filewriter.file_writer.exists")
    @patch("filewriter.file_writer.makedirs")
    @patch("filewriter.file_writer.isdir")
    @patch("filewriter.file_writer.file_modified")
    @patch("filewriter.file_writer.hash_file")
    @patch("filewriter.file_writer.getmtime")
    def test_write_file(self, test_name, file_exists, dir_exists, is_file_modified,should_insert, file_path, new_content, mod_content, existing_content, modified_time, mocked_hash, expected_written,expected_result,
                        mock_getmtime, mock_hash_file, mock_file_modified, mock_isdir, mock_makedirs, mock_exists, mock_file):

        # Setup the mocks
        mock_isdir.return_value = dir_exists
        mock_exists.return_value = file_exists
        mock_file_modified.return_value = is_file_modified
        mock_getmtime.return_value = modified_time
        mock_hash_file.return_value = mocked_hash

        if is_file_modified:
            mock_file().read.return_value = mod_content

        file_attribute = (modified_time, mocked_hash, existing_content) if file_exists else None

        result = write_file(file_path, new_content, file_attribute, should_insert)

        # Assertions
        mock_makedirs.assert_called_once() if not dir_exists else mock_makedirs.assert_not_called()
        mock_exists.assert_called_once_with(file_path)
        if file_exists:
            mock_file_modified.assert_called_once_with(file_path, modified_time, mocked_hash)
        else:
            mock_file_modified.assert_not_called()

        mock_file().read.assert_called_once() if is_file_modified else mock_file().read.assert_not_called()
        mock_getmtime.assert_called_once_with(file_path)
        mock_hash_file.assert_called_once_with(file_path)
        mock_file().write.assert_called_once_with(expected_written)

        self.assertIsInstance(result, tuple)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
