/** BGC DSL grammar. */
grammar BgcDsl;

import CommonLexerRules;

/** 
 * Main rule
 * Each model has a unique name as an ID, a list of substances that
 * are used in the model, global parameters, and diagnostic values.
 * The model itself is then comprised of compartments and connections.
 *
 * - name = model identifier
 * - substanceDeclarations = list of substance declarations
 * - parameterDeclarations = list of parameter declarations
 * - environments = list of environment and diagnostic variables
 * - compartments = list of compartment specifications
 * - connections = list of connection specifications
 */
bgcModel:
	'model' name=ID
	'substances' substanceDeclarations+=substanceDeclaration+
	('parameters' parameterDeclarations+=parameterDeclaration*)?
	('diagnostics' environments+=environmentVariableDeclaration*)?
	(compartments+=compartment|connections+=connection)+
;

/** 
 * Substance declaration for the BGC model.
 * - type = primitive data type
 * - name = unique name in its scope
 * - unit = unit of measurement
 */
substanceDeclaration:
	type=primitiveTypes name=ID unit
;

/**
 * Parameter declaration for the BGC model or a compartment.
 * - type = primitive data type
 * - name = unique name in its scope
 * - unit = unit of measurement
 * - expression = an arithmetic expression to specify its start value
 */
parameterDeclaration:
	type=primitiveTypes name=ID unit '=' expression=arithmeticExpression
;

/**
 * Diagnostic declaration for the BGC model or a compartment.
 * - type = primitive data type
 * - name = unique name in its scope
 * - unit = unit of measurement
 * - expression = an optional arithmetic expression to specify its start
 *   value. Not all diagnostics have a start value in the models as input
 *   for the DSL design.
 */
environmentVariableDeclaration:
	type=primitiveTypes name=ID unit ('=' expression=arithmeticExpression)?
;

/** primitive data type. */
primitiveTypes:
	'int' | 'float' | 'double' | 'string'
;

/**
 * A compartment is a portion of a BGC model containing a set of substances and
 * calculations regarding for the compartment.
 * Compartments can abstract, i.e., they are not intended to be used directly.
 * They can inherit from parent compartments.
 * The substances define the state of the compartment.
 * 
 * Like the global scope, compartments can have parameter and diagnostics of their
 * own. Furthermoe, the contain calculations and update directives for states.
 * Calculations can used to make update directives more readable.
 *
 * - abtract = if present make compartment abstract
 * - name = unique identifier of the compartment
 * - parent = unique identifier of the parent compartment
 * - states = list of substance states
 * - constants = list of parameter declarations
 * - evnironments = list of environment and diagnostic variables
 * - calculations = list of calculations
 * - updateStates = list of state update expressions
 */
compartment:
	'abstract'? 'compartment' name=ID ('extends' parent = ID)? '{'
		'states' states+=substanceState+
		('parameters' constants+=parameterDeclaration*)?
		('diagnostics' evnironments+=environmentVariableDeclaration*)?

		calculations+=calculation*
		updateStates+=updateState+
	'}'
;

/**
 * Declaration of a state for one substance in a compartment.
 * - substance = unique identifier (type substanceDeclaration)
 * - expression = can be any arithmetic expression to set the initial value
 *   of the state. The expression will be computed during setup. The expression
 *   is optional. The default values is 0.
 */
substanceState:
	substance=ID ('=' expression=arithmeticExpression)?
;

/**
 * Update the substance state specified by the stat identifier.
 * - state = uniqe state identifiec (type substanceState)
 * - expression = used to compute the new state
 */
updateState:
    'update' state=ID '=' expression=arithmeticExpression
;

/**
 * Connections connect two compartments with each other. They are used to describe
 * the exchange of substances. The substances are transferred from the sourceCompartment
 * to the targetCompartment.
 * A connection can contain either one expression after an equal sign or a set of expression
 * to address multiple substances.
 * To reduce complexity and facility resue of expressions, it is also possible to use
 * calculations in connections.
 *
 * - name = unique name of the connection
 * - substances = list of IDs referring to substance declarations
 * - sourceCompartment = ID of the source compartment
 * - targetCompartment = ID of the target compartment
 * - expression = arithmetic expression
 * - substanceExpressions = list of arithemetic expressions
 * - calculations = list of calculations
 */
