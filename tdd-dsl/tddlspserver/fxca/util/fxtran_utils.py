"""Utils for the Fxtran parser"""

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

import fnmatch
import logging
import os
import pathlib
import subprocess

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

from symboltable.symbol_table import ModuleSymbol

logger = logging.getLogger(__name__)


@dataclass
class PublicObj:
    """
    Test Case for a Unit-test
    """

    # Require public entities
    need_public: bool = False
    # By default, entities are public unless general private statement
    default_private: bool = False
    # Entities specifically mentioned as public optionally with attributes
    pub_elements: Dict[str, List[str]] = field(default_factory=dict)
    # Entities specifically mentioned as private optionally with attributes
    pr_elements: Dict[str, List[str]] = field(default_factory=dict)

    def is_public(self, name: str) -> bool:
        # Entity is considered public if public is not needed or entities are
        # public by default and entity is not specifically marked as private (also
        # not in a private context) or entity is specifically marked as public
        if not self.need_public or not self.default_private and not name.startswith(tuple(self.pr_elements.keys())) or name in self.pub_elements:
            return True
        else:
            return False


# Set the namespace as Fxtran for XPath expressions
ns = {"fx": "http://fxtran.net/#syntax"}
autogenerated_comments: Set = {"! <<Add return expression here>>", "! <<Add SUBROUTINE body here>>"}


def filter_xml(
        xml_path: str = "", need_public: bool = False, modules: List[ModuleSymbol] = []) -> Tuple[List[Tuple[str]], List[Tuple[str, str, List[str]]]]:
    """
    XML filter for Fxtran output files (http://fxtran.net/#syntax) using XPath expressions
    """

    # Extract names of module symbols for scope filter
    module_names = list(map(lambda s: s.name, modules))
    # Extract filename of original file
    base_name = os.path.splitext(os.path.basename(xml_path))[0]
    base_module: ModuleSymbol = None

    # Get the root element
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Are filtered modules in scope
    is_filtered_scope: bool = False

    # Variables to return (EN-decl elements within T-decl-stmt elements)
    variables: List = []
    # Scopes to return
    scopes = []
    # Stack to track the current scope
    scope_stack = []
    # Variables defined in scope
    scope_stack_var: Dict[str, Dict[str, str]] = {}
    pub_element: PublicObj = PublicObj(need_public=need_public)  # Elements declared as public

    # Last defined value
    last_variable_type: str = ""
    is_generated_scope: bool = False

    # Dynamically extracted scope-changing elements
    dyn_scope_elements = set()
    dyn_end_scope_elements = set()

    # Special element tags
    end_function_stmt_elements: Set = {"end-function-stmt", "end-subroutine-stmt"}

    # Iterate over all elements in the XML tree
    for element in root.iter():

        # Check if element is scope-changing by searching for scope-ending element
        # Extract the tag name without the namespace
        tag = element.tag.rsplit("}", 1)[-1]

        if tag.endswith("-stmt"):
            # Extract the statement name
            stmt_name = tag.rsplit("-", 1)[0]
            # Find scope name element
            name_element = element.find(f".//fx:{stmt_name}-N", ns)

            if tag not in dyn_scope_elements and name_element is not None:
                end_tag = "end-" + tag
                if root.find(f".//fx:{end_tag}", ns) is not None:
                    dyn_scope_elements.add(tag)
                    dyn_end_scope_elements.add(end_tag)

        # Reduce the scope stack when leaving scopes
        if tag in tuple(dyn_end_scope_elements):
            # Update generic status and return type for functions

            if tag in tuple(end_function_stmt_elements):
                current_scope = ".".join(scope_stack)
                for scope in reversed(scopes):
                    if ".".join([scope[4], scope[1]]) == current_scope:
                        if is_generated_scope:
                            # Save generic flag
                            scope[5] = is_generated_scope
                            # Reset generic flag
                            is_generated_scope = False

                        if is_filtered_scope and pub_element.is_public(current_scope):

                            # Update return name of first functions without result statement

                            # Get return name
                            result_type = scope_stack_var.get(current_scope).get("-1")
                            # Set return type for current scope
                            result_type = last_variable_type if result_type == -1 else result_type
                            scope[3] = result_type
                    break

            scope_stack.pop()

            # Check scope is filtered and top level scope ended
            if not scope_stack:
                is_filtered_scope = False

        # Extend the scope stack when entering scopes
        elif tag in tuple(dyn_scope_elements):
            # Extract scope name
            scope_name = name_element.find(".//fx:n", ns).text

            new_top_level_module: bool = False
            if stmt_name == "module":
                # Add top level modules to content assist
                if not scope_stack:
                    new_top_level_module: bool = True
                    # Set top level modules in filtered scope as base module
                    if scope_name in module_names:
                        is_filtered_scope = True
                        module: ModuleSymbol = next(filter(lambda module: module.name == scope_name, modules))

                        # Get filename of original file
                        module.file = base_name

                        base_module = module

            # Set result_id for dereference in all stacks
            result_id = None

            # Check scope is filtered and is in filtered scope
            if is_filtered_scope or new_top_level_module:
                # Extract arguments
                argument_names = []
                for itm in element.findall(".//fx:arg-N", ns):
                    argument_names.append(itm.find(".//fx:n", ns).text)

                # Get the current scope from the scope stack
                current_scope = ".".join(scope_stack)

                # Extract resultId for functions
                if element.tag.endswith("function-stmt"):
                    result_element = element.find(".//fx:result-spec", ns)
                    if result_element is not None:
                        result_id = result_element.find(".//fx:n", ns).text
                    else:
                        result_id = -1

                # Add type, name and arguments to returning scopes
                # Check public availability
                scope_id = ".".join([current_scope, scope_name]) if current_scope else scope_name
                if pub_element.is_public(scope_id) and scope_name not in module_names:
                    scopes.append([stmt_name, scope_name, argument_names, result_id, current_scope, is_generated_scope])

            # Update scope stack
            scope_stack.append(scope_name)

            # Update scope stack variables for dereference in all stacks
            scope_stack_var[".".join(scope_stack)] = {"-1": result_id} if result_id else {}

        # Store assignment statements for optional return values of functions
        elif tag == "a-stmt":
            # Check scope is filtered and is in filtered scope
            if is_filtered_scope:
                # Get current variable name
                variable_name = element.find(".//fx:n", ns).text

                # Get the current scope from the scope stack
                current_scope = ".".join(scope_stack)

                # Type for return type of functions, None if not found
                last_variable_type = scope_stack_var.get(current_scope).get(variable_name, None)

        # Check comment for autogenerated elements by comments inside the operation
        elif tag == "C":
            if any(autogenerated_comment in element.text for autogenerated_comment in autogenerated_comments):
                # Set generic flag
                is_generated_scope = True

        # Store public available ids
        elif tag == "public-stmt":
            current_scope = ".".join(scope_stack)
            pub_ids = list(map((lambda itm: itm.text), element.findall(".//fx:n", ns)))
            for item in pub_ids:
                item_id = ".".join([current_scope, item])
                pub_element.pub_elements[item_id] = pub_element.pub_elements.get(item_id, [])

        # Store private available ids
        elif tag == "private-stmt":
            pr_ids = list(map((lambda itm: itm.text), element.findall(".//fx:n", ns)))

            # Elements are private by default if no variable is given. Else extract private elements.
            if not pr_ids:
                pub_element.default_private = True
            else:
                for item in pr_ids:
                    item_id = ".".join([current_scope, item])
                    pub_element.pr_elements[item_id] = pub_element.pr_elements.get(item_id, [])

        # Extract variables, public only, if needed
        elif tag == "contains-stmt":
            # Check if top level scope is in filtered scope or if filtered scope is empty
            if is_filtered_scope and len(scope_stack) == 1 and scope_stack[0] == base_module.name:
                base_module.contains_function = True

        # Extract variables, public only, if needed
        elif tag == "T-decl-stmt":

            # Check scope is filtered and is in filtered scope
            if is_filtered_scope:
                # Get element attributes for public filter
                attributes = list(map(lambda itm: itm.text, element.findall(".//fx:attribute-N", ns)))

                # Get the current scope from the scope stack
                current_scope = ".".join(scope_stack)

                # Get the type of the variable if it exists
                t_spec_element = element.find(".//fx:T-N", ns)

                # Extract variable type
                if t_spec_element is not None:
                    if t_spec_element[0].text:
                        # Direct type name
                        variable_type = t_spec_element[0].text
                    else:
                        derived_element: ET.Element = element.find(".//fx:derived-T-spec", ns)
                        if derived_element is not None:
                            derived_type: str = derived_element.text
                            type_name_element: ET.Element = t_spec_element[0].find(".//fx:n", ns)
                            if type_name_element is not None and derived_type is not None:
                                # Derived selector type name
                                variable_type = "".join([derived_type, "(", type_name_element.text, ")"])
                            elif type_name_element is not None:
                                # Derived Selector type name
                                variable_type = type_name_element.text if type_name_element.text else ""
                            elif derived_type is not None:
                                # Derived type name
                                variable_type = derived_type
                            else:
                                # No type found
                                variable_type = ""
                        else:
                            intrinsic_element: ET.Element = element.find(".//fx:intrinsic-T-spec", ns)
                            if intrinsic_element is not None:
                                intrinsic_element_type = intrinsic_element[0].find(".//fx:c", ns)
                                intrinsic_type: str = intrinsic_element_type.text
                                type_name_element: ET.Element = intrinsic_element[0].find(".//fx:n", ns)
                                if type_name_element is not None and intrinsic_element_type is not None:
                                    # Intrinsic selector type name
                                    variable_type = "".join([intrinsic_type, "(", type_name_element.text, ")"])
                                elif type_name_element is not None:
                                    # Intrinsic Selector type name
                                    variable_type = type_name_element.text if type_name_element.text else ""
                                elif intrinsic_type is not None:
                                    # Intrinsic type name
                                    variable_type = intrinsic_type
                                else:
                                    # No type found
                                    variable_type = ""
                            else:
                                # No type found
                                variable_type = ""
                else:
                    # No type found
                    variable_type = ""

                for en_decl in element.findall(".//fx:EN-decl", ns):
                    # Get the name of the variable from the named element
                    variable_name = en_decl.find(".//fx:n", ns).text

                    # Add element to public object if Public attribute is found or extend attributes if element is already public
                    variable_id = ".".join([current_scope, variable_name])
                    if "PUBLIC" in attributes:
                        pub_element.pub_elements[variable_id] = pub_element.pub_elements.get(variable_id, [])

                    # Save name for return type of functions
                    variable = (variable_name, variable_type, current_scope)

                    # Add variable with type to current scope
                    scope_stack_var.get(current_scope)[variable_name] = variable_type

                    # Update return type of current scope
                    if scope_stack_var.get(current_scope).get("-1") == variable_name:
                        scope_stack_var.get(current_scope)["-1"] = variable_type

                    # Check public availability or variable is return variable of current scope
                    if pub_element.is_public(variable_id):
                        # Save the variable names with their respective types and scopes
                        variables.append(variable)

    return variables, scopes


