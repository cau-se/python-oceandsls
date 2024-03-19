"""Definition of meta model 'types'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *

name = 'types'
nsURI = 'http://oceandsl.org/expression/types'
nsPrefix = 'types'

eClass = EPackage( name = name, nsURI = nsURI, nsPrefix = nsPrefix )

eClassifiers = {}
getEClassifier = partial( Ecore.getEClassifier, searchspace = eClassifiers )


class Type( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


@abstract
class NamedElement( EObject, metaclass = MetaEClass ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )

    def __init__( self, *, name = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if name is not None:
            self.name = name


@abstract
class TypeAssignment( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


@abstract
class Dimension( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class TypeModel( EObject, metaclass = MetaEClass ):

    types = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, types = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if types:
            self.types.extend( types )


class Value( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class Attribute( NamedElement ):

    type = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, type = None, **kwargs ):

        super( ).__init__( **kwargs )

        if type is not None:
            self.type = type


class Enumeral( NamedElement ):

    value = EAttribute( eType = ELong, unique = True, derived = False, changeable = True )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class TypeReference( TypeAssignment ):

    type = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, type = None, **kwargs ):

        super( ).__init__( **kwargs )

        if type is not None:
            self.type = type


class SizeDimension( Dimension ):

    size = EAttribute( eType = ELongObject, unique = True, derived = False, changeable = True )

    def __init__( self, *, size = None, **kwargs ):

        super( ).__init__( **kwargs )

        if size is not None:
            self.size = size


class RangeDimension( Dimension ):

    lower_bound = EAttribute( eType = ELongObject, unique = True, derived = False, changeable = True )
    upper_bound = EAttribute( eType = ELongObject, unique = True, derived = False, changeable = True )

    def __init__( self, *, lower_bound = None, upper_bound = None, **kwargs ):

        super( ).__init__( **kwargs )

        if lower_bound is not None:
            self.lower_bound = lower_bound

        if upper_bound is not None:
            self.upper_bound = upper_bound


class EnumeralValue( Value ):

    value = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class ObjectValue( Value ):

    value = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value


class RangeValue( Value ):

    value = EReference( ordered = True, unique = True, containment = True, derived = False )
    type = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, value = None, type = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value

        if type is not None:
            self.type = type


class NamedType( Type, NamedElement ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class InlineEnumerationType( Type, TypeAssignment ):

    values = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, values = None, **kwargs ):

        super( ).__init__( **kwargs )

        if values:
            self.values.extend( values )


class RecordType( NamedType ):

    attributes = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, attributes = None, **kwargs ):

        super( ).__init__( **kwargs )

        if attributes:
            self.attributes.extend( attributes )


class PrimitiveType( NamedType ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class RangeType( NamedType ):

    type = EReference( ordered = True, unique = True, containment = False, derived = False )
    minimum = EReference( ordered = True, unique = True, containment = True, derived = False )
    maximum = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, type = None, minimum = None, maximum = None, **kwargs ):

        super( ).__init__( **kwargs )

        if type is not None:
            self.type = type

        if minimum is not None:
            self.minimum = minimum

        if maximum is not None:
            self.maximum = maximum


class EnumerationType( NamedType ):

    values = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, values = None, **kwargs ):

        super( ).__init__( **kwargs )

        if values:
            self.values.extend( values )


class ArrayType( TypeReference, Type ):

    dimensions = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, dimensions = None, **kwargs ):

        super( ).__init__( **kwargs )

        if dimensions:
            self.dimensions.extend( dimensions )
