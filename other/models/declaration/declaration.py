"""Definition of meta model 'declaration'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from types import NamedElement

name = 'declaration'
nsURI = 'http://www.oceandsl.org/declaration/Declaration'
nsPrefix = 'declaration'

eClass = EPackage( name = name, nsURI = nsURI, nsPrefix = nsPrefix )

eClassifiers = {}
getEClassifier = partial( Ecore.getEClassifier, searchspace = eClassifiers )
EKind = EEnum( 'EKind', literals = [ 'ALTERNATIVE', 'MULTIPLE' ] )


class DeclarationModel( EObject, metaclass = MetaEClass ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    types = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )
    parameterGroupDeclarations = EReference(
            ordered = True, unique = True, containment = True, derived = False, upper = -1
    )
    featureDeclarations = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )

    def __init__( self, *, name = None, types = None, parameterGroupDeclarations = None, featureDeclarations = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if name is not None:
            self.name = name

        if types:
            self.types.extend( types )

        if parameterGroupDeclarations:
            self.parameterGroupDeclarations.extend( parameterGroupDeclarations )

        if featureDeclarations:
            self.featureDeclarations.extend( featureDeclarations )


class FeatureGroupDeclaration( EObject, metaclass = MetaEClass ):

    kind = EAttribute( eType = EKind, unique = True, derived = False, changeable = True )
    featureDeclarations = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )

    def __init__( self, *, kind = None, featureDeclarations = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if kind is not None:
            self.kind = kind

        if featureDeclarations:
            self.featureDeclarations.extend( featureDeclarations )


class ParameterGroupDeclaration( NamedElement ):

    description = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    parameterDeclarations = EReference(
        ordered = True, unique = True,
        containment = True, derived = False, upper = -1
        )

    def __init__( self, *, description = None, parameterDeclarations = None, **kwargs ):

        super( ).__init__( **kwargs )

        if description is not None:
            self.description = description

        if parameterDeclarations:
            self.parameterDeclarations.extend( parameterDeclarations )


class FeatureDeclaration( NamedElement ):

    required = EAttribute( eType = EBoolean, unique = True, derived = False, changeable = True )
    description = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    requires = EReference( ordered = True, unique = False, containment = False, derived = False, upper = -1 )
    excludes = EReference( ordered = True, unique = False, containment = False, derived = False, upper = -1 )
    parameterGroupDeclarations = EReference(
            ordered = True, unique = True, containment = True, derived = False, upper = -1
    )
    featureGroupDeclarations = EReference(
            ordered = True, unique = True, containment = True, derived = False, upper = -1
    )

    def __init__( self, *, required = None, description = None, requires = None, excludes = None, parameterGroupDeclarations = None, featureGroupDeclarations = None, **kwargs ):

        super( ).__init__( **kwargs )

        if required is not None:
            self.required = required

        if description is not None:
            self.description = description

        if requires:
            self.requires.extend( requires )

        if excludes:
            self.excludes.extend( excludes )

        if parameterGroupDeclarations:
            self.parameterGroupDeclarations.extend( parameterGroupDeclarations )

        if featureGroupDeclarations:
            self.featureGroupDeclarations.extend( featureGroupDeclarations )


class ParameterDeclaration( NamedElement ):

    description = EAttribute( eType = EString, unique = True, derived = False, changeable = True )
    type = EReference( ordered = True, unique = True, containment = True, derived = False )
    unit = EReference( ordered = True, unique = True, containment = True, derived = False )
    defaultValue = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, type = None, unit = None, description = None, defaultValue = None, **kwargs ):

        super( ).__init__( **kwargs )

        if description is not None:
            self.description = description

        if type is not None:
            self.type = type

        if unit is not None:
            self.unit = unit

        if defaultValue is not None:
            self.defaultValue = defaultValue
