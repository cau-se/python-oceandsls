
import jinja2 as j
import os

from ..symbolTable.SymbolTable import SymbolTable, VariableSymbol, Enum, CompartmentSymbol
from ..gen.python.BgcDsl.BgcDslParser import BgcDslParser

class BgcCodeGenerator():
   
    def __init__(self, symbolTable : SymbolTable, outputPath : str) -> None:
        self._symbolTable : SymbolTable = symbolTable
       # self.templateLoader = j.PackageLoader(str(self.__module__), "fileWriter/jinja-templates")
       # print(str(self.__module__))
       # self.templateEnv = j.Environment(loader=self.templateLoader)

        self.templateLoader = j.FileSystemLoader(searchpath="/home/serafim/Desktop/python-oceandsls/bgc-dsl/bgcLSPServer/fileWriter/jinja-templates")
        self.templateEnv = j.Environment(loader=self.templateLoader)

        self.outputPath = outputPath


    def generate(self) -> None:

      #  print(self._symbolTable.children())
        for c in self._symbolTable.children():
            if c.name:
                print(c.name)
            else:
                print("ff")
        symbols = list(filter(lambda x :type(x) is CompartmentSymbol,self._symbolTable.children()))
        print(symbols)
#    filter( lambda x : x is CompartmentSymbol, self._symbolTable.children())) # Get Compartments
     #   print(symbols)
        for e in symbols:
            mainTemplate = self.templateEnv.get_template('fun_group.txt')  # Entry Template
            classname = e.name #
            print(f'classname:{classname}')
            parameters = e.value.constants
            print(f'parmas:{parameters}')
            module = e.name
            print(f'module:{module}')
            fungroup_path = os.path.join(self.outputPath, f'{module}')
            print(f'path exists{os.path.isdir(self.outputPath)}')
            control = open(fungroup_path, "w+")
            control.write(mainTemplate.render(class_name = classname, parameters = parameters, modulname = module, namelist = parameters))
            control.close()




