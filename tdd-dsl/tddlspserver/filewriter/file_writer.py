"""pfUnit generator utils to generate *.pf Fortran unit tests files"""

__author__ = "sgu"

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

from difflib import Differ
from hashlib import md5
# Utils
from logging import DEBUG, getLogger
from re import search, sub, escape, IGNORECASE, MULTILINE, DOTALL
from os import path, makedirs
from os.path import getmtime, dirname, isdir, splitext, exists
from typing import Any, Dict, List, Tuple

# Debug
logger = getLogger(__name__)

show_debug_output: bool = False


def difflib_merge(file_content0: str, file_content1: str) -> str:
    """
    Merge two file-contents based on difflib.

    :param file_content0: Content of first file
    :param file_content1: Content of second file
    :return: 3-way merge of comparing the first file and second file
    """
    merged_content = "\n".join(
        lines[2:] for lines in Differ( ).compare(
            file_content0.split("\n"), file_content1.split("\n")
        ) if not lines.startswith("?")
    )

    return merged_content


def cmake_merge(insert_contents: Dict[str, str], file_content):
    """
    Merge cmake configuration files.

    :param insert_contents: List of code to be merged
    :param file_content: File content in which to be merged
    :return: Merged content
    """

    first_sut = next(iter(insert_contents.values()))

    # Check if main or test file needs to be merged
    if first_sut[0].startswith("add_library"):

        for sut_name, sut_statements in insert_contents.items():

            library_statement = sut_statements[0]
            target_include_statements = sut_statements[1]

            # Check if library exists
            add_library_pattern = r"^ *add_library *\( *" + sut_name + r"[^\)]*\)$"
            match_add_library = search(add_library_pattern, file_content, IGNORECASE | MULTILINE | DOTALL)
            if match_add_library:
                # Replace add_library statement
                file_content = sub(add_library_pattern, library_statement, file_content, flags=IGNORECASE | MULTILINE | DOTALL)
            else:
                # Add library statement and target include statement and extend set_target statement

                target_include_pattern = r"(^target_include_directories\([^\)]*\)$\n)+"
                set_target_pattern = r"^set_target_properties \([^\n]*( PROPERTIES)$"

                # Find the position to insert the new code
                match_target_include = search(target_include_pattern, file_content, flags=IGNORECASE | MULTILINE | DOTALL)

                # Add add_library statement and extend set_target statement
                if match_target_include:
                    insert_position_start = match_target_include.start()
                    insert_position_end = match_target_include.end()
                else:
                    # If target_include_directories is not found, raise an error
                    raise ValueError(f"target_include_directories statement not found.")

                # Insert library and target statement
                file_content = (file_content[:insert_position_start] + library_statement + "\n\n" + file_content[
                    insert_position_start:insert_position_end] + target_include_statements + "\n" + file_content[
                    insert_position_end:])

                match_set_target = search(set_target_pattern, file_content, flags=IGNORECASE | MULTILINE | DOTALL)

                # Insert target_include statement
                if match_set_target:
                    insert_position = match_set_target.regs[1][0]
                else:
                    # If set_target_properties is not found, raise an error
                    raise ValueError(f"set_target_properties statement not found.")

                # Insert function name into set_target_properties statement
                file_content = (file_content[:insert_position] + " " + sut_name + file_content[insert_position:])

    else:

        for test_name, test_statements in insert_contents.items():
            test_statement = test_statements[0]

            # Check if test exists
            add_pfunit_pattern = r"^ *add_pfunit_ctest *\( *" + test_name + r"[^\)]*\)$"
            match_add_pfunit = search(add_pfunit_pattern, file_content, IGNORECASE | MULTILINE | DOTALL)
            if match_add_pfunit:
                # Replace add_library statement
                file_content = sub(add_pfunit_pattern, test_statement, file_content, flags=IGNORECASE | MULTILINE | DOTALL)
            else:
                # Add test statement at the file end
                file_content = file_content + "\n" + test_statement

    return file_content


