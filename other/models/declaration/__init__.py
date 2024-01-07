from .declaration import getEClassifier, eClassifiers
from .declaration import name, nsURI, nsPrefix, eClass
from .declaration import DeclarationModel, ParameterGroupDeclaration, FeatureDeclaration, FeatureGroupDeclaration, EKind, ParameterDeclaration

from types import NamedType, TypeAssignment
from expression import Expression
from units import Unit

from . import declaration

__all__ = [ 'DeclarationModel', 'ParameterGroupDeclaration', 'FeatureDeclaration',
            'FeatureGroupDeclaration', 'EKind', 'ParameterDeclaration' ]

eSubpackages = [ ]
eSuperPackage = None
declaration.eSubpackages = eSubpackages
declaration.eSuperPackage = eSuperPackage

DeclarationModel.types.eType = NamedType
DeclarationModel.parameterGroupDeclarations.eType = ParameterGroupDeclaration
DeclarationModel.featureDeclarations.eType = FeatureDeclaration
ParameterGroupDeclaration.parameterDeclarations.eType = ParameterDeclaration
FeatureDeclaration.requires.eType = FeatureDeclaration
FeatureDeclaration.excludes.eType = FeatureDeclaration
FeatureDeclaration.parameterGroupDeclarations.eType = ParameterGroupDeclaration
FeatureDeclaration.featureGroupDeclarations.eType = FeatureGroupDeclaration
FeatureGroupDeclaration.featureDeclarations.eType = FeatureDeclaration
ParameterDeclaration.type.eType = TypeAssignment
ParameterDeclaration.unit.eType = Unit
ParameterDeclaration.defaultValue.eType = Expression

otherClassifiers = [ EKind ]

for classif in otherClassifiers:
    eClassifiers[ classif.name ] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values( ):
    eClass.eClassifiers.append( classif.eClass )

for subpack in eSubpackages:
    eClass.eSubpackages.append( subpack.eClass )
