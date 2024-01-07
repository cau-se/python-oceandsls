from ast import *


class MyTransform( NodeTransformer ):

    def visit_ClassDef( self, node, parserName ):
        # print(unparse(node.body))
        result = [ ]
        for x in node.body:
            # print(type(x))
            if isinstance( x, FunctionDef ):
                print( "Enter FuncDef: " + x.name )
                if x.name == "__init__":
                    result.append( x )
            elif isinstance( x, (Import, ImportFrom) ):
                result.append( x )
            elif isinstance( x, ClassDef ):
                print( "Enter ClassDef: " + x.name )
                print( x.__dict__ )
                result.append( self.visit_ClassDef( x, parserName ) )
        node.body = result
        return node


def writeClassesOut( filePath: str, grammarParserName: str, outputpath: str = "." ):

    visitor = MyTransform( )

    with open( filePath ) as f:
        data = f.read( )

    node = parse( data )

    node = visitor.visit_ClassDef( node, grammarParserName )
    bug = unparse( node )

    f = open( outputpath + grammarParserName + "Classes.py", "w" )
    f.write( bug )