// sourceCompartment and targetCompartment are of type compartment
// substances and substance are of type substanceDeclaration
connection:
	'connection' (
		(name=ID ('(' substances+=ID (',' substances+=ID)* ')')? 'from' sourceCompartment=ID 'to' targetCompartment=ID) |
		(sourceCompartment=ID 'to' targetCompartment=ID name=ID ('(' substances+=ID (',' substances+=ID)* ')')?)
	)
	(
		'=' expression=arithmeticExpression |
		'{' (substanceExpressions+=substanceExpression | calculations+=calculation)* '}'
	)
;

/**
 * Substance expression specifications.
 * - substance = unique identifier for the substance
 * - expression = arithmetic expression to comupte a substance value
 */
substanceExpression:
	substance=ID '=' expression=arithmeticExpression
;

/**
 * Calculations, there are two types basic and alternative calculations.
 */
calculation: basicCalculation | alternativeCalculation;

/**
 * Basic calculation compute one value and make it available under the unique name.
 * - name = unique name of the calculation
 * - expression = expression used to compute the value
 */
basicCalculation:
	'calc' name=ID '=' expression=arithmeticExpression
;

/**
 * Alternative calculations which are selected by an expression and a 
 * list of case calculations
 * - name = unique identifier of the calculation
 * - expression = the selection expression, for the cases
 * - alternatives = list of cases
 */
alternativeCalculation:
	'alternatives' name=ID ':' expression=arithmeticExpression '{'
		alternatives+=caseCalculation*
	'}'
;

/**
 * One case calculation.
 * - literal = literal to define the case
 * - expression = the expression to be used in case the case is selected.
 */
caseCalculation:
    'case' literalExp=literalExpression ':' expression=arithmeticExpression
;

// ----------------------
// Units
// ----------------------

unit:
	':' elements+=unitElement+ |
	'::'
;

unitElement:
	prefixUnit | groupUnit
;

groupUnit:
	'(' elements+=unitElement* ')' ('^' exponent=NUMBER)?
;

// substance is of type substanceDeclaration
// removed unit-label for UNIT_STRING, here
prefixUnit:
	(UNIT_STRING | custom=CUSTOM_STRING) (substance=ID)? ('^' exponent=NUMBER)?
;

// ----------------------
// Expression definitions
// ----------------------

// returns expression
arithmeticExpression:
	multiplicationExpression (operator=eAdditionOperator right=arithmeticExpression)?
;

// returns eAdditionOperator
eAdditionOperator:
	ADDITION = '+' |
	SUBTRACTION = '-'
;

// returns expression
multiplicationExpression:
	powerExpression (operator=eMultiplicationOperator right=multiplicationExpression)?
;

// returns eMultiplicationOperator
eMultiplicationOperator:
	MULTIPLICATION = '*' |
	DIVISION = '/' |
	MODULO = '%'
;

// returns expression
powerExpression:
	valueExpression ('^' right=valueExpression)?
;

valueExpression:
	arrayExpression |
	functionCallingExpression |
	literalExpression |
	parenthesisExpression |
	termReference
;

arrayExpression:
	'[' expressions+=arithmeticExpression (',' expressions+=arithmeticExpression)* ']'
;

functionCallingExpression: type=function '(' expressions+= arithmeticExpression (',' expressions+= arithmeticExpression)* ')';

function:
	'exp' | 'inverse' | 'max'
;

literalExpression:
	value=literal
;

literal:
	numberLiteral |
	stringLiteral
;

numberLiteral:
	value=NUMBER
;

stringLiteral:
	value='string'
;

// returns ecore::EBigDecimal
// changed pre-dot numbers from * to +
NUMBER:
	('-')? ('0'..'9')+ ('.' ('0'..'9')+)?
;

// returns ecore::EString
CUSTOM_STRING:
	'#'('A' .. 'Z'|'a'..'z')+
;

// returns ecore::EString
UNIT_STRING:
	('Q'|'R'|'Y'|'Z'|'E'|'P'|'T'|'G'|'M'|'k'|'h'|'da'|'d'|'c'|'m'|'my'|'n'|'p'|'f'|'a'|'z'|'y'|'r'|'q')?('s'|'m'|'g'|'mol'|'cd'|'W'|'J'|'K'|'A')
;

parenthesisExpression:
	'(' expression=arithmeticExpression ')'
;

// sourceCompartment and targetCompartment are of type compartment
// reference is of type term
termReference:
	(sourceCompartment=ID '>')?  (targetCompartment=ID ':')? reference=qualifiedName
;

// should be moved to documentation
subterm:
	updateState | connection | parameterDeclaration | calculation | environmentVariableDeclaration | substanceExpression | substanceState
;

qualifiedName:
	ID ('.' ID)*
;

// returns ecore::EInt
INT:
	'this one has been deactivated'
;
