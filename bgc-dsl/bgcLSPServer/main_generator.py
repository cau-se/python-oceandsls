if __name__ == '__main__':
    # main()
    import sys
    sys.path.append("..")
    from gen.python.BgcDsl.BgcDslLexer import BgcDslLexer
    from gen.python.BgcDsl.BgcDslParser import BgcDslParser
    from antlr4 import InputStream, CommonTokenStream
    from symbolTable.SymbolTable import VariableSymbol
    from cst.SymbolTableVisitor import SymbolTableVisitor
    from fileWriter.Generator import BgcCodeGenerator

    tableVisitor = SymbolTableVisitor("testConf")


def generate(input, output)
    with open(input) as conf_file:
        data = conf_file.read()
        input_stream = InputStream(data)
        lexer = BgcDslLexer(input_stream)
        stream = CommonTokenStream(lexer)
        dcl_parsed = BgcDslParser(stream).bgcModel()
        tableVisitor.visit(dcl_parsed)
        table = tableVisitor.symbolTable
        generator = BgcCodeGenerator(table, "output")
        generator.generate()
