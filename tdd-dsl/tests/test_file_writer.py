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
from unittest.mock import patch, mock_open
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

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_hash_file(self, mock_file):
        path = "dummy_path"
        expected_hash = ""  # MD5 of empty string
        result = hash_file(path)
        self.assertEqual(expected_hash, result)

    @patch("os.path.getmtime", return_value=1)
    @patch("module.hash_file", return_value="dummy_hash")
    def test_file_modified(self, mock_hash, mock_getmtime):
        path = "dummy_path"
        mtime = 0
        file_hash = "different_hash"
        result = file_modified(path, mtime, file_hash)
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_write_file_new(self, mock_file):
        file_path = "test.pf"
        content = "test content"
        result = write_file(file_path, content)
        mock_file().write.assert_called_once_with(content)
        self.assertIsInstance(result, tuple)

if __name__ == "__main__":
    unittest.main()
