from pyecoregen import ecore as a
from pyecore.resources import ResourceSet, URI
import sys


def readAndCreateEcore( ecores, output ):
    for i in ecores:
        # Read the .ecore Files
        rset = ResourceSet( )
        resource = rset.get_resource( URI( i ) )
        library_model = resource.contents[ 0 ]
        rset.metamodel_registry[ library_model.nsURI ] = library_model

        # Generate the Python files
        generator = a.EcoreGenerator( )
        generator.generate( library_model, output )
        print( i + " done." )


args = sys.argv
if (not len( args ) == 1):
    readAndCreateEcore( args[ 1:(len( args ) - 1) ], args[ len( args ) - 1 ] )
else:
    print( "Usage i.e.: python ecoreExp.py file1.py file2.py output/" )
