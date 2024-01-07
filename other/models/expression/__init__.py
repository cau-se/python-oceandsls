from .expression import getEClassifier, eClassifiers
from .expression import name, nsURI, nsPrefix, eClass
from .expression import Expression, EAdditionOperator, EMultiplicationOperator, ValueExpression, LiteralExpression, ParenthesisExpression, ArrayExpression, NamedElementReference, StringValue, LongValue, DoubleValue, BooleanValue, ArithmeticExpression, MultiplicationExpression

from types import NamedElement, Value

from . import expression

__all__ = [ 'Expression', 'EAdditionOperator', 'EMultiplicationOperator', 'ValueExpression', 'LiteralExpression', 'ParenthesisExpression',
            'ArrayExpression', 'NamedElementReference', 'StringValue', 'LongValue', 'DoubleValue', 'BooleanValue', 'ArithmeticExpression', 'MultiplicationExpression' ]

eSubpackages = [ ]
eSuperPackage = None
expression.eSubpackages = eSubpackages
expression.eSuperPackage = eSuperPackage

LiteralExpression.value.eType = Value
ParenthesisExpression.expression.eType = Expression
ArrayExpression.elements.eType = Expression
NamedElementReference.element.eType = NamedElement
NamedElementReference.attribute.eType = NamedElement
ArithmeticExpression.left.eType = Expression
ArithmeticExpression.right.eType = Expression
MultiplicationExpression.left.eType = ValueExpression
MultiplicationExpression.right.eType = Expression

otherClassifiers = [ EAdditionOperator, EMultiplicationOperator ]

for classif in otherClassifiers:
    eClassifiers[ classif.name ] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values( ):
    eClass.eClassifiers.append( classif.eClass )

for subpack in eSubpackages:
    eClass.eSubpackages.append( subpack.eClass )
