/*******************************************************************************
 * TODO License

 Grammars always start with a grammar header. This grammar is called Configuration
 and must match the filename: Configuration.g4
 *******************************************************************************/
grammar Configuration; //
import Expression;   // include all rules from Expression.g4

//TODO generate Metamodel PyCore

//TODO add DeclarationModel reference for declaration = ID
configurationModel          :   'configuration' name=ID ':' declarationModel=ID
                                includes+=include*
                                ('activate' featureActivations+=featureActivation (',' featureActivations+=featureActivation)*)?
                                (parameterGroups+=parameterGroup|featureConfigurations+=featureConfiguration)*
                            ;


include                     :   'include' importedNamespace = qualifiedName;

//TODO deactivated? set deactivated to true if '!' else to false
//TODO add FeatureDeclaration reference for declaration = ID
featureActivation           :   (deactivated='!')?
                                declaration=ID
                            ;

//TODO add FeatureDeclaration reference for declaration = ID
featureConfiguration        :   'feature' declaration=ID '{'
                                ('activate' featureActivations+=featureActivation (',' featureActivations+=featureActivation)*)?
                                (parameterGroups+=parameterGroup|featureConfigurations+=featureConfiguration)*
                                '}'
                            ;

// Generic parameter group setup
//TODO add ParameterGroupDeclaration reference for declaration = ID
parameterGroup              :   'group' declaration=ID '{'
                                (parameters+=parameterAssignment)*
                                '}'
                            ;

//TODO add ParameterDeclaration reference for declaration = QualifiedName
// Array elements and ranges can be selected with brackets or, as in Fortran and the CP-DSL paper, with parentheses:
// levels[1] : 5, levels(4:5) : [ 1, 2 ]
parameterAssignment         :   declaration = qualifiedName
                                (   '[' selectors+=selector (',' selectors+=selector)*  ']'
                                |   '(' selectors+=selector (',' selectors+=selector)*  ')'
                                )? ':' value=arithmeticExpression (unit=unitSpecification)?
                            ;

selector                    :   elementSelector | rangeSelector;
elementSelector             :   element=ELONG;
rangeSelector               :   lowerBound=ELONG ':' upperBound=ELONG;

// Units follow the value, e.g. 9.81 m/s^2 or 2 km/h. They are composed from identifiers (instead of a special
// identifier token containing '*', '/' and '^'), so references in expressions like SIZE.sNx*SIZE.nSx stay products.
unitSpecification           :   unitFactor (('*' | '/') unitFactor)*
                            ;

unitFactor                  :   ID ('^' ELONG)?
                            ;

qualifiedName               :   ID ('.' ID)*
                            ;

