from .templates import getEClassifier, eClassifiers
from .templates import name, nsURI, nsPrefix, eClass
from .templates import TemplateModel, Template, FileTemplate, TextTemplate, RichString, TemplateConditional, TemplateLoop, TemplateElse, TemplateElseConditional, TemplateEnd, TemplateReference, Conditional, Switch, Case, ExpressionCase, TypeCase, DefaultCase, Loop, BooleanOperator, CompareOperator, FunctionReference, EFunction, ArrayAccess, LoopReference, LoopIndexValue, LoopCounter, RichStringLiteral, RichStringLiteralStart, RichStringLiteralInbetween, RichStringLiteralEnd, TemplateParameter, BooleanExpression, NotExpression, CompareExpression, NamedElementReference

from types import NamedElement, TypeReference
from pyecore.ecore import EObject
from expression import NamedElementReference, Expression
from declaration import DeclarationModel

from . import templates

__all__ = [ 'TemplateModel', 'Template', 'FileTemplate', 'TextTemplate', 'RichString', 'TemplateConditional', 'TemplateLoop', 'TemplateElse', 'TemplateElseConditional', 'TemplateEnd', 'TemplateReference', 'Conditional', 'Switch', 'Case', 'ExpressionCase', 'TypeCase', 'DefaultCase', 'Loop', 'BooleanOperator',
            'CompareOperator', 'FunctionReference', 'EFunction', 'ArrayAccess', 'LoopReference', 'LoopIndexValue', 'LoopCounter', 'RichStringLiteral', 'RichStringLiteralStart', 'RichStringLiteralInbetween', 'RichStringLiteralEnd', 'TemplateParameter', 'BooleanExpression', 'NotExpression', 'CompareExpression', 'NamedElementReference' ]

eSubpackages = [ ]
eSuperPackage = None
templates.eSubpackages = eSubpackages
templates.eSuperPackage = eSuperPackage

TemplateModel.declaration.eType = DeclarationModel
TemplateModel.templates.eType = Template
Template.body.eType = Expression
FileTemplate.filename.eType = Expression
FileTemplate.condition.eType = Expression
TextTemplate.parameters.eType = NamedElement
RichString.expressions.eType = EObject
TemplateConditional.expression.eType = Expression
TemplateLoop.variable.eType = NamedElementReference
TemplateElseConditional.expression.eType = Expression
TemplateReference.template.eType = TextTemplate
TemplateReference.assignments.eType = Expression
Conditional.expression.eType = Expression
Conditional.then.eType = Expression
Conditional.else_.eType = Expression
Switch.selection.eType = NamedElementReference
Switch.cases.eType = Case
Case.result.eType = Expression
ExpressionCase.value.eType = Expression
TypeCase.type.eType = TypeReference
Loop.variable.eType = NamedElementReference
Loop.then.eType = Expression
FunctionReference.elements.eType = Expression
ArrayAccess.reference.eType = NamedElementReference
ArrayAccess.indicies.eType = Expression
TemplateParameter.type.eType = TypeReference
BooleanExpression.left.eType = Expression
BooleanExpression.right.eType = Expression
NotExpression.expression.eType = Expression
CompareExpression.left.eType = Expression
CompareExpression.right.eType = Expression

otherClassifiers = [ BooleanOperator, CompareOperator, EFunction ]

for classif in otherClassifiers:
    eClassifiers[ classif.name ] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values( ):
    eClass.eClassifiers.append( classif.eClass )

for subpack in eSubpackages:
    eClass.eSubpackages.append( subpack.eClass )
