# CP-DSL - Parameter Declaration and Configuration DSL

## Name

cp-dsl

## Description

The CP-DSL allows to declare parameter and features for the configuration of
the build and setup of models.

This documentation shows how to setup VSCode, Vi and Emacs with the LSP
service.

## License

Apache 2.0

## Prerequisites

You need `python3` installed and, in case your python installation is managed by the distribution installer, you
need a virtual environment.

For VSCode, you also need `npm`, `node` and `VSCode` installed.

In Ubuntu you can install `virtualenv` with
- `sudo apt install python3-virtualenv`

Alternatively, you can install it via pip
- `python -m pip install virtualenv`

## Installation

You can either install additional python packages in your system using pip or use a virtual evnironment to
ensure the system installation is not modified.

### Create virtual environment

- Open a terminal and ensure you are in the home folder `cd`
- Run `virtualenv local` local is then the name of your virtual environment
- Activate virtual environment
  `source local/bin/activate`
  This will change your command line prompt to `(local) username@hostname:~$`

### Include LSPs in VSCode

We first install the LSP for the Declaration DSL.
Therefore, open `python-oceandsls/cp-dsl` in VSCode

Type 

`code python-oceandsls/cp-dsl`

or, in case your vscode is still open, go to **File** > **Open Folder** and
choose `python-oceandsls/cp-dsl`

Trust author files in `python-oceandsls/cp-dsl`

Goto **Run and Debug** (press **Ctrl/Cmd+Shift+D**)

Select *DCL Server + Client*

Start Debugging via **F5**

This opens a new VSCode instance with support for the Declaration DSL.

![vscode install python](images/vscode-open-declaration-file.png)

Open a `*.decl` file in one of the example projects `MITgcm`, `testing`, or 
`UVic`.

If server is working correctly, a notification is shown with the text
**Text Document Did Open**.

You can now edit the declaration file.

For the **Configuration DSL** you can perform the same steps after opening
VSCode.

Goto **Run and Debug** (press **Ctrl/Cmd+Shift+D**)

Select *CONF Server + Client*

Start Debugging via **F5**

This opens a new VSCode instance with support for the Configuration DSL.

# Troubleshooting

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

# Generate configuration files

The main idea behind CP-DSL is the ability to generate specific configuration
files for a model, but keep all settings in a easy to read format. To generate
the files for a respective model, you need therefore a generator to translate
CP-DSL configuration files into specific files, e.g., namelists, header files,
and model specific setting files. 

## Using console generator

The console generator can be used on command line or in build scripts. For
this readme, we run it on command line.

We assume, you unpacked `python-oceandsls` in your root directory.

Open a terminal and type:

`cp $HOME/python-oceandsls`

And run the generator as follows.

`python -m cp-dsl [-u|-m] -f <path-to-oconf-file>`

We provide 2 different models to test and experiment with, which can be found in
`python-oceandsls/cp-dsl/input`:
- mitgcm: to generate for mitgcm, use flag `-m`
- uvic: to generate for uvic, use flag `-u`

The compiler writes the generated files in the `gen` folder in your current
folder. With flag `-o <path-to-your-output-folder>` it is possible to define a
sepcific output folder.
**IMPORTANT:** make sure the `.decl` file for your `.oconf` file is in the same
directory (different pathes are not yet supported).

The compiler can throw different errors and warnings while compiling the files:
- Warnings are only a info for the user, i.e. to inform the user that in the
  declaration a parameter has no default value.
- Errors are mostly thrown by pythons `AttributeError` or by array index errors
  so make sure you dont use a operator between a string and a integer.

To try it out, we generate files for UVic with:

`python -m cp-dsl -u -f input/UVic/configuration.oconf`

The results will appear in `input/UVic/gen`

## Using language-server
not yet supported

# Change or add templates

It is possible to adjuct the output generated by the compiler. 

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
