from parsimonious import TokenGrammar, ParseError, IncompleteParseError  # type: ignore

grammar = TokenGrammar(
    r"""
HeaderFile <- IncludeStatement* HeaderFileElement+
HeaderFileElement <- TypeDefinition / FunctionDeclaration / VariableDefinition / VariableDeclaration

ImplementationFile <- IncludeStatement* ImplementationFileElement+
ImplementationFileElement <- TypeDefinition / VariableDefinition / FunctionDefinition

IncludeStatement <- 'include' string-literal ';'

TypeDefinition <- StructDefinition / EnumDefinition / UnionDefinition
StructDefinition <- NormalStructDefinition / OpaqueStructDefinition
NormalStructDefinition <- 'struct' identifier '{' VariableDeclaration+ '}'
OpaqueStructDefinition <- 'opaque' 'struct' identifier ';'
EnumDefinition <- 'enum' identifier '{' EnumMember (',' EnumMember)* ','? '}'
EnumMember <- identifier ('=' Expression)?
UnionDefinition <- RobustUnionDefinition / FragileUnionDefinition
RobustUnionDefinition <- 'union' identifier '{' VariableDeclaration UnionBody '}'
UnionBody <- 'switch' '(' identifier ')' '{' UnionBodySet+ '}'
UnionBodySet <- CaseSpecifier+ (VariableDeclaration / ';')
FragileUnionDefinition <- 'fragile' 'union' identifier '{' VariableDeclaration+ '}'

FunctionDeclaration <- FunctionSignature ';'
FunctionDefinition <- FunctionSignature Block
FunctionSignature <- Type identifier '(' SignatureArguments? ')'
SignatureArguments <- Type identifier (',' Type identifier)* ','?

Block <- '{' Statement* '}'
       
Statement <- VariableDefinition / StructureStatement / FlowControlStatement / AssignmentStatement / FragileStatement / ExpressionStatement / EmptyStatement
EmptyStatement <- ';'
FragileStatement <- 'fragile' Statement
ExpressionStatement <- Expression ';'

VariableDeclaration <- Type identifier ';'
VariableDefinition <- Type identifier '=' Expression ';'

StructureStatement <- IfStatement / SwitchStatement / WhileStatement / DoWhileStatement / ForStatement
IfStatement <- 'if' '(' Expression ')' Block ('else' Block)?
SwitchStatement <- 'switch' '(' Expression ')' '{' (CaseSpecifier / Statement)+ '}'
CaseSpecifier <- ('case' Expression ':') / ('default' ':')
WhileStatement <- 'while' '(' Expression ')' Block
DoWhileStatement <- 'do' Block 'while' '(' Expression ')' ';'
ForStatement <- 'for' '(' ForInit? ';' Expression ';' ForUpdate? ')' Block
ForInit <- ForInitializer (',' ForInitializer)* ','?
ForInitializer <- Type identifier '=' Expression
ForUpdate <- AssignmentBody (',' AssignmentBody)* ','?

FlowControlStatement <- ContinueStatement / BreakStatement / ReturnStatement
ContinueStatement <- 'continue' ';'
BreakStatement <- 'break' ';'
ReturnStatement <- 'return' Expression? ';'

AssignmentStatement <- AssignmentBody ';'
AssignmentBody <- DirectAssignmentBody / UpdateAssignmentBody / CrementAssignmentBody
DirectAssignmentBody <- Expression '=' Expression
UpdateAssignmentBody <- Expression ('+=' / '-=' / '*=' / '/=' / '%=' / '&=' / '^=' / '|=') Expression
CrementAssignmentBody <- Expression ('++' / '--')

Type <- ConstType / PointerType / ArrayType / FunctionType / BasicType
ConstType <- 'const' BasicType
PointerType <- BasicType '*'
ArrayType <- BasicType '[' Expression ']'
FunctionType <- BasicType 'function' '(' FunctionTypeArgs? ')'
FunctionTypeArgs <- BasicType (',' BasicType)* ','?
BasicType <- 'void' / 'bool' / 'float32' / 'float64' /
             'int8' / 'int16' / 'int32' / 'int64' / 'intaddr' / 'intmax' / 'intsize' /
             'uint8' / 'uint16' / 'uint32' / 'uint64' / 'uintaddr' / 'uintmax' / 'uintsize' /
             ('struct' identifier) / ('enum' identifier) / ('union' identifier) / ('(' Type ')')


AtomicExpression <- identifier / constant / 'true' / 'false' / string-literal / ('(' Expression ')')

ObjectExpression <- (AtomicExpression ObjectSuffix*) / ArrayLiteral / StructLiteral
ObjectSuffix <- ArrayIndexSuffix / FunctionCallSuffix / StructElementSuffix / StructPointerElementSuffix

ArrayIndexSuffix <- '[' Expression ']'

FunctionCallSuffix <- '(' CommasExpressionList? ')'
CommasExpressionList <- Expression (',' Expression)* ','?

StructElementSuffix <- '.' identifier

StructPointerElementSuffix <- '->' identifier

ArrayLiteral <- '{' CommasExpressionList '}'

StructLiteral <- '{' StructLiteralElement (',' StructLiteralElement)* ','? '}'
StructLiteralElement <- '.' identifier '=' Expression

FactorExpression <- CastExpression / AddressOfExpression / DerefExpression / PositiveExpression / NegativeExpression / BitwiseNotExpression / LogicalNotExpression / SizeofExpression / ObjectExpression

CastExpression <- '(' Type ')' ObjectExpression

AddressOfExpression <- '&' ObjectExpression

DerefExpression <- '*' ObjectExpression

PositiveExpression <- '+' ObjectExpression

NegativeExpression <- '-' ObjectExpression

BitwiseNotExpression <- '~' ObjectExpression

LogicalNotExpression <- '!' ObjectExpression

SizeofExpression <- ('sizeof' ObjectExpression) / ('sizeof' Type)

TermExpression <- FactorExpression TermSuffix?
TermSuffix <- ('*' FactorExpression)+ / ('/' FactorExpression)+ / ('%' FactorExpression)+

ArithmeticExpression <- TermExpression ArithmeticSuffix?
ArithmeticSuffix <- ('+' TermExpression)+ / ('-' TermExpression)+

BitwiseOpExpression <- ShiftExpression / XorExpression / BitwiseAndExpression / BitwiseOrExpression / ArithmeticExpression

ShiftExpression <- (ArithmeticExpression '<<' ArithmeticExpression) / (ArithmeticExpression '>>' ArithmeticExpression)

XorExpression <- ArithmeticExpression '^' ArithmeticExpression

BitwiseAndExpression <- ArithmeticExpression ('&' ArithmeticExpression)+

BitwiseOrExpression <- ArithmeticExpression ('|' ArithmeticExpression)+

ComparisonExpression <- EqualExpression / NotEqualExpression / LessEqExpression / GreaterEqExpression / LessThanExpression / GreaterThanExpression / BitwiseOpExpression

EqualExpression <- BitwiseOpExpression '==' BitwiseOpExpression

NotEqualExpression <- BitwiseOpExpression '!=' BitwiseOpExpression

LessEqExpression <- BitwiseOpExpression '<=' BitwiseOpExpression

GreaterEqExpression <- BitwiseOpExpression '>=' BitwiseOpExpression

LessThanExpression <- BitwiseOpExpression '<' BitwiseOpExpression

GreaterThanExpression <- BitwiseOpExpression '>' BitwiseOpExpression

LogicalOpExpression <- LogicalAndExpression / LogicalOrExpression / ComparisonExpression

LogicalAndExpression <- ComparisonExpression ('&&' ComparisonExpression)+

LogicalOrExpression <- ComparisonExpression ('||' ComparisonExpression)+

Expression <- LogicalOpExpression

identifier = "identifier"
constant = "constant"
string_literal = "string_literal"
""".replace(' <- ', ' = ').replace('string-literal', 'string_literal'))


class LegibleParseError(ParseError):
    def line(self):
        return "🤷"

    def column(self):
        return "🤷"


class LegibleIncompleteParseError(IncompleteParseError):
    def line(self):
        return "🤷"

    def column(self):
        return "🤷"


def parse_from_rule(rule, tokens):
    try:
        return rule.parse(tokens)
    except IncompleteParseError as error:
        raise LegibleIncompleteParseError(error.text, error.pos, error.expr)
    except ParseError as error:
        raise LegibleParseError(error.text, error.pos, error.expr)


def parse_header(tokens):
    return parse_from_rule(grammar['HeaderFile'], tokens)


def parse_implementation(tokens):
    return parse_from_rule(grammar['ImplementationFile'], tokens)
