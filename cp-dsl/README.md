# CP-DSL - Parameter Declaration and Configuration DSL

The CP-DSL allows to declare parameter and features for the configuration of
the build and setup of models.

This documentation shows how to setup VSCode, Vi and Emacs with the LSP
service.

## Prerequisites

You need `python3` installed and, in case your python installation is managed
by the distribution installer, you need a virtual environment.

For VSCode, you also need `npm` installed

See main README.md for details.

## Installation

You can either install additional python packages in your system using pip or
use a virtual evnironment to ensure the system installation is not modified.

Instructions are in the main README.md

After installing the dependencies and setting up the virutal environment,
go to the extension directory `python-oceandsls/cp-dsl`

## Install and setup VSCode

Install VScode in Ubuntu:

`$ sudo apt install code`

### Install Python extensions in VSCode

Start VScode by typing:

`$ code`

![vscode start screen](images/vscode-start-screen.png)

You can no choose a theme, if you like.

Click on *extensions*. This is the icon on the left made out of squares. If
unsure hover with the mouse over the icons on the left until you find extensions.

Search for the Python plugin as depicted in the screenshot below.
You can either browse the list or type the name in the search field at the top.

![vscode install python](images/vscode-install-python.png)

### Include LSPs in VSCode

Include the Declaration DSL in VSCode

Open `python-oceandsls/cp-dsl/dcllspserver` in VSCode

Type 

`$ code python-oceandsls/cp-dsl`

or, in case your vscode is still open, go to File > Open Folder and choose
`python-oceandsls/cp-dsl`

Trust author files in `python-oceandsls/cp-dsl`

gNow open `python-oceandsls/cp-dsl/dcllspserver` with File > Open Folder

Goto *Run and Debug* (press `Ctrl/Cmd+Shift+D`)

Select *Server + Client*

Start Debugging via `F5` or GUI

This opens a new VSCode instance with support for the Declaration DSL.

Open a `*.dcl` file

If server is working correctly notification shows `Text Document Did Open`


Open `python-oceandsls/cp-dsl/conflspserver` in VSCode

Follow the same steps as above, but for `*.conf` files and conflspserver

### Troubleshooting

- If VS Code doesn`t automatically locate the interpreter of the virtual environment. [Set it manually](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter)
  - Open Command prompt
  `Ctrl/Cmd+Shift+P`
    - Run select interpreter command
  `Python: Select Interpreter`
  - Alternative create `.vscode/settings.json` file in `python-oceandsls/cp-dsl` directory and set `python.defaultInterpreterPath` to point to the virtual environment
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

## Setup Vi

# Setup Emacs

# Compile and generate code

## Using console compiler
- open a terminal and type `python -m cp-dsl -f <path-to-oconf-file>`
- there are two different file generator available atm
  - mitgcm: to generate for mitgcm, use flag `-m`
  - uvic: to generate for uvic, use flag `-u`
- the compiler writes the generated files in the `gen` folder in your cwd
  - with flag `-o <path-to-your-output-folder>` it is possible to define a sepcific output folder
- IMPORTANT: make sure the `.decl` file for your `.oconf` file is in the same directory (different pathes are not yet supported)

the compiler can throw different errors and warnings while compiling the files:
- Warnings are only a info for the user, i.e. to inform the user that in the declaration a parameter has no default value
- Errors are mostly thrown by pythons `AttributeError` or by array index errors so make sure you dont use a operator between a string and a integer

## Using language-server
not yet supported

# Change or add templates

## Change a template (uvic, mitgcm):
- go to folder `/confLSPServer/fileWriter/jinja-templates`
- edit the files as you wish, the templates are named as the files they generate added by a `.template`

## Add a template
- go to folder `/confLSPServer/fileWriter/jinja-templates`
  - create your templates using [jinja-template-language](https://jinja.palletsprojects.com/en/3.1.x/)
  - example for a instance splitter:
    ```jinja
    {% macro typeDeciderTemplate(elem, lastSymbol) -%}
    {% if isinstance(elem, featureSymbol) -%}
        {{ featureTemplate(elem) }}
    {%- elif isinstance(elem, groupSymbol) -%}
        {{ groupTemplate(elem) }}
    {%- elif isinstance(elem, enumSymbol) -%}
    {%- else -%}
        {{parameterTemplate(elem, lastSymbol)}}
    {%- endif %}
    {%- endmacro -%}
    ```
- create a code-generator
  - navigate to `/confLSPServer/fileWriter/`
  - open `CodeGenerator.py` you will find a superclass for a code generator:
    ```python
    class StandartCodeGenerator():
    """
    a simple code generator representing a simple structrue and helpful functions
    """
      def __init__(self, symbolTable : SymbolTable, outputPath : str, templatePath = "") -> None:
          self._symbolTable : SymbolTable = symbolTable
          self.outputPath = outputPath
          if not templatePath == "":
              self.templateLoader = j.PackageLoader(str(self.__module__), templatePath)
              self.templateEnv = j.Environment(loader=self.templateLoader)
          
      def writeFile(self, content : str, filename : str):
          """method to write content to a file inside the output folder

          Args:
              content (str): string to write into the file
              filename (str): filename specified
          """
          path = os.path.join(self.outputPath, filename)
          f = open(path, "w")
          f.write(content)
          f.close()
      
      def generate(self) -> None:
          """generate method that uses jinja templates to write files into output path
          """
          print("GIVE THE GENERATOR A TEMPLATE AND DATA TO WORK WITH")
    ```
  - use this superclass to create a generator
  - add the option to compile to this generator in the main method
    - `parser.add_argument("<your_flag>", action="store_true", dest=<your_language>)`
  - check for the argument:
    ```python
    if args.your_language:
      generator = yourCodeGenerator(table, outputPath)
      generator.generate()
    ```
