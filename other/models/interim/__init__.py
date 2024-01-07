from .interim import getEClassifier, eClassifiers
from .interim import name, nsURI, nsPrefix, eClass
from .interim import InterimModel, ParameterGroup, Parameter, ParameterEntry, ValueContainer, ArrayValue, IndexToValueContainerMap, ScalarValue, Feature

from declaration import DeclarationModel, FeatureDeclaration, ParameterGroupDeclaration, ParameterDeclaration
from types import TypeAssignment, Value
from configuration import Selector
from expression import Expression

from . import interim

__all__ = [ 'InterimModel', 'ParameterGroup', 'Parameter', 'ParameterEntry',
            'ValueContainer', 'ArrayValue', 'IndexToValueContainerMap', 'ScalarValue', 'Feature' ]

eSubpackages = [ ]
eSuperPackage = None
interim.eSubpackages = eSubpackages
interim.eSuperPackage = eSuperPackage

InterimModel.declaration.eType = DeclarationModel
InterimModel.parameterGroups.eType = ParameterGroup
InterimModel.features.eType = Feature
ParameterGroup.declaration.eType = ParameterGroupDeclaration
ParameterGroup.parameters.eType = Parameter
Parameter.declaration.eType = ParameterDeclaration
Parameter.specifiedType.eType = TypeAssignment
Parameter.computedValue.eType = ValueContainer
Parameter.dataEntries.eType = ParameterEntry
ParameterEntry.expression.eType = Expression
ParameterEntry.selectors.eType = Selector
ArrayValue.values.eType = IndexToValueContainerMap
IndexToValueContainerMap.value.eType = ValueContainer
ScalarValue.value.eType = Value
Feature.parameterGroups.eType = ParameterGroup
Feature.features.eType = Feature
Feature.declaration.eType = FeatureDeclaration

otherClassifiers = [ ]

for classif in otherClassifiers:
    eClassifiers[ classif.name ] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values( ):
    eClass.eClassifiers.append( classif.eClass )

for subpack in eSubpackages:
    eClass.eSubpackages.append( subpack.eClass )
