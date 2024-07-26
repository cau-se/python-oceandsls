/*******************************************************************************
 * TODO License

 Grammars always start with a grammar header. This grammar is called Expression
 and must match the filename: Expression.g4
 *******************************************************************************/
grammar Expression; //
import Terminals;   // include all rules from Terminals.g4

//TODO generate Metamodel PyCore

/** Parser rules (start lowercase)*/
//TODO optional add expression type

//TODO Syntactic Predicates => ->
arithmeticExpression        : left=multiplicationExpression op=eAdditionOperator right=arithmeticExpression
                            | multiplicationExpression
                            ;

eAdditionOperator           : '+'
                            | '-'
                            ;

//TODO predicates: ->
multiplicationExpression    : left=valueExpression op=eMultiplicationOperator right=multiplicationExpression
                            | valueExpression
                            ;

eMultiplicationOperator     : '*'
                            | '/'
                            | '%'
                            ;

valueExpression             : parenthesisExpression
                            | namedElementReference
                            | arrayExpression
                            | literalExpression
                            ;

literalExpression           : value = literal ;

//TODO returns types::Value
literal                     : stringValue
                            | longValue
                            | doubleValue
                            | booleanValue
                            ;

parenthesisExpression       : '(' expression=arithmeticExpression ')' ;

//TODO {ArrayExpression} enforce Type and return object of ArrayExpression
arrayExpression             : '[' (elements+=arithmeticExpression (',' elements+=arithmeticExpression)*)? ']' ;

//TODO returns NamedElementReference
//TODO add NamedElement reference for element = ID and attribute  ID
//TODO {NamedElementReference} enforce Type and return object of NamedElementReference
namedElementReference       : element=ID ('.' attribute=ID)? ;

stringValue                 : value = STRING ;

longValue                   : value = ELONG ;

doubleValue                 : value = EDOUBLE ;

booleanValue                : value = EBoolean ;

// -----------------------------------------------------------------------
// ANTLR expr grammar with parenthesis and numbers
// -----------------------------------------------------------------------
/*
expr
    : '(' expr ')'                              # ParenExpr
    | left=expr op=('*'|'/'|'%') right=expr     # InfixExpr
    | left=expr op=('+'|'-') right=expr         # InfixExpr
    | atom=INT                                  # NumberExpr
    ;
*/
// -----------------------------------------------------------------------

/** Lexer rules (start uppercase)*/

// TODO returns ecore::ELong
ELONG       : '-'? INT;

// TODO returns ecore::EDouble
EDOUBLE     : '-'? INT? '.' INT (('E'|'e') '-'? INT)?;

// TODO returns ecore::EBoolean
EBoolean    : 'true'
            | 'false'
            ;
