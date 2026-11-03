# odsllib

Shared library of the [OceanDSL](https://oceandsl.uni-kiel.de) languages
(CP-DSL, TDD-DSL, BGC-DSL). It contains:

- `odsllib.code_completion_core` – a Python port of
  [antlr4-c3](https://github.com/mike-lischke/antlr4-c3), which computes code completion
  candidates (tokens and rules) from an ANTLR4 parser's ATN.
- `odsllib.symbol_table` – a Python port of the antlr4-c3 symbol table (scopes, typed and unit
  symbols, routines, fundamental types and units); the DSLs add their own symbols as subclasses.
- `odsllib.lsp` – language server infrastructure built on
  [pygls](https://github.com/openlawlibrary/pygls):
  - `parse_source()` parses a document with a fresh lexer/parser and returns syntax diagnostics
    (including input left over after the start rule),
  - `DiagnosticListener`, `InputMismatchErrorStrategy`,
  - caret/token mapping (`find_caret_token()`, `compute_caret_token_position()`),
  - keyword completion (`collect_candidates()`, `keyword_items()`),
  - token-based semantic highlighting (`encode_semantic_tokens()`),
  - `AntlrLanguageServer`, a base server providing diagnostics, completion, semantic tokens
    and the `registerCompletions`/`unregisterCompletions` commands,
  - symbol completion from a symbol table (`odsllib.lsp.symbols.suggest_symbols()`),
  - the common command line of the servers (`odsllib.lsp.cli.server_argument_parser()`,
    `run_server()`: --tcp, --ws, --host, --port, -f/--file, --log-file, --debug),
  - `odsllib.lsp.testing.run_lsp_session()` to test a server process end-to-end over stdio.

## Install

```
pip install odsllib
```

## Usage

```python
from odsllib.lsp.server import AntlrLanguageServer
from mydsl.gen.MyDslLexer import MyDslLexer
from mydsl.gen.MyDslParser import MyDslParser


class MyDslServer(AntlrLanguageServer):
    lexer_class = MyDslLexer
    parser_class = MyDslParser
    start_rule = "model"
    preferred_rules = {MyDslParser.RULE_reference}

    def symbol_completions(self, result, position, candidates, uri):
        ...  # return CompletionItems for preferred rule candidates


MyDslServer("my-dsl", "1.0").start_io()
```

The old import location `codeCompletionCore.CodeCompletionCore` (odsllib <= 0.38) still works
but is deprecated.

## Development

```
pip install -e ".[test]"
pytest
```

The test grammar in `tests/grammars` is generated with ANTLR 4.13.1 into `tests/gen`.

## License

Apache 2.0
