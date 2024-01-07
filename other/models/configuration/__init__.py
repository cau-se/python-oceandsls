from .configuration import getEClassifier, eClassifiers
from .configuration import name, nsURI, nsPrefix, eClass
from .configuration import ConfigurationModel, Include, FeatureActivation, FeatureConfiguration, Selector, ElementSelector, RangeSelector, ParameterGroup, ParameterAssignment, Unit

from declaration import FeatureDeclaration, ParameterDeclaration, DeclarationModel, ParameterGroupDeclaration
from expression import Expression

from . import configuration

__all__ = [ 'ConfigurationModel', 'Include', 'FeatureActivation', 'FeatureConfiguration',
            'Selector', 'ElementSelector', 'RangeSelector', 'ParameterGroup', 'ParameterAssignment', 'Unit' ]

eSubpackages = [ ]
eSuperPackage = None
configuration.eSubpackages = eSubpackages
configuration.eSuperPackage = eSuperPackage

ConfigurationModel.declarationModel.eType = DeclarationModel
ConfigurationModel.includes.eType = Include
ConfigurationModel.featureActivations.eType = FeatureActivation
ConfigurationModel.parameterGroups.eType = ParameterGroup
ConfigurationModel.featureConfigurations.eType = FeatureConfiguration
FeatureActivation.declaration.eType = FeatureDeclaration
FeatureConfiguration.declaration.eType = FeatureDeclaration
FeatureConfiguration.featureActivations.eType = FeatureActivation
FeatureConfiguration.parameterGroups.eType = ParameterGroup
FeatureConfiguration.featureConfigurations.eType = FeatureConfiguration
ParameterGroup.declaration.eType = ParameterGroupDeclaration
ParameterGroup.parameters.eType = ParameterAssignment
ParameterAssignment.declaration.eType = ParameterDeclaration
ParameterAssignment.selectors.eType = Selector
ParameterAssignment.value.eType = Expression
ParameterAssignment.unit.eType = Unit

otherClassifiers = [ ]

for classif in otherClassifiers:
    eClassifiers[ classif.name ] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values( ):
    eClass.eClassifiers.append( classif.eClass )

for subpack in eSubpackages:
    eClass.eSubpackages.append( subpack.eClass )
