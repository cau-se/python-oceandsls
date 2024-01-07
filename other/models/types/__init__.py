from .types import getEClassifier, eClassifiers
from .types import name, nsURI, nsPrefix, eClass
from .types import Type, NamedElement, NamedType, RecordType, Attribute, PrimitiveType, RangeType, EnumerationType, InlineEnumerationType, Enumeral, TypeReference, TypeAssignment, ArrayType, Dimension, SizeDimension, RangeDimension, TypeModel, Value, EnumeralValue, ObjectValue, RangeValue

from pyecore.ecore import EObject

from . import types

__all__ = [ 'Type', 'NamedElement', 'NamedType', 'RecordType', 'Attribute', 'PrimitiveType', 'RangeType', 'EnumerationType', 'InlineEnumerationType', 'Enumeral',
            'TypeReference', 'TypeAssignment', 'ArrayType', 'Dimension', 'SizeDimension', 'RangeDimension', 'TypeModel', 'Value', 'EnumeralValue', 'ObjectValue', 'RangeValue' ]

eSubpackages = [ ]
eSuperPackage = None
types.eSubpackages = eSubpackages
types.eSuperPackage = eSuperPackage

RecordType.attributes.eType = Attribute
Attribute.type.eType = TypeReference
RangeType.type.eType = PrimitiveType
RangeType.minimum.eType = Value
RangeType.maximum.eType = Value
EnumerationType.values.eType = Enumeral
InlineEnumerationType.values.eType = Enumeral
TypeReference.type.eType = Type
ArrayType.dimensions.eType = Dimension
TypeModel.types.eType = NamedType
EnumeralValue.value.eType = Enumeral
ObjectValue.value.eType = EObject
RangeValue.value.eType = Value
RangeValue.type.eType = RangeType

otherClassifiers = [ ]

for classif in otherClassifiers:
    eClassifiers[ classif.name ] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values( ):
    eClass.eClassifiers.append( classif.eClass )

for subpack in eSubpackages:
    eClass.eSubpackages.append( subpack.eClass )
