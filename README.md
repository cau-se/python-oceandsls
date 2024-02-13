# OceanDSL Python-based DSL Implementation

## Name

oceandsl-languages

## Description

This project contains multiple DSLs for ocean and earth system models.

- CP-DSL including Declaration-DSL, Configuration-DSL and Template-DSL
- TDD-DSL testing DSL for test-driven development
- BGC-DSL language to specify biogeochemical models

Documentation including the languages and architecture can be found in the `doc`.

## License

Apache 2.0

## Install

### Install Python

The OceanDSL languages are based on python3.
Install PYthon in Ubuntu with:
- `sudo apt install python3 python3-pip`

In some distributions *python3* uses the executable name *python3* leaving
python for *python2*. As the following instructions use *python*, you have
either substitute the names accordingly or in Ubuntu install the following
packages:

- `sudo apt install python-is-python3`

Install the virtual environment. This helps to keep your distribution
Python setup and the setup for the DSLs separate.

- `sudo apt install python3-virtualenv`

Alternatively, you can install the packages via *pip*. Howver, this does
not work in Ubuntu, as it manages its packages via apt/dpkg.
- `python -m pip install --upgrade pip setuptools wheel`

Check whether *virtualenv* is installed:

- `python -m pip show virtualenv`

If missing install it:

- `python -m pip install virtualenv`

### Install LSP Server Dependencies

For this how to, we assume that you install your virtual environment in your
home directory. You can, however, install it anywhere.

Generate virtual environment in directory `.venv` using the standard
library `venv`:

- `cd $HOME`
- `python -m venv .venv`

Or use `virtualenv`:
- `virtualenv`

Activate virtual environment `.venv`
- `source .venv/bin/activate`

install `antlr4-python3-runtime`, `Jinja2`, `mock`, `pygls` and `pytest`
package into virtual environment `.venv`
- `python -m pip install antlr4-python3-runtime Jinja2 mock pygls pytest`


## Optional: update npm and node

Install and update JavaScript package manager which is used by VSCode.
- `sudo apt install npm`

Check `npm` version
- `npm --version`

In case the package is not up-to-date, install latest `npm` version globally
(`-g` or `--global`)
- `sudo npm install -g npm@latest`

Install latest `node` version
- `sudo n latest`

Install the dependencies to the global mode (`-g` or `--global`)
- `sudo npm update -g`


