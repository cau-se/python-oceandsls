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
parameterAssignment         :   declaration = qualifiedName ('[' selectors+=selector (',' selectors+=selector)*  ']')? ':' value=arithmeticExpression (unit=unitSpecification)?
                            ;

selector                    :   elementSelector | rangeSelector;
elementSelector             :   element=ELONG;
rangeSelector               :   lowerBound=ELONG ':' upperBound=ELONG;

unitSpecification           :   unit=ID
                            ;

qualifiedName               :   ID ('.' ID)*
                            ;

/** Lexer rules (start uppercase)*/

ID                          : ( [a-zA-Z] | '_') ( [a-zA-Z] | '_' | [0-9] | '^' | '-' | '*' | '/' )*; // override identifiers