def get_files(path: str = "", pattern: str = "*.[fF]90"):
    """
    return files from directory and subdirectories matching a pattern
    :param path: path to directory
    :param pattern: pattern of files to return
    :return: pattern matching files in directory and subdirectories
    """
    files = []
    for root, dir_names, file_names in os.walk(path):
        for file_name in fnmatch.filter(file_names, pattern):
            files.append((root, file_name))

    return files


def get_subdirectories(path: str = "", recursive: bool = False, follow_symlinks: bool = False):
    """
    Returns subdirectory names not starting with "." under given path.

    :param path: root path
    :param recursive: return subdirectories recursively
    :param follow_symlinks: follow symlinks
    :return: subdirectories
    """
    sub_dirs: List[str] = [entry.path for entry in os.scandir(path) if not entry.name.startswith(".") and entry.is_dir(follow_symlinks=follow_symlinks)]
    if recursive:
        for path in sub_dirs:
            sub_dirs.extend(get_subdirectories(path))
    return sub_dirs


def get_subdirectories_gen(path: str = "", recursive: bool = False, follow_symlinks: bool = False):
    """
    Yield subdirectory names not starting with "." under given path. Does not follow symlinks.

    :param path: root path
    :param recursive: yield subdirectories recursively
    :param follow_symlinks: follow symlinks
    :return: yielded subdirectories
    """
    for entry in os.scandir(path):
        if not entry.name.startswith(".") and entry.is_dir(follow_symlinks=follow_symlinks):
            yield entry
            if recursive:
                yield from get_subdirectories_gen(entry.path, recursive)


def write_decorate_src_xml(src_dir: str = "", out_dir: str = "out", fxtran_path: str = "~/bin/fxtran"):
    """
    run Fxtran decorating source code with XML tags

    :param src_dir: input source code path
    :param out_dir: output xml path
    :param fxtran_path: fxtran binary path
    :return:
    """

    # Define the fxtran command
    fxtran_cmd_ops = " ".join(
        [fxtran_path,  # "-line-length 200",
         "-no-cpp", "-name-attr", "-code-tag",  # "-strip-comments",
         # "-no-include",
         # "-construct-tag",
         "-o"]
    )

    # Get Fortran files
    fortran_files = get_files(src_dir, "*.[fF]90")

    for filepath, filename in fortran_files:

        try:
            # Create output directory relative to source directory if it doesn't exist
            rel_path = os.path.relpath(filepath, src_dir)
            rel_out_dir = os.path.join(out_dir, rel_path) if rel_path != "." else out_dir
            pathlib.Path(rel_out_dir).mkdir(mode=0o750, parents=True, exist_ok=True)
        except PermissionError as e:
            raise RuntimeError(f"Permission denied for output directory \"{out_dir}\". Error (code {e.errno}): {e.strerror} \"{e.filename}\"")

        # Build output path for xml file
        out_file_path = os.path.join(rel_out_dir, filename + ".xml")
        # Build the fxtran command
        fxtran_cmd = " ".join([fxtran_cmd_ops, out_file_path, filename])

        try:
            # Call fxtran via subprocess with filepath as working directory
            subprocess.check_output(fxtran_cmd, shell=True, stderr=subprocess.STDOUT, cwd=filepath)
        except subprocess.CalledProcessError as e:
            logger.warning(f"command \"{e.cmd}\" return with error (code {e.returncode}): {e.output}")
        except PermissionError as e:
            raise RuntimeError(f"Permission denied for calling fxtran parser \"{fxtran_path}\". Error (code {e.errno}): {e.strerror} \"{e.filename}\"")
