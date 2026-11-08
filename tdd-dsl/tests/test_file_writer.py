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
"""Tests of the merge and write utils of the pFUnit generator (tddlspserver.filewriter.file_writer)."""

import unittest
from os import path
from unittest.mock import patch, mock_open

from parameterized import parameterized

from tddlspserver.filewriter.file_writer import (
    difflib_merge,
    cmake_merge,
    remove_fortran_subroutine_or_function,
    fortran_merge,
    hash_file,
    file_modified,
    write_file
)

ADD_LIBRARY = {"add_sut": ["add_library(add_sut\n  add.f90\n  )", "target_include_directories(add_sut PUBLIC include)"]}
ADD_TEST = {"test_add": ["add_pfunit_ctest (test_add\n  TEST_SOURCES test_add.pf\n  )"]}
CMAKE_MAIN = """...

add_library(existing_sut
  existing.f90
  )

target_include_directories(existing_sut PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
set_target_properties (existing_sut PROPERTIES
  Fortran_MODULE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

add_subdirectory(tests)"""
CMAKE_MAIN_MERGED = """...

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
CMAKE_MAIN_WITH_SUT = """add_library(add_sut
  old.f90
  )

target_include_directories(add_sut PUBLIC include)
set_target_properties (add_sut PROPERTIES
  Fortran_MODULE_DIRECTORY x)