def remove_fortran_subroutine_or_function(fortran_code, names) -> str:
    # Define regex components
    whitespace = r'[ \t\r\f]*'
    decl_rest = r'[^\n]*\n'
    optional_attribute = r'(elemental|pure)?'  # Matches optional attributes
    function_or_subroutine = r'(function|subroutine)'  # Matches function or subroutine keywords

    # Create a regex pattern for the function/subroutine removal
    arguments = r'\(.*\)'  # Matches the argument list
    comment = r'(! <<Replace with (return expression|SUBROUTINE body) here>>)'  # Matches the specific comment
    code_lines = r'(.*?\n)*?'  # Matches any lines of code

    # Remove each specified function or subroutine
    for name in names:
        name_pattern = escape(name)  # Escape the name to safely include it in the regex
        end_statement = rf'{whitespace}end{whitespace}(function|subroutine){whitespace}{name_pattern}\s*$'  # Matches the end statement

        # Combine components into the full regex pattern
        pattern = (
            f'^{whitespace}{optional_attribute}{whitespace}{function_or_subroutine}{whitespace}{name_pattern}{whitespace}'
            f'{arguments}{whitespace}{decl_rest}'
            f'{code_lines}'
            f'{whitespace}{comment}{whitespace}{decl_rest}'
            f'{code_lines}'
            f'{end_statement}'
        )

        # Remove the specified function or subroutine from the Fortran code
        modified_code = sub(pattern, '', fortran_code, flags=MULTILINE | DOTALL | IGNORECASE)

        # Update the fortran_code for the next iteration
        fortran_code = modified_code

    # Clean public/private declarations
    public_pattern = r"(?:(\n *(public|private)(?: *\:\:)? *(.*?))\n)+"
    modified_code = sub(public_pattern, lambda m: clean_public_private(m.group(0), names), fortran_code, flags=MULTILINE | IGNORECASE)

    # TODO decide if to clean up any extra whitespace or empty lines?
    # modified_code = sub(r'\n\s*\n', '\n', modified_code)  # Remove empty lines
    return modified_code.strip()  # Return the modified code without leading/trailing whitespace


def clean_public_private(declaration, names) -> str:
    # Loop over each name to remove it from the declaration
    for name in names:
        name_pattern = escape(name)  # Escape the name to safely include it in the regex
        # This pattern matches the name and any preceding comma and optional whitespace
        removal_pattern = rf',?\s*{name_pattern}\s*(?=,|$)'
        declaration = sub(removal_pattern, '', declaration)

    # Remove any empty public/private declarations
    if search(r'public\s*::\s*$', declaration) or search(r'private\s*::\s*$', declaration):
        return ''  # Remove the entire line if it's empty after removal

    return declaration


def fortran_merge(insert_content: Dict[str, List[str]], file_content):
    """
    Insert operation into fortran code at the module end.

    :param insert_content: List of code to be merged
    :param file_content: File content in which to be merged
    :return: Merged content
    """
    for module_name, ops in insert_content.items():

        ops_names: str = ops[0]
        ops_impls: str = ops[1]

        if ops_names == "" or ops_impls == "":
            # Filter out empty operations
            continue

        remove_fortran_subroutine_or_function(file_content, ops_names)

        public_pattern = r"(?:(\n *public(?: *\:\:.*)?)\n)+"
        private_pattern = r"\n(( *)private(?: *\:\:.*)?\n)+"
        implicit_pattern = r"\n( *)implicit none *\n"

        module_start_pattern = r"(\n( *)module +" + module_name + " *\n?)"
        module_end_pattern = r"(\n( *)end +module +" + module_name + " *\n?)"

        # Find the position to insert the new code
        match_public = search(public_pattern, file_content, flags=IGNORECASE)
        match_private = search(private_pattern, file_content, flags=IGNORECASE)
        match_implicit = search(implicit_pattern, file_content, flags=IGNORECASE)
        match_module_start = search(module_start_pattern, file_content, flags=IGNORECASE)

        # Insert code accessible
        if match_public:
            # Insert after the "public" statement
            insert_position = match_public.end()
            line_insertion = match_public.regs[-1]
        elif match_private:
            # Insert after the "private" statement
            insert_position = match_private.end()
            line_insertion = match_private.regs[-1]
        elif match_implicit:
            # Insert after the "implicit" statement
            insert_position = match_implicit.end()
            line_insertion = match_implicit.regs[-1]
        elif match_module_start:
            # Insert after the module start
            insert_position = match_module_start.end()
            line_insertion = match_module_start.regs[-1]
        else:
            # If neither "contains" nor the function/subroutine is found, raise an error
            raise ValueError(f"Private/Public, Module or \"Implicit\" statement not found. Module: {module_name}")

        if match_public:
            # Add to last public statement
            file_content = (file_content[:line_insertion[1]] + f", {ops_names}" + "\n" + file_content[insert_position:])
        else:
            # Insert public statement with line insertion
            file_content = (file_content[:insert_position] + file_content[line_insertion[0]:line_insertion[1]] +
                            f"PUBLIC :: {ops_names}" + "\n" + file_content[insert_position:])

        match_module_end = search(module_end_pattern, file_content, flags=IGNORECASE)

        # Insert function code
        if match_module_end:
            # Insert before the module end
            insert_position = match_module_end.start()
            line_insertion = match_module_end.regs[-1]
        else:
            # If neither "contains" nor the module is found, raise an error
            raise ValueError(f"Module statement not found. Module: {module_name}")

        # Insert function code with line insertion
        file_content = (
            file_content[:insert_position] + "\n" + file_content[line_insertion[0]:line_insertion[1]] + ops_impls + "\n" + file_content[insert_position:])

    return file_content

