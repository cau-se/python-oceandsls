"""Definition of meta model 'templates'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from expression import Expression, NamedElementReference, ValueExpression
from types import NamedElement

name = 'templates'
nsURI = 'http://www.oceandsl.org/template/Templates'
nsPrefix = 'templates'

eClass = EPackage( name = name, nsURI = nsURI, nsPrefix = nsPrefix )

eClassifiers = {}
getEClassifier = partial( Ecore.getEClassifier, searchspace = eClassifiers )
BooleanOperator = EEnum( 'BooleanOperator', literals = [ 'OR', 'AND' ] )

CompareOperator = EEnum( 'CompareOperator', literals = [ 'EQ', 'NE', 'LW', 'GR', 'LE', 'GE' ] )

EFunction = EEnum( 'EFunction', literals = [ 'EXIST', 'IS_EMPTY', 'SIZE', 'UPPER_CASE', 'LOWER_CASE' ] )


class TemplateModel( EObject, metaclass = MetaEClass ):

    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )
    templates = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, declaration = None, templates = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if declaration is not None:
            self.declaration = declaration

        if templates:
            self.templates.extend( templates )


class Template( EObject, metaclass = MetaEClass ):

    body = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, body = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if body is not None:
            self.body = body


class Case( EObject, metaclass = MetaEClass ):

    result = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, result = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if result is not None:
            self.result = result


class RichStringLiteralStart( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class RichStringLiteralInbetween( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class RichStringLiteralEnd( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class FileTemplate( Template ):

    filename = EReference( ordered = True, unique = True, containment = True, derived = False )
    condition = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, filename = None, condition = None, **kwargs ):

        super( ).__init__( **kwargs )

        if filename is not None:
            self.filename = filename

        if condition is not None:
            self.condition = condition


class TextTemplate( Template ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    parameters = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, name = None, parameters = None, **kwargs ):

        super( ).__init__( **kwargs )

        if name is not None:
            self.name = name

        if parameters:
            self.parameters.extend( parameters )


class TemplateConditional( Expression ):

    expression = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, expression = None, **kwargs ):

        super( ).__init__( **kwargs )

        if expression is not None:
            self.expression = expression


class TemplateLoop( Expression ):

    variable = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, variable = None, **kwargs ):

        super( ).__init__( **kwargs )

        if variable is not None:
            self.variable = variable


class TemplateElse( Expression ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class TemplateElseConditional( Expression ):

    expression = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, expression = None, **kwargs ):

        super( ).__init__( **kwargs )

        if expression is not None:
            self.expression = expression


class TemplateEnd( Expression ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class ExpressionCase( Case ):

    value = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class TypeCase( Case ):

    type = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, type = None, **kwargs ):

        super( ).__init__( **kwargs )

        if type is not None:
            self.type = type


class DefaultCase( Case ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class TemplateParameter( NamedElement ):

    type = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, type = None, **kwargs ):

        super( ).__init__( **kwargs )

        if type is not None:
            self.type = type


class BooleanExpression( Expression ):

    operator = EAttribute( eType = BooleanOperator, unique = True, derived = False, changeable = True )
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


class NotExpression( Expression ):

    expression = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, expression = None, **kwargs ):

        super( ).__init__( **kwargs )

        if expression is not None:
            self.expression = expression


class CompareExpression( Expression ):

    operator = EAttribute( eType = CompareOperator, unique = True, derived = False, changeable = True )
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


class RichString( ValueExpression ):

    expressions = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, expressions = None, **kwargs ):

        super( ).__init__( **kwargs )

        if expressions:
            self.expressions.extend( expressions )


class TemplateReference( ValueExpression ):

    template = EReference( ordered = True, unique = True, containment = False, derived = False )
    assignments = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, template = None, assignments = None, **kwargs ):

        super( ).__init__( **kwargs )

        if template is not None:
            self.template = template

        if assignments:
            self.assignments.extend( assignments )


class Conditional( ValueExpression ):

    expression = EReference( ordered = True, unique = True, containment = True, derived = False )
    then = EReference( ordered = True, unique = True, containment = True, derived = False )
    else_ = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, expression = None, then = None, else_ = None, **kwargs ):

        super( ).__init__( **kwargs )

        if expression is not None:
            self.expression = expression

        if then is not None:
            self.then = then

        if else_ is not None:
            self.else_ = else_


class Switch( ValueExpression ):

    selection = EReference( ordered = True, unique = True, containment = True, derived = False )
    cases = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, selection = None, cases = None, **kwargs ):

        super( ).__init__( **kwargs )

        if selection is not None:
            self.selection = selection

        if cases:
            self.cases.extend( cases )


class Loop( ValueExpression ):

    join = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    variable = EReference( ordered = True, unique = True, containment = True, derived = False )
    then = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, variable = None, join = None, then = None, **kwargs ):

        super( ).__init__( **kwargs )

        if join is not None:
            self.join = join

        if variable is not None:
            self.variable = variable

        if then is not None:
            self.then = then


class FunctionReference( ValueExpression ):

    function = EAttribute( eType = EFunction, unique = True, derived = False, changeable = True )
    elements = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, function = None, elements = None, **kwargs ):

        super( ).__init__( **kwargs )

        if function is not None:
            self.function = function

        if elements:
            self.elements.extend( elements )


class ArrayAccess( ValueExpression ):

    reference = EReference( ordered = True, unique = True, containment = True, derived = False )
    indicies = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, reference = None, indicies = None, **kwargs ):

        super( ).__init__( **kwargs )

        if reference is not None:
            self.reference = reference

        if indicies:
            self.indicies.extend( indicies )


class LoopIndexValue( ValueExpression ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class LoopCounter( ValueExpression ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class LoopReference( NamedElementReference ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class RichStringLiteral( RichStringLiteralStart, RichStringLiteralInbetween, RichStringLiteralEnd ):

    value = EAttribute( eType = EString, unique = True, derived = False, changeable = True )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class NamedElementReference( LoopReference ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )
