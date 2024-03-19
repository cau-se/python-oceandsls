"""Definition of meta model 'interim'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *

name = 'interim'
nsURI = 'https://oceandsl.org/interim'
nsPrefix = 'interim'

eClass = EPackage( name = name, nsURI = nsURI, nsPrefix = nsPrefix )

eClassifiers = {}
getEClassifier = partial( Ecore.getEClassifier, searchspace = eClassifiers )


class InterimModel( EObject, metaclass = MetaEClass ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )
    parameterGroups = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )
    features = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, declaration = None, name = None, parameterGroups = None, features = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if name is not None:
            self.name = name

        if declaration is not None:
            self.declaration = declaration

        if parameterGroups:
            self.parameterGroups.extend( parameterGroups )

        if features:
            self.features.extend( features )


class ParameterGroup( EObject, metaclass = MetaEClass ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )
    parameters = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, name = None, declaration = None, parameters = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if name is not None:
            self.name = name

        if declaration is not None:
            self.declaration = declaration

        if parameters:
            self.parameters.extend( parameters )


class Parameter( EObject, metaclass = MetaEClass ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )
    specifiedType = EReference( ordered = True, unique = True, containment = True, derived = False )
    computedValue = EReference( ordered = True, unique = True, containment = True, derived = False )
    dataEntries = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, name = None, declaration = None, specifiedType = None, computedValue = None, dataEntries = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if name is not None:
            self.name = name

        if declaration is not None:
            self.declaration = declaration

        if specifiedType is not None:
            self.specifiedType = specifiedType

        if computedValue is not None:
            self.computedValue = computedValue

        if dataEntries:
            self.dataEntries.extend( dataEntries )


class ParameterEntry( EObject, metaclass = MetaEClass ):

    expression = EReference( ordered = True, unique = True, containment = False, derived = False )
    selectors = EReference( ordered = True, unique = True, containment = False, derived = False, upper = -1 )

    def __init__( self, *, expression = None, selectors = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if expression is not None:
            self.expression = expression

        if selectors:
            self.selectors.extend( selectors )


class ValueContainer( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class IndexToValueContainerMap( EObject, metaclass = MetaEClass ):

    key = EAttribute( eType = ELongObject, unique = True, derived = False, changeable = True )
    value = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, value = None, key = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if key is not None:
            self.key = key

        if value is not None:
            self.value = value


class Feature( EObject, metaclass = MetaEClass ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    active = EAttribute( eType = EBoolean, unique = True, derived = False, changeable = True )
    parameterGroups = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )
    features = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )
    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, name = None, parameterGroups = None, features = None, declaration = None, active = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if name is not None:
            self.name = name

        if active is not None:
            self.active = active

        if parameterGroups:
            self.parameterGroups.extend( parameterGroups )

        if features:
            self.features.extend( features )

        if declaration is not None:
            self.declaration = declaration


class ArrayValue( ValueContainer ):

    upper_bound = EAttribute( eType = ELong, unique = True, derived = False, changeable = True )
    lower_bound = EAttribute( eType = ELong, unique = True, derived = False, changeable = True )
    values = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, values = None, upper_bound = None, lower_bound = None, **kwargs ):

        super( ).__init__( **kwargs )

        if upper_bound is not None:
            self.upper_bound = upper_bound

        if lower_bound is not None:
            self.lower_bound = lower_bound

        if values:
            self.values.extend( values )


class ScalarValue( ValueContainer ):

    value = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, value = None, **kwargs ):

        super( ).__init__( **kwargs )

        if value is not None:
            self.value = value
