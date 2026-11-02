# TDD-DSL

TDD-DSL facilitates test-driven development (TDD) of Fortran 90+ research software with the unit testing
framework [pFUnit 4](https://github.com/Goddard-Fortran-Ecosystem/pFUnit). Test suites are written in a
YAML-like DSL; the tooling generates the pFUnit files, CMake setup and templates for the system under test
(SUT). See S. Gundlach, R. Jung and W. Hasselbring: *Facilitating Test-Driven Development via
Domain-Specific Languages in Computational Science Software Engineering*.

```
suite test_suite:
test test_fT_ME:
    overwrite: pf, cmake
    srcpath: 'src'
    modules:
        cfo_example
    var:
        dp: integer, PARAMETER = KIND(0D0)
        xIntercept: real(dp) = 283D0 / 19D0
    assert Equal:
        in:
            fT_ME(xIntercept), K
        out:
            0D0, K
        tolerance: 1D-12
```

## Installation

```
pip install TDD-Language
```

This installs the `tdd_dsl` command and the shared library `odsllib`. To include symbols of the SUT in
content assist and generation, install the Fortran parser [fxtran](https://github.com/pmarguinaud/fxtran)
and put it on the `PATH` (or pass `-fx PATH`). Without fxtran, the server still works but only knows the
symbols defined in the test specification.

## Usage

- Language server over stdio (default), TCP or WebSocket: `tdd_dsl`, `tdd_dsl --tcp --port 2087`, `tdd_dsl --ws`
- Generate pFUnit/CMake/Fortran files without an editor: `tdd_dsl -f suite.tdd`
- Recommend SUTs to test based on complexity metrics: `tdd_dsl -s path/to/src -m "Test Index"`

The language server provides syntax and consistency diagnostics, content assist (keywords, test variables,
SUT variables/functions/routines, modules, source paths), semantic highlighting and generates the test
files whenever a `.tdd` file is saved. Paths in `srcpath` are relative to the server's working directory.

## Development

```
pip install -e ../antlrLib -e ".[test]"
pytest
```

The parser in `tddlspserver/gen` is generated from `tddlspserver/grammars/TestSuite.g4` with ANTLR 4.13.1
(`make TestSuite` in the repository root).

---

# Development environment

## Install ANTlR4 for development
- https://www.antlr.org/download.html
- https://www.antlr3.org/works/
- move to /usr/local/lib
- update CLASSPATH (source.sh)
- require java versions up to 55.0 (JDK Version Java 11 Bytecode Version 55.0)
    - sudo apt-get install openjdk-11-jre openjdk-11-jdk openjdk-11-demo openjdk-11-doc openjdk-11-jre-headless openjdk-11-source
    - sudo update-alternatives --config javac

## Add pFUnit4
- sudo apt-get install cmake
- sudo apt install gfortran
- sudo apt install m4
# Example installation of pFUnit and pFUnit_demos — Software testing documentation
- https://coderefinery.github.io/testing/code/fortran/build_pFUnit/#on-own-computer
     - export FC=/usr/bin/gfortran
     - export PFUNIT_DIR=/usr/local/PFUNIT-4.7

## Optional: check python packages

- update package manager tools
    - `python -m pip install --upgrade pip setuptools wheel`
- check if python package `virtualenv` is installed if Python < 3.3 is used else a subset of it has been integrated into the standard library under `venv`
    - `python -m pip show virtualenv`
    - if not install package `virtualenv` into global system environment
        - `python -m pip install virtualenv`

## Install Server Dependencies

- generate virtual environment in directory `.venv` using the standard library `venv`
    - `python -m venv .venv`
    - alternative use `virtualenv`, see optional python packages
- activate virtual environment `.venv`
    - `source .venv/bin/activate`
- install `antlr4-python3-runtime`, `Jinja2`, `pygls`, `pytest`, `pylint` and `autopep8` package into virtual environment `.venv`
    - `python -m pip install antlr4-python3-runtime Jinja2 pygls pytest pylint autopep8`

## Optional: update npm and node

- check `npm` version
    - `npm --version`
- install `npm` and `node` if necessary 
    - `sudo apt-get install npm nodejs`
- install the Node manager via `npm`
    `sudo npm install -g n`
- install latest `node` version
    - `sudo n latest`
- install latest `npm` version globally (`-g` or `--global`)
    - `sudo npm install -g npm@latest`
- Install the dependencies to the global mode (`-g` or `--global`)
    - `sudo npm update -g`

## Install Client Dependencies

- Goto extension directory `python-oceandsls/tdd-dsl`
- Install the dependencies to the local node_modules
    - `npm install`

## Run Example using VSCode

- Open `python-oceandsls/tdd-dsl` in VSCode
- Trust author files in `python-oceandsls/tdd-dsl`
- Goto Run and Debug
    - `Ctrl/Cmd+Shift+D`
- Select `Server + Client`
- Start Debugging via `F5` or GUI
- Open a `*.tdd` file
- If server is working correctly notification shows `Text Document Did Open`

## Troubleshooting

- If VS Code doesn`t automatically locate the interpreter of the virtual environment. [Set it manually](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter)
    - Open Command prompt
      `Ctrl/Cmd+Shift+P`
        - Run select interpreter command
          `Python: Select Interpreter`
    - Alternative create `.vscode/settings.json` file in `python-oceandsls/tdd-dsl` directory and set `python.defaultInterpreterPath` to point to the virtual environment
        - settings.json

              {
                  // set Python Interpreter relative to workspaceFolder to virtual environment '.venv'
                  "python.defaultInterpreterPath": "${workspaceFolder}/../.venv/bin/python",
                  // alternative
                  //"python.defaultInterpreterPath": "../.venv",
                  // deprecated
                  // "python.pythonPath": "${workspaceFolder}/../.venv/bin/python",

                  // Pylance VSCode code analysis and auto-completion using Python 3.10
                  "python.analysis.extraPaths": [
                      "{workspaceFolder}/../.venv/lib/python3.10/site-packages/:${workspaceFolder}/../antlrLib/"
                  ],


                  // Object with environment variables that will be added to the VS Code process to be used by the terminal on OS X
                  "terminal.integrated.env.osx": {"PYTHONPATH": "${workspaceFolder}/.."},

                  // Object with environment variables that will be added to the VS Code process to be used by the terminal on Linux
                  "terminal.integrated.env.linux": {"PYTHONPATH": "${workspaceFolder}/.."},

                  // Object with environment variables that will be added to the VS Code process to be used by the terminal on Windows
                  "terminal.integrated.env.windows": {"PYTHONPATH": "${workspaceFolder}/.."},
              }

- If npm version conflicts exists change npm to the required version
    - E.g. reset npm version to 9.2.0
        - `sudo npm install -g npm@9.2.0`