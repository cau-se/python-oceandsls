"""Definition of meta model 'units'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *

name = 'units'
nsURI = 'http://oceandsl.org/declaration/units'
nsPrefix = 'units'

eClass = EPackage( name = name, nsURI = nsURI, nsPrefix = nsPrefix )

eClassifiers = {}
getEClassifier = partial( Ecore.getEClassifier, searchspace = eClassifiers )
EPrefix = EEnum(
    'EPrefix', literals = [ 'noP', 'yotta', 'zetta', 'exa', 'peta', 'tera', 'giga', 'mega', 'kilo',
                            'hecto', 'deca', 'deci', 'centi', 'mili', 'micro', 'nano', 'pico', 'femto', 'atto', 'zepto', 'yocto' ]
    )

ESIUnitType = EEnum(
    'ESIUnitType', literals = [
            'meter', 'gram', 'ton', 'second', 'ampere', 'kelvin', 'mole', 'candela', 'pascal', 'Joul' ]
    )


@abstract
class PrimitiveUnit( EObject, metaclass = MetaEClass ):

    prefix = EAttribute( eType = EPrefix, unique = True, derived = False, changeable = True )

    def __init__( self, *, prefix = None ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

        if prefix is not None:
            self.prefix = prefix


class ElementUnit( EObject, metaclass = MetaEClass ):

    def __init__( self ):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super( ).__init__( )

    def render( self ):
        raise NotImplementedError( 'operation render(...) not yet implemented' )


@abstract
class BasicUnit( ElementUnit ):

    def __init__( self, **kwargs ):
        super( ).__init__( **kwargs )


class ComposedUnit( ElementUnit ):

    exponent = EAttribute( eType = ELongObject, unique = True, derived = False, changeable = True )
    numerator = EReference( ordered = True, unique = True, containment = True, derived = False )
    denominator = EReference( ordered = True, unique = True, containment = True, derived = False )

    def __init__( self, *, numerator = None, denominator = None, exponent = None, **kwargs ):

        super( ).__init__( **kwargs )

        if exponent is not None:
            self.exponent = exponent

        if numerator is not None:
            self.numerator = numerator

        if denominator is not None:
            self.denominator = denominator

    def render( self ):

        raise NotImplementedError( 'operation render(...) not yet implemented' )


class Unit( BasicUnit ):

    units = EReference( ordered = True, unique = True, containment = True, derived = False, upper = -1 )

    def __init__( self, *, units = None, **kwargs ):

        super( ).__init__( **kwargs )

        if units:
            self.units.extend( units )

    def render( self ):

        raise NotImplementedError( 'operation render(...) not yet implemented' )


class SIUnit( PrimitiveUnit, BasicUnit ):

    type = EAttribute( eType = ESIUnitType, unique = True, derived = False, changeable = True )

    def __init__( self, *, type = None, **kwargs ):

        super( ).__init__( **kwargs )

        if type is not None:
            self.type = type

    def render( self ):

        raise NotImplementedError( 'operation render(...) not yet implemented' )


class CustomUnit( PrimitiveUnit, BasicUnit ):

    name = EAttribute( eType = EString, unique = True, derived = False, changeable = True )

    def __init__( self, *, name = None, **kwargs ):

        super( ).__init__( **kwargs )

        if name is not None:
            self.name = name

    def render( self ):

        raise NotImplementedError( 'operation render(...) not yet implemented' )
