/*******************************************************************************
 * TODO License

 Grammars always start with a grammar header. This grammar is called Declaration
 and must match the filename: Declaration.g4
 *******************************************************************************/
grammar Declaration; //
import Expression;   // include all rules from Expression.g4

//TODO generate Metamodel PyCore

//TODO {DeclarationModel} enforce Type and return object of DeclarationModel
declarationModel            :   'model' name=ID
                                ('types' types+=declaredType* )?
                                (parameterGroupDeclarations+=parameterGroupDeclaration|featureDeclarations+=featureDeclaration)*
                            ;

// rule to create metamodel inheritance
namedElement                :   parameterDeclaration
                            |   parameterGroupDeclaration
                            |   featureDeclaration
                            ;

//TODO {ParameterGroupDeclaration} enforce Type and return object of ParameterGroupDeclaration
parameterGroupDeclaration   :   'group' name=ID ':' description=STRING '{' parameterDeclarations+=parameterDeclaration* '}' # paramGroupAssignStat
                            ;

parameterDeclaration        :   'def' name=ID type=paramType ':' unit=unitSpecification (',' description=STRING)? ('=' defaultValue=arithmeticExpression)? # paramAssignStat
                            ;

//TODO required? set required to true if '!' else to false
//TODO add FeatureDeclaration reference for requires+= ID and excludes+= ID
featureDeclaration          :   (required='required')? 'feature' name=ID ':' description=STRING ( '{'
                                ('requires' requires+=featureReference)*
                                ('excludes' excludes+=featureReference)*
                                (parameterGroupDeclarations+=parameterGroupDeclaration | featureGroupDeclarations+=featureGroupDeclaration)*
                   	            '}')? # featureAssignStat
                            ;

featureReference            : elements+=ID ('.' elements+=ID)*
                            ;

featureGroupDeclaration     :   'sub' kind=eKind featureDeclarations+=featureDeclaration*  # featureGroupAssignStat
                            ;

eKind                       :   alternative = 'alternative'
                            |   multiple = 'multiple'
                            ;

/**
 * Typing
 */
paramType                   :   typeReference
                            |   inlineEnumerationType
                            |   arrayType
                            ;

inlineEnumerationType       :   '(' values+=enumeral ( ',' values+=enumeral)* ')' ;

//TODO {TypeReference} enforce Type and return object of TypeReference
//TODO add Type reference for type = ID
typeReference               :   type=ID ;

//TODO {ArrayType} enforce Type and return object of ArrayType
//TODO add Type reference for type = ID
arrayType                   :   type=ID '[' dimensions+=dimension (',' dimensions+=dimension)* ']' ;

dimension                   :   sizeDimension
                            |   rangeDimension
                            ;

//TODO {SizeDimension} enforce Type and return object of SizeDimension
sizeDimension               :   (size=ELONG)? ;

//TODO {RangeDimension} enforce Type and return object of RangeDimension
rangeDimension              :   (lowerBound=ELONG)? ':' (upperBound=ELONG)? ;

declaredType                :   rangeType
                            |   enumerationType
                            ;

//TODO add PrimitiveType reference for type = ID
rangeType                   :   'range' name=ID type=ID '['
           		                minimum=literal ':' maximum=literal
           	                    ']'
                            ;

//TODO {EnumerationType} enforce Type and return object of EnumerationType
enumerationType             :   'enum' name=ID '{' values+=enumeral ( ',' values+=enumeral)* '}' ;

enumeral                    :   name=ID ('=' value=ELONG)? ;

/**
 * Units
 */

unitSpecification           :   units+=composedUnit ( '*' units+=composedUnit)* ;

basicUnit                   :   sIUnit
                            |   customUnit
                            |   '(' unitSpecification ')'
                            ;

sIUnit                      :   (prefix=ePrefix)? type=eSIUnitType #siunit;

//TODO {CustomUnit} enforce Type and return object of CustomUnit
customUnit                  :   name=STRING #customunit;

composedUnit                :   numerator=basicUnit (('/' denominator=basicUnit) | ('**' exponent=ELONG))
                            |   basicUnit
                            ;

ePrefix                     :   noP    = 'noP'
                            |   yotta  = 'yotta'
                            |   zetta  = 'zetta'
                            |   exa    = 'exa'
                            |   peta   = 'peta'
                            |   tera   = 'tera'
                            |   giga   = 'giga'
                            |   mega   = 'mega'
                            |   kilo   = 'kilo'
                            |   hecto  = 'hecto'
                            |   deca   = 'deca'
                            |   deci   = 'deci'
                            |   centi  = 'centi'
                            |   mili   = 'mili'
                            |   micro  = 'micro'
                            |   nano   = 'nano'
                            |   pico   = 'pico'
                            |   femto  = 'femto'
                            |   atto   = 'atto'
                            |   zepto  = 'zepto'
                            |   yocto  = 'yocto'
                            ;

eSIUnitType                 :   meter      = 'meter'
                            |   gram       = 'gram'
                            |   ton        = 'ton'
                            |   second     = 'second'
                            |   ampere     = 'ampere'
                            |   kelvin     = 'kelvin'
                            |   mole       = 'mole'
                            |   candela    = 'candela'
                            |   pascal     = 'pascal'
                            |   joule      = 'Joule'
                            ;
