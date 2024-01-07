from .units import getEClassifier, eClassifiers
from .units import name, nsURI, nsPrefix, eClass
from .units import Unit, PrimitiveUnit, BasicUnit, ElementUnit, EPrefix, SIUnit, ESIUnitType, CustomUnit, ComposedUnit

from . import units

__all__ = [ 'Unit', 'PrimitiveUnit', 'BasicUnit', 'ElementUnit',
            'EPrefix', 'SIUnit', 'ESIUnitType', 'CustomUnit', 'ComposedUnit' ]

eSubpackages = [ ]
eSuperPackage = None
units.eSubpackages = eSubpackages
units.eSuperPackage = eSuperPackage

Unit.units.eType = ElementUnit
ComposedUnit.numerator.eType = BasicUnit
ComposedUnit.denominator.eType = BasicUnit

otherClassifiers = [ EPrefix, ESIUnitType ]

for classif in otherClassifiers:
    eClassifiers[ classif.name ] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values( ):
    eClass.eClassifiers.append( classif.eClass )

for subpack in eSubpackages:
    eClass.eSubpackages.append( subpack.eClass )
