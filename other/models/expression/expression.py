"""Definition of meta model 'expression'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from types import Value

name = 'expression'
nsURI = 'http://www.oceandsl.org/expression/Expression'
nsPrefix = 'expression'

eClass = EPackage( name = name, nsURI = nsURI, nsPrefix = nsPrefix )

eClassifiers = {}
getEClassifier = partial( Ecore.getEClassifier, searchspace = eClassifiers )
EAdditionOperator = EEnum( 'EAdditionOperator', literals = [ 'ADDITION', 'SUBTRACTION' ] )

EMultiplicationOperator = EEnum(
    'EMultiplicationOperator', literals = [
            'MULTIPLICATION', 'DIVISION', 'MODULO' ]
    )


class Expression( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class ValueExpression( Expression ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class StringValue( Value ):

    value = EAttribute( eType = EString, unique = True, derived = False, changeable = True )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class LongValue( Value ):

    value = EAttribute( eType = ELong, unique = True, derived = False, changeable = True )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class DoubleValue( Value ):

    value = EAttribute( eType = EDouble, unique = True, derived = False, changeable = True )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class BooleanValue( Value ):

    value = EAttribute( eType = EBoolean, unique = True, derived = False, changeable = True )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class ArithmeticExpression( Expression ):

    operator = EAttribute( eType = EAdditionOperator, unique = True, derived = False, changeable = True )
    left = EReference( ordered = True, unique = True, containment = True, derived = False )
    right = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, left = None, operator = None, right = None, **kwargs ):

        super( ).__init__( **kwargs )

        if operator is not None:
            self.operator = operator

        if left is not None:
            self.left = left

        if right is not None:
            self.right = right


class MultiplicationExpression( Expression ):

    operator = EAttribute(
        eType = EMultiplicationOperator, unique = True,
        derived = False, changeable = True
        )
    left = EReference( ordered = True, unique = True, containment = True, derived = False )
    right = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, left = None, operator = None, right = None, **kwargs ):

        super( ).__init__( **kwargs )

        if operator is not None:
            self.operator = operator

        if left is not None:
            self.left = left

        if right is not None:
            self.right = right


class LiteralExpression( ValueExpression ):

    value = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class ParenthesisExpression( ValueExpression ):

    expression = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, expression = None, **kwargs ):

        super( ).__init__( **kwargs )

        if expression is not None:
            self.expression = expression


class ArrayExpression( ValueExpression ):

    elements = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, elements = None, **kwargs ):

        super( ).__init__( **kwargs )

        if elements:
            self.elements.extend( elements )


class NamedElementReference( ValueExpression ):

    element = EReference( ordered = True, unique = True, containment = False, derived = False )
    attribute = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, element = None, attribute = None, **kwargs ):

        super( ).__init__( **kwargs )

        if element is not None:
            self.element = element

        if attribute is not None:
            self.attribute = attribute
