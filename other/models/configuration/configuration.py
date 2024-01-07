"""Definition of meta model 'configuration'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *

name = 'configuration'
nsURI = 'http://www.oceandsl.org/configuration/Configuration'
nsPrefix = 'configuration'

eClass = EPackage( name = name, nsURI = nsURI, nsPrefix = nsPrefix )

eClassifiers = {}
getEClassifier = partial( Ecore.getEClassifier, searchspace = eClassifiers )


class ConfigurationModel( EObject, metaclass = MetaEClass ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    declarationModel = EReference( ordered = True, unique = True, containment = False, derived = False )
    includes = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )
    featureActivations = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )
    parameterGroups = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )
    featureConfigurations = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )

    def __init__( self, *, name = None, declarationModel = None, includes = None, featureActivations = None, parameterGroups = None, featureConfigurations = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if name is not None:
            self.name = name

        if declarationModel is not None:
            self.declarationModel = declarationModel

        if includes:
            self.includes.extend( includes )

        if featureActivations:
            self.featureActivations.extend( featureActivations )

        if parameterGroups:
            self.parameterGroups.extend( parameterGroups )

        if featureConfigurations:
            self.featureConfigurations.extend( featureConfigurations )


class Include( EObject, metaclass = MetaEClass ):

    importedNamespace = EAttribute( eType = EString, unique = True, derived = False, changeable = True )

    def __init__( self, *, importedNamespace = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if importedNamespace is not None:
            self.importedNamespace = importedNamespace


class FeatureActivation( EObject, metaclass = MetaEClass ):

    deactivated = EAttribute( eType = EBoolean, unique = True, derived = False, changeable = True )
    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )

    def __init__( self, *, deactivated = None, declaration = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if deactivated is not None:
            self.deactivated = deactivated

        if declaration is not None:
            self.declaration = declaration


class FeatureConfiguration( EObject, metaclass = MetaEClass ):

    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )
    featureActivations = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )
    parameterGroups = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )
    featureConfigurations = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )

    def __init__( self, *, declaration = None, featureActivations = None, parameterGroups = None, featureConfigurations = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if declaration is not None:
            self.declaration = declaration

        if featureActivations:
            self.featureActivations.extend( featureActivations )

        if parameterGroups:
            self.parameterGroups.extend( parameterGroups )

        if featureConfigurations:
            self.featureConfigurations.extend( featureConfigurations )


class Selector( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )


class ParameterGroup( EObject, metaclass = MetaEClass ):

    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )
    parameters = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, declaration = None, parameters = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if declaration is not None:
            self.declaration = declaration

        if parameters:
            self.parameters.extend( parameters )


class ParameterAssignment( EObject, metaclass = MetaEClass ):

    declaration = EReference( ordered = True, unique = True, containment = False, derived = False )
    selectors = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )
    value = EReference( ordered = True, unique = True, containment = True, derived = False )
    unit = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, declaration = None, selectors = None, value = None, unit = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if declaration is not None:
            self.declaration = declaration

        if selectors:
            self.selectors.extend( selectors )

        if value is not None:
            self.value = value

        if unit is not None:
            self.unit = unit


class Unit( EObject, metaclass = MetaEClass ):

    unit = EAttribute( eType = EString, unique = True, derived = False, changeable = True )

    def __init__( self, *, unit = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if unit is not None:
            self.unit = unit


class ElementSelector( Selector ):

    element = EAttribute( eType = ELong, unique = True, derived = False, changeable = True )

    def __init__( self, *, element = None, **kwargs ):

        super( ).__init__( **kwargs )

        if element is not None:
            self.element = element


class RangeSelector( Selector ):

    lowerBound = EAttribute( eType = ELong, unique = True, derived = False, changeable = True )
    upperBound = EAttribute( eType = ELong, unique = True, derived = False, changeable = True )

    def __init__( self, *, lowerBound = None, upperBound = None, **kwargs ):

        super( ).__init__( **kwargs )

        if lowerBound is not None:
            self.lowerBound = lowerBound

        if upperBound is not None:
            self.upperBound = upperBound