def hash_file(path: str) -> str:
    """
    Hash file using MD5.

    :param path: System file path.
    :return: MD5 hash of the file as a hexadecimal string.
    """
    try:
        with open(path, "rb") as f:
            return md5(f.read()).hexdigest()
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")
    except IOError as e:
        raise ValueError(f"Error reading file {path}: {e}")



def file_modified(path=None, mtime: float = 0, fileHash: str = None) -> bool:
    """
    Check hash and modification time of file.

    :param path: system path to file
    :param mtime: last modification time
    :param fileHash: last md5 file hash
    :return: If modification time or file hash is changed
    """
    if getmtime(path) > mtime or fileHash != hash_file(path):
        logger.debug(f"... modified {path}")
        return True
    else:
        logger.debug(f"... not modified {path}")
        return False


def write_file(file_path: str = "", content: str | Dict = "", file_attr: tuple[float, str, str] = None, insert: bool = False) -> Tuple[float, str, str]:
    """
    Write/merge pFUnit-file under :test_path:/:test_folder:/:filename:.pf for test-case.
    Merges file if it exists using difflib.

    :param file_path: system path to file
    :param content: test-case content
    :param file_attr: file attributes such as file hash and modification time
    :param insert: flag if content should be merged or overwritten
    :return: hast and modification time of file
    """

    # Define the folder and filename. Current working directory is ignored for absolut test_path
    path = dirname(file_path)

    # Create folder if it doesn't exist
    if path and not isdir(path):
        makedirs(path)
        if show_debug_output and logger.isEnabledFor(DEBUG):
            logger.debug(f"... create {path}")

    # Get File extension for merge functions
    extension: str = splitext(file_path)[1]

    # Create file if it doesn't exist else merge with existing file
    if exists(file_path):
        # Check if file is known or was modified
        if file_attr is None or file_modified(file_path, file_attr[0], file_attr[1]):
            # Reload file from disk if it is unknown or modified
            with open(file_path, mode="r", encoding="utf-8") as f:
                content_org = f.read()
        else:
            # Keep original file content
            content_org = file_attr[2]

        # Log
        if show_debug_output and logger.isEnabledFor(DEBUG):
            logger.debug(f"...try merge {file_path}")

        # Merge current content with original file content based on file extension
        match extension:
            case ".f90":
                # Insert operation at the module end
                content = fortran_merge(content, content_org) if insert else content
            case ".pf":
                # Difflib merge of file
                content = difflib_merge(content, content_org) if insert else content
            case ".txt":
                content = cmake_merge(content, content_org) if insert else content
            case _:
                pass

    else:
        #
        # Save content of new file for later merge
        match extension:
            case ".f90":
                # Keep new content for later insert merge
                content_org = content
            case ".pf":
                # Set emtpy original content for later difflib merge of file
                content_org = ""
            case ".txt":
                # Keep new content for later insert merge
                content_org = content
            case _:
                pass

    # Write rendered and optional merged content to file
    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write(content)
        if show_debug_output and logger.isEnabledFor(DEBUG):
            logger.debug(f"... write {file_path}")

    return getmtime(file_path), hash_file(file_path), content_org
