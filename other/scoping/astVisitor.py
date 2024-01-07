from antlr_ast.ast import parse, process_tree, Terminal
import buildpython as grammar
import ast
import astunparse
import dictScope
import itertools


def depth_ast( root ):
    return 1 + max(
        map( depth_ast, ast.iter_child_nodes( root ) ),
        default = 0
        )


# way to compare two ast wich each other
def compare_ast( node1, node2 ):
    if type( node1 ) is not type( node2 ):
        return False
    if isinstance( node1, ast.AST ):
        for k, v in vars( node1 ).iteritems( ):
            if k in ('lineno', 'col_offset', 'ctx'):
                continue
            if not compare_ast( v, getattr( node2, k ) ):
                return False
        return True
    elif isinstance( node1, list ):
        return all( itertools.starmap( compare_ast, itertools.izip( node1, node2 ) ) )
    else:
        return node1 == node2


def find_function( root, node, depth ):
    last_function = root
    curr_depth = depth_ast( root )
    root_depth = depth
    for nod in ast.walk( root ):
        curr_depth = depth_ast( nod )
        if compare_ast( nod, node ) and depth == curr_depth:
            block = depth_ast( last_function ) - curr_depth
            return (last_function, block)
        else:
            if curr_depth == root_depth - 1:
                last_function = nod
    raise


def createAst( grammar, grammar_input, first_grammar_rule ):
    antlr_tree = parse( grammar, grammar_input, first_grammar_rule, True )
    return process_tree( antlr_tree )


def insertVariablesInScope( grammar, grammar_input: str, first_grammar_rule: str, track_names: list, with_resolving: bool, scope: dictScope = None, id_name: str = "ID" ):
    if scope is None:
        scope = dictScope.dictScope( )
        scope.__init__( )
    simple_tree = createAst( grammar, grammar_input, first_grammar_rule )
    for line in simple_tree:
        astDepth = depth_ast( line )
        for node in ast.walk( line ):
            thisNodeDepth = depth_ast( node )
            # Block Scope build: global -> funktionVar -> blocks : Means everytime -1 in the depth of the node
            if type( node ).__name__ in track_names:
                if thisNodeDepth >= astDepth - 1:
                    print( "add Global " + type( node ).__name__ + " with value: " + str( node ) )
                    for value in ast.iter_fields( node ):
                        if (value[ 0 ] == id_name):
                            node_name = value[ 1 ]
                    scope.addFunctionOrGlobalVar( str( node_name ), node )
                else:
                    try:
                        node_function, block = find_function( simple_tree, node, thisNodeDepth )
                        for value in ast.iter_fields( node ):
                            if (value[ 0 ] == id_name):
                                node_name = value[ 1 ]
                        print( "Found function: " + node_function + " and add: " + type( node ).__name__ + " with value: " + str( node ) + " in block " + str( block ) )
                        scope.addLocal( str( node_name ), value = node, funcI = node_function, block = block )
                    except:
                        print( "Something went wrong, the node " + astunparse.dump( node ) + " could not be added to block scope" )
    return scope


if __name__ == "__main___":
    NAMES = [ "AssignStat" ]  # TODO: How do we know what we are seaching for?
    FILE_PATH = "/home/armin/Dokumente/antlr4/test.testGrammar"
    FIRST_GRAMMAR_RULE = "prog"
    ID_NAME = "ID"
    EXPR_NAME = "expr"
    TYPE_EXPR = "type"
    scope = dictScope.dictScope( )
    scope.__init__( )

    with open( FILE_PATH ) as file:
        print( insertVariablesInScope( grammar, file.read( ), FIRST_GRAMMAR_RULE, NAMES, False, scope ) )