"""

FUNCTION_IMPLEMENTATION = {"test_module": ["test_function", "    ! Function implementation here"]}


def fortran_module(statement: str = "") -> str:
    return f"""
        module test_module{statement}
        contains
        end module test_module
        """


def merged_fortran_module(statement: str, public: str = "\n        PUBLIC :: test_function") -> str:
    return f"""
        module test_module{statement}{public}
        contains
            ! Function implementation here

        end module test_module
        """


class TestPfUnitGeneratorUtils(unittest.TestCase):

    @parameterized.expand([
        ("modified_line", "line1\nline2\nline3", "line1\nline2 modified\nline3", "line1\nline2\nline2 modified\nline3"),
        # A changed line is kept in both versions
        # Input: three lines, the second one modified in the second content
        # Expected Result: both versions of the second line

        ("identical_content", "a\nb\nc", "a\nb\nc", "a\nb\nc"),
        # Identical contents
        # Input: the same three lines twice
        # Expected Result: the unchanged lines

        ("added_line", "a\nb", "a\nb\nc", "a\nb\nc"),
        # A line added in the second content
        # Input: 'a, b' and 'a, b, c'
        # Expected Result: 'a, b, c'

        ("removed_line", "a\nb\nc", "a\nc", "a\nb\nc"),
        # A line missing in the second content is kept
        # Input: 'a, b, c' and 'a, c'
        # Expected Result: 'a, b, c'
    ])
    def test_difflib_merge(self, test_name, file_content0, file_content1, expected_output):
        result = difflib_merge(file_content0, file_content1)
        self.assertEqual(expected_output.strip(), result.strip(), test_name)

    @parameterized.expand([
        ("add_library", ADD_LIBRARY, CMAKE_MAIN, CMAKE_MAIN_MERGED),
        # A new library is added to the main CMake file
        # Input: the add_sut library and a CMake file with the library existing_sut
        # Expected Result: add_library and target_include_directories of add_sut inserted, add_sut added to
        # set_target_properties

        ("replace_library", ADD_LIBRARY, CMAKE_MAIN_WITH_SUT, CMAKE_MAIN_WITH_SUT.replace("old.f90", "add.f90")),
        # An existing library is replaced
        # Input: the add_sut library and a CMake file that already defines add_sut with old.f90
        # Expected Result: the add_library statement lists add.f90

        ("add_test", ADD_TEST, "add_pfunit_ctest (test_sub\n  TEST_SOURCES test_sub.pf\n  )",
         "add_pfunit_ctest (test_sub\n  TEST_SOURCES test_sub.pf\n  )\n"
         "add_pfunit_ctest (test_add\n  TEST_SOURCES test_add.pf\n  )"),
        # A new pFUnit test is appended to the test CMake file
        # Input: the test test_add and a CMake file with the test test_sub
        # Expected Result: test_add appended after test_sub

        ("replace_test", ADD_TEST, "add_pfunit_ctest (test_add\n  TEST_SOURCES old.pf\n  )",
         "add_pfunit_ctest (test_add\n  TEST_SOURCES test_add.pf\n  )"),
        # An existing pFUnit test is replaced
        # Input: the test test_add and a CMake file that already defines test_add with old.pf
        # Expected Result: the test lists test_add.pf
    ])
    def test_cmake_merge(self, test_name, insert_contents, file_content, expected_output):
        result = cmake_merge(insert_contents, file_content)
        self.assertEqual(expected_output.strip(), result.strip(), test_name)

    @parameterized.expand([
        ("cmake_without_target_include", cmake_merge, ADD_LIBRARY, "add_library(x\n  x.f90\n  )\n",
         "target_include_directories statement not found."),
        # A new library needs a target_include_directories statement to insert it before
        # Input: a CMake file with add_library only
        # Expected Result: ValueError about the missing target_include_directories statement

        ("cmake_without_set_target", cmake_merge, ADD_LIBRARY,
         "add_library(x\n  x.f90\n  )\ntarget_include_directories(x PUBLIC y)\n",
         "set_target_properties statement not found."),
        # A new library is added to the set_target_properties statement
        # Input: a CMake file without set_target_properties
        # Expected Result: ValueError about the missing set_target_properties statement

        ("fortran_without_module", fortran_merge, {"m": ["f", "impl"]}, "subroutine s()\nend subroutine s\n",
         "Private/Public, Module or \"Implicit\" statement not found. Module: m"),
        # The operation is inserted into its module
        # Input: Fortran code without the module m
        # Expected Result: ValueError about the missing module statement

        ("fortran_without_module_end", fortran_merge, {"m": ["f", "impl"]}, "\nmodule m\n",
         "Module statement not found. Module: m"),
        # The implementation is inserted before the module end
        # Input: Fortran code with 'module m' but without 'end module m'
        # Expected Result: ValueError about the missing module end
    ])
    def test_merge_errors(self, test_name, merge, insert_contents, file_content, expected_message):
        with self.assertRaises(ValueError) as context:
            merge(insert_contents, file_content)
        self.assertEqual(expected_message, str(context.exception), test_name)

    @parameterized.expand([
        ("subroutine_template", """
        subroutine test_subroutine()
            ! <<Replace with SUBROUTINE body here>>
        end subroutine test_subroutine
        """, ["test_subroutine"], ""),
        # A generated subroutine template is removed
        # Input: a subroutine with the template comment of the SUBROUTINE body
        # Expected Result: empty code

        ("elemental_function_template", """
        elemental function f(a)
            ! <<Replace with return expression here>>
        end function f
        """, ["f"], ""),
        # A generated function template with an attribute is removed
        # Input: an elemental function with the template comment of the return expression
        # Expected Result: empty code

        ("implemented_subroutine", """
        subroutine keep()
            call x()
        end subroutine keep
        """, ["keep"], "subroutine keep()\n            call x()\n        end subroutine keep"),
        # Implemented routines are kept
        # Input: a subroutine without the template comment
        # Expected Result: the unchanged subroutine

        ("other_name", """
        subroutine other()
            ! <<Replace with SUBROUTINE body here>>
        end subroutine other
        """, ["test_subroutine"],
         "subroutine other()\n            ! <<Replace with SUBROUTINE body here>>\n        end subroutine other"),
        # Only the named routines are removed
        # Input: the template of the subroutine other, name test_subroutine
        # Expected Result: the unchanged subroutine other
    ])
    def test_remove_fortran_subroutine_or_function(self, test_name, fortran_code, names, expected_output):
        result = remove_fortran_subroutine_or_function(fortran_code, names)
        self.assertEqual(expected_output.strip(), result.strip(), test_name)

    @parameterized.expand([
        ("after_module_start", FUNCTION_IMPLEMENTATION, fortran_module(), merged_fortran_module("")),
        # Without access statements the public statement follows the module statement
        # Input: test_function and a module without public, private and implicit statements
        # Expected Result: 'PUBLIC :: test_function' after the module statement, the implementation before its end

        ("after_implicit_none", FUNCTION_IMPLEMENTATION, fortran_module("\n        implicit none"),
         merged_fortran_module("\n        implicit none")),
        # The public statement follows 'implicit none'
        # Input: test_function and a module with 'implicit none'
        # Expected Result: 'PUBLIC :: test_function' after 'implicit none'

        ("after_private", FUNCTION_IMPLEMENTATION, fortran_module("\n        private"),
         merged_fortran_module("\n        private")),
        # The public statement follows the private statement
        # Input: test_function and a module with 'private'
        # Expected Result: 'PUBLIC :: test_function' after 'private'

        ("extend_public", FUNCTION_IMPLEMENTATION, fortran_module("\n        public :: other"),
         merged_fortran_module("\n        public :: other", public=", test_function")),
        # An existing public statement is extended
        # Input: test_function and a module with 'public :: other'
        # Expected Result: 'public :: other, test_function'

        ("empty_operation", {"test_module": ["", ""]}, "module test_module\nend module test_module\n",
         "module test_module\nend module test_module\n"),
        # Empty operations are skipped
        # Input: an operation without name and implementation
        # Expected Result: the unchanged module
    ])
    def test_fortran_merge(self, test_name, insert_content, file_content, expected_output):
        result = fortran_merge(insert_content, file_content)
        self.assertEqual(expected_output.strip(), result.strip(), test_name)

    @parameterized.expand([
        ("text", b"data", "8d777f385d3dfec8815d20f7496026dc"),
        # The MD5 hash of a short text
        # Input: b"data"
        # Expected Result: 8d777f385d3dfec8815d20f7496026dc

        ("empty", b"", "d41d8cd98f00b204e9800998ecf8427e"),
        # The MD5 hash of an empty file
        # Input: b""
        # Expected Result: d41d8cd98f00b204e9800998ecf8427e

        ("large", b"a" * (10 ** 9), "c9fad513774bd938134c288576bd93cc"),
        # The MD5 hash of a large file
        # Input: 10^9 times b"a"
        # Expected Result: c9fad513774bd938134c288576bd93cc

        ("newlines", b"\n\n\n", "2228e977ebea8966e27929f43e39cb67"),
        # Newlines are hashed
        # Input: three newlines
        # Expected Result: 2228e977ebea8966e27929f43e39cb67

        ("mixed_line_endings", b"line0\r\nline1\nline2\r", "cc5b4fa5fe1201bb64140e3f4da0a501"),
        # Line endings are not normalized
        # Input: CRLF, LF and CR line endings
        # Expected Result: cc5b4fa5fe1201bb64140e3f4da0a501

        ("binary", b"\x00\x01\x02\x03", "37b59afd592725f9305e484a5d7f5168"),
        # Binary content
        # Input: the bytes 0 to 3
        # Expected Result: 37b59afd592725f9305e484a5d7f5168
    ])
    @patch("builtins.open", new_callable=mock_open)
    def test_hash_file(self, test_name, file_data, expected_hash, mock_file):
        mock_file.return_value.read.return_value = file_data  # Set the mock file data
        result = hash_file("dummy_path")
        self.assertEqual(expected_hash, result, test_name)

    @parameterized.expand([
        ("file_not_found", "non_existent_file", FileNotFoundError, "File not found: non_existent_file"),
        # A missing file
        # Input: open raises FileNotFoundError
        # Expected Result: ValueError 'File not found: non_existent_file'

        ("io_error", "restricted_file", IOError("Permission denied"),
         "Error reading file restricted_file: Permission denied"),
        # A file that cannot be read
        # Input: open raises IOError('Permission denied')
        # Expected Result: ValueError with the path and the error

        ("permission_error", "locked_file", PermissionError("Access denied"),
         "Error reading file locked_file: Access denied"),
        # PermissionError is an IOError as well
        # Input: open raises PermissionError('Access denied')
        # Expected Result: ValueError with the path and the error
    ])
    def test_hash_file_errors(self, test_name, file_path, error, expected_message):
        with patch("builtins.open", side_effect=error):
            with self.assertRaises(ValueError) as context:
                hash_file(file_path)
        self.assertEqual(expected_message, str(context.exception), test_name)

    @parameterized.expand([
        ("older_and_different_hash", 0, "different_hash", True),
        # The file is newer and its hash changed
        # Input: known mtime 0 (file mtime 1), known hash different
        # Expected Result: modified

        ("older_same_hash", 0, "dummy_hash", True),
        # The file is newer than known
        # Input: known mtime 0 (file mtime 1), same hash
        # Expected Result: modified

        ("same_time_different_hash", 1, "different_hash", True),
        # The hash changed
        # Input: known mtime 1 (file mtime 1), known hash different
        # Expected Result: modified

        ("same_time_same_hash", 1, "dummy_hash", False),
        # Neither time nor hash changed
        # Input: known mtime 1 (file mtime 1), same hash
        # Expected Result: not modified

        ("newer_same_hash", 2, "dummy_hash", False),
        # The known time is newer and the hash is the same
        # Input: known mtime 2 (file mtime 1), same hash
        # Expected Result: not modified
    ])
    @patch("tddlspserver.filewriter.file_writer.getmtime", return_value=1)
    @patch("tddlspserver.filewriter.file_writer.hash_file", return_value="dummy_hash")
    def test_file_modified(self, test_name, mtime, file_hash, expected_result, mock_hash, mock_getmtime):
        result = file_modified("dummy_path", mtime, file_hash)
        self.assertEqual(expected_result, result, test_name)
        mock_getmtime.assert_called_once_with("dummy_path")
        if mtime >= 1:  # the hash is only computed if the modification time does not decide
            mock_hash.assert_called_once_with("dummy_path")

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
        ("new_file", FILE_DOES_NOT_EXIST, DIR_EXISTS, FILE_NOT_MODIFIED, SHOULD_INSERT, FILE_PATH, NEW_CONTENT,
         MOD_CONTENT, EXISTING_CONTENT, MODIFIED_TIME, MOCKED_HASH, NEW_CONTENT,
         (MODIFIED_TIME, MOCKED_HASH, EMPTY_CONTENT)),
        # A new file is created
        # Input: a file that does not exist, the content to write
        # Expected Result: the content is written, the original content of a new pFUnit file is empty

        ("existing_file_modified", FILE_EXISTS, DIR_EXISTS, FILE_MODIFIED, SHOULD_INSERT, FILE_PATH, NEW_CONTENT,
         MOD_CONTENT, EXISTING_CONTENT, MODIFIED_TIME, MOCKED_HASH, f"{NEW_CONTENT}\n{MOD_CONTENT}",
         (MODIFIED_TIME, MOCKED_HASH, MOD_CONTENT)),
        # A file that was modified on disk is reloaded and merged
        # Input: an existing file whose content on disk was modified, new content to insert
        # Expected Result: the new content merged with the content on disk

        ("existing_file_not_modified", FILE_EXISTS, DIR_EXISTS, FILE_NOT_MODIFIED, SHOULD_INSERT, FILE_PATH,
         NEW_CONTENT, MOD_CONTENT, EXISTING_CONTENT, MODIFIED_TIME, MOCKED_HASH, f"{NEW_CONTENT}\n{EXISTING_CONTENT}",
         (MODIFIED_TIME, MOCKED_HASH, EXISTING_CONTENT)),
        # A file that was not modified is merged with its known content
        # Input: an existing, unmodified file, new content to insert
        # Expected Result: the new content merged with the known content, the file is not read

        ("new_directory", FILE_DOES_NOT_EXIST, DIR_DOES_NOT_EXIST, FILE_NOT_MODIFIED, SHOULD_INSERT, FILE_PATH,
         NEW_CONTENT, MOD_CONTENT, EXISTING_CONTENT, MODIFIED_TIME, MOCKED_HASH, NEW_CONTENT,
         (MODIFIED_TIME, MOCKED_HASH, EMPTY_CONTENT)),
        # A missing directory is created
        # Input: a file in a directory that does not exist
        # Expected Result: the directory is created and the content written

        ("existing_file_overwritten", FILE_EXISTS, DIR_EXISTS, FILE_NOT_MODIFIED, SHOULD_NOT_INSERT, FILE_PATH,
         NEW_CONTENT, MOD_CONTENT, EXISTING_CONTENT, MODIFIED_TIME, MOCKED_HASH, NEW_CONTENT,
         (MODIFIED_TIME, MOCKED_HASH, EXISTING_CONTENT)),
        # Without insert the file is overwritten
        # Input: an existing, unmodified file, new content, insert disabled
        # Expected Result: only the new content is written, the known content is returned as original content
    ])
    @patch("builtins.open", new_callable=mock_open)
    @patch("tddlspserver.filewriter.file_writer.exists")
    @patch("tddlspserver.filewriter.file_writer.makedirs")
    @patch("tddlspserver.filewriter.file_writer.isdir")
    @patch("tddlspserver.filewriter.file_writer.file_modified")
    @patch("tddlspserver.filewriter.file_writer.hash_file")
    @patch("tddlspserver.filewriter.file_writer.getmtime")
    def test_write_file(self, test_name, file_exists, dir_exists, is_file_modified, should_insert, file_path,
                        new_content, mod_content, existing_content, modified_time, mocked_hash, expected_written,
                        expected_result,
                        mock_getmtime, mock_hash_file, mock_file_modified, mock_isdir, mock_makedirs, mock_exists,
                        mock_file):
        # Set up the mocks
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
        if dir_exists:
            mock_makedirs.assert_not_called()
        else:
            mock_makedirs.assert_called_once_with(self.TEST_DIR)
        mock_exists.assert_called_once_with(file_path)
        if file_exists:
            mock_file_modified.assert_called_once_with(file_path, modified_time, mocked_hash)
        else:
            mock_file_modified.assert_not_called()

        if is_file_modified:
            mock_file().read.assert_called_once()
        else:
            mock_file().read.assert_not_called()
        mock_getmtime.assert_called_once_with(file_path)
        mock_hash_file.assert_called_once_with(file_path)
        mock_file().write.assert_called_once_with(expected_written)

        self.assertIsInstance(result, tuple)
        self.assertEqual(expected_result, result, test_name)


if __name__ == "__main__":
    unittest.main()
