
class Lexemes:
    ADD = "+"
    AND = "and"
    ARROW_ASSIGN = "->"
    AS = "as"
    ASSERT = "assert"
    ASSIGN = "="
    ASYNC = "async"
    AWAIT = "await"
    BOOL = "bool"
    BREAK = "break"
    CLASS = "class"
    COLON_ASSIGN = ":"
    COMMA = ","
    CONTINUE = "continue"
    DEF = "def"
    DEL = "del"
    DIFF = "-"
    DIV_FLOAT = "/"
    DIV_INT = "//"
    EQ = "=="
    EQUAL = "="
    ELIF = "elif"
    ELSE = "else"
    EOL_COMMENT = "#"
    EXCEPT = "except"
    FALSE = "False"
    FINALLY = "finally"
    FOR = "for"
    FROM = "from"
    GLOBAL = "global"
    GE = ">="
    GT = ">"
    IF = "if"
    IMPORT = "import"
    IN = "in"
    INT = "int"
    IS = "is"
    LAMBDA = "lambda"
    LSBRACKET = "["
    LE = "<="
    LPAREN = "("
    LT = "<"
    MINUS = "-"
    ML_COMMENT = '"""'
    MOD = "%"
    MULT = "*"
    NE = "!="
    NEWLINE = "\n"
    NONE = "None"
    NONLOCAL = "nonlocal"
    NOT = "not"
    OR = "or"
    PASS = "pass"
    PRINT = "print"
    QUOTE = '"'
    RAISE = "raise"
    RSBRACKET = "]"
    RPAREN = ")"
    RETURN = "return"
    STR = "str"
    SUM = "+"
    TRUE = "True"
    TRY = "try"
    WHILE = "while"
    WITH = "with"
    YIELD = "yield"

class Tag:
    ARITHMETIC_OPERATOR = "ARITHMETIC_OPERATOR"
    ARROW_ASSIGN = "ARROW_ASSIGN"
    AS = "AS"
    ASSIGN = "ASSIGN"
    ASYNC = "ASYNC"
    AWAIT = "AWAIT"
    BIN_OPERATOR = "BIN_OPERATOR"
    BIN_VALUE = "BIN_VALUE"
    BREAK = "BREAK"
    CLASS = "CLASS"
    CONTINUE = "CONTINUE"
    COLON_ASSIGN = "COLON_ASSIGN"
    COMMA = "COMMA"
    COMPARISON_OPERATOR = "COMPARISON_OPERATOR"
    DEDENT = "DEDENT"
    DEF = "DEF"
    DEL = "DEL"
    ELIF = "ELIF"
    ELSE = "ELSE"
    EOL_COMMENT = "EOL_COMMENT"
    EXCEPT = "EXCEPT"
    FINALLY = "FINALLY"
    FOR = "FOR"
    GLOBAL = "GLOBAL"
    ID = "ID"
    IF = "IF"
    IMPORT = "IMPORT"
    IN = "IN"
    INDENT = "INDENT"
    IS = "IS"
    LAMBDA = "LAMBDA"
    LSBRACKET = "LSBRACKET"
    LPAREN = "LPAREN"
    ML_COMMENT = "ML_COMMENT"
    NEWLINE = "NEWLINE"
    NONE = "NONE"
    NONLOCAL = "NONLOCAL"
    NUM = "NUM"
    PASS = "PASS"
    QUOTE = "QUOTE"
    RAISE = "RAISE"
    RETURN = "RETURN"
    RSBRACKET = "RSBRACKET"
    RPAREN = "RPAREN"
    STR = "STR"
    TRY = "TRY"
    WHILE = "WHILE"
    WITH = "WITH"
    YIELD = "YIELD"

lexeme_to_tag = {
    Lexemes.AND:            Tag.BIN_OPERATOR,
    Lexemes.ARROW_ASSIGN:   Tag.ARROW_ASSIGN,
    Lexemes.AS:             Tag.ASSIGN,
    Lexemes.ASSIGN:         Tag.ASSIGN,
    Lexemes.ASYNC:          Tag.ASYNC,
    Lexemes.AWAIT:          Tag.AWAIT,
    Lexemes.BOOL:           Tag.ID,
    Lexemes.BREAK:          Tag.BREAK,
    Lexemes.CLASS:          Tag.CLASS,
    Lexemes.COLON_ASSIGN:   Tag.COLON_ASSIGN,
    Lexemes.COMMA:          Tag.COMMA,
    Lexemes.CONTINUE:       Tag.CONTINUE,
    Lexemes.DEF:            Tag.DEF,
    Lexemes.DEL:            Tag.DEL,
    Lexemes.DIFF:           Tag.ARITHMETIC_OPERATOR,
    Lexemes.DIV_FLOAT:      Tag.ARITHMETIC_OPERATOR,
    Lexemes.DIV_INT:        Tag.ARITHMETIC_OPERATOR,
    Lexemes.EQ:             Tag.COMPARISON_OPERATOR,
    Lexemes.ELIF:           Tag.ELIF,
    Lexemes.ELSE:           Tag.ELSE,
    Lexemes.EOL_COMMENT:    Tag.EOL_COMMENT,
    Lexemes.EXCEPT:         Tag.EXCEPT,
    Lexemes.FALSE:          Tag.ID,
    Lexemes.FINALLY:        Tag.FINALLY,
    Lexemes.FOR:            Tag.FOR,
    Lexemes.GLOBAL:         Tag.GLOBAL,
    Lexemes.GE:             Tag.COMPARISON_OPERATOR,
    Lexemes.GT:             Tag.COMPARISON_OPERATOR,
    Lexemes.IF:             Tag.IF,
    Lexemes.IMPORT:         Tag.IMPORT,
    Lexemes.IN:             Tag.IN,
    Lexemes.INT:            Tag.ID,
    Lexemes.IS:             Tag.IS,
    Lexemes.LAMBDA:         Tag.LAMBDA,
    Lexemes.LSBRACKET:      Tag.LSBRACKET,
    Lexemes.LE:             Tag.COMPARISON_OPERATOR,
    Lexemes.LPAREN:         Tag.LPAREN,
    Lexemes.LT:             Tag.COMPARISON_OPERATOR,
    Lexemes.ML_COMMENT:     Tag.ML_COMMENT,
    Lexemes.MOD:            Tag.ARITHMETIC_OPERATOR,
    Lexemes.MULT:           Tag.ARITHMETIC_OPERATOR,
    Lexemes.NE:             Tag.COMPARISON_OPERATOR,
    Lexemes.NEWLINE:        Tag.NEWLINE,
    Lexemes.NONE:           Tag.NONE,
    Lexemes.NONLOCAL:       Tag.NONLOCAL,
    Lexemes.NOT:            Tag.BIN_OPERATOR,
    Lexemes.OR:             Tag.BIN_OPERATOR,
    Lexemes.PASS:           Tag.PASS,
    Lexemes.PRINT:          Tag.ID,
    Lexemes.QUOTE:          Tag.QUOTE,
    Lexemes.RAISE:          Tag.RAISE,
    Lexemes.RSBRACKET:      Tag.RSBRACKET,
    Lexemes.RPAREN:         Tag.RPAREN,
    Lexemes.RETURN:         Tag.RETURN,
    Lexemes.STR:            Tag.STR,
    Lexemes.SUM:            Tag.ARITHMETIC_OPERATOR,
    Lexemes.TRUE:           Tag.ID,
    Lexemes.TRY:            Tag.TRY,
    Lexemes.WHILE:          Tag.WHILE,
    Lexemes.WITH:           Tag.WITH,
    Lexemes.YIELD:          Tag.YIELD
}

compound_symbols = {
    "!" : Lexemes.ASSIGN,
    Lexemes.ASSIGN : Lexemes.ASSIGN,
    Lexemes.GT : Lexemes.ASSIGN,
    Lexemes.LT : Lexemes.ASSIGN,
    Lexemes.DIFF : Lexemes.GT
}

'''
FIRST[Program] = $ def if while for pass return -->
FIRST[DefList] = def
FIRST[StatementList] = if while for pass return -->
FIRST[Def] = def
FIRST[TypedVarList] = ID
FIRST[Return] = int str [
FIRST[Block] = NEWLINE
FIRST[TypedVar] = ID
FIRST[Type] = int str [
FIRST[TypedVarListTail] = ,
FIRST[Statement] = if while for pass return -->
FIRST[SimpleStatement] = pass return -->
FIRST[Expr] = -->
FIRST[ElifList] = elif
FIRST[Else] = else
FIRST[Elif] = elif
FIRST[SSTail] = =
FIRST[ReturnExpr] = -->
FIRST[orExpr] = -->
FIRST[ExprPrime] = if
FIRST[andExpr] = -->
FIRST[orExprPrime] = or
FIRST[notExpr] = -->
FIRST[andExprPrime] = and
FIRST[CompExpr] = ID ( [ -
FIRST[notExprPrime] = not
FIRST[IntExpr] = ID ( [ -
FIRST[CompExprPrime] =
FIRST[CompOp] =
FIRST[Term] = ID ( [ -
FIRST[IntExprPrime] = + -
FIRST[Factor] = ID ( [ -
FIRST[TermPrime] = *
FIRST[//] =
FIRST[%] =
FIRST[Name] = ID
FIRST[Literal] =
FIRST[List] = [
FIRST[NameTail] = ( [
FIRST[ExprList] = -->
FIRST[None] =
FIRST[True] =
FIRST[False] =
FIRST[INTEGER] =
FIRST[STRING] =
FIRST[ExprListTail] = ,
FIRST[==] =
FIRST[!=] =
FIRST[<] =
FIRST[>] =
FIRST[<=] =
FIRST[>=] =
FIRST[is] =
'''

'''
FIRST[Program] = def ID ( [ if while for pass return -
FIRST[DefList] = def
FIRST[StatementList] = ID ( [ if while for pass return -
FIRST[Def] = def
FIRST[TypedVarList] = ID
FIRST[Return] = ->Type
FIRST[Block] = NEWLINE
FIRST[TypedVar] = ID
FIRST[Type] = int str [
FIRST[TypedVarListTail] = ,
FIRST[Statement] = ID ( [ if while for pass return -
FIRST[SimpleStatement] = ID ( [ pass return -
FIRST[Expr] = ID ( [ -
FIRST[ElifList] = elif
FIRST[Else] = else
FIRST[Elif] = elif
FIRST[SSTail] = =
FIRST[ReturnExpr] = ID ( [ -
FIRST[orExpr] = ID ( [ -
FIRST[ExprPrime] = if
FIRST[andExpr] = ID ( [ -
FIRST[orExprPrime] = or
FIRST[notExpr] = ID ( [ -
FIRST[andExprPrime] = and
FIRST[CompExpr] = ID ( [ -
FIRST[notExprPrime] = not
FIRST[IntExpr] = ID ( [ -
FIRST[CompExprPrime] =
FIRST[CompOp] =
FIRST[Term] = ID ( [ -
FIRST[IntExprPrime] = + -
FIRST[Factor] = ID ( [ -
FIRST[TermPrime] = * //
FIRST[%] =
FIRST[Name] = ID
FIRST[Literal] =
FIRST[List] = [
FIRST[NameTail] = ( [
FIRST[ExprList] = ID ( [ -
FIRST[None] =
FIRST[True] =
FIRST[False] =
FIRST[INTEGER] =
FIRST[STRING] =
FIRST[ExprListTail] = ,
FIRST[==] =
FIRST[!=] =
FIRST[<] =
FIRST[>] =
FIRST[<=] =
FIRST[>=] =
FIRST[is] =
FOLLOW[Program] =
FOLLOW[DefList] = ID ( [ if while for pass return -
FOLLOW[StatementList] = DEDENT
FOLLOW[Def] = def ID ( [ if while for pass return -
FOLLOW[TypedVarList] = )
FOLLOW[Return] = :
FOLLOW[Block] = def ID ( [ DEDENT if while for elif else pass return -
FOLLOW[TypedVar] = ) ,
FOLLOW[Type] = ) ] ,
FOLLOW[TypedVarListTail] = )
FOLLOW[Statement] = ID ( [ DEDENT if while for pass return -
FOLLOW[SimpleStatement] = NEWLINE
FOLLOW[Expr] = ) : , NEWLINE =
FOLLOW[ElifList] = ID ( [ DEDENT if while for else pass return -
FOLLOW[Else] = ID ( [ DEDENT if while for pass return -
FOLLOW[Elif] = ID ( [ DEDENT if while for elif else pass return -
FOLLOW[SSTail] = NEWLINE
FOLLOW[ReturnExpr] = NEWLINE
FOLLOW[orExpr] = ) : , NEWLINE if =
FOLLOW[ExprPrime] = ) : , NEWLINE =
FOLLOW[andExpr] = ) : , NEWLINE if else = or
FOLLOW[orExprPrime] = ) : , NEWLINE if =
FOLLOW[notExpr] = ) : , NEWLINE if else = or and
FOLLOW[andExprPrime] = ) : , NEWLINE if else = or
FOLLOW[CompExpr] = ) : , NEWLINE if else = or and not
FOLLOW[notExprPrime] = ) : , NEWLINE if else = or and
FOLLOW[IntExpr] = ) : , NEWLINE if else = or and not
FOLLOW[CompExprPrime] = ) : , NEWLINE if else = or and not
FOLLOW[CompOp] = ID ( [ -
FOLLOW[Term] = ) : , NEWLINE if else = or and not + -
FOLLOW[IntExprPrime] = ) : , NEWLINE if else = or and not
FOLLOW[Factor] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[TermPrime] = ) : , NEWLINE if else = or and not + -
FOLLOW[%] = ID ( [ -
FOLLOW[Name] =
FOLLOW[Literal] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[List] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[NameTail] =
FOLLOW[ExprList] =
FOLLOW[None] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[True] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[False] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[INTEGER] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[STRING] = ) : , NEWLINE if else = or and not + - * //
FOLLOW[ExprListTail] =
FOLLOW[==] =
FOLLOW[!=] =
FOLLOW[<] = ID ( [ -
FOLLOW[>] = ID ( [ -
FOLLOW[<=] = ID ( [ -
FOLLOW[>=] = ID ( [ -
FOLLOW[is] = ID ( [ -
'''

first = {
    "Program" : ["$", Lexemes.DEF, Lexemes.IF, Lexemes.WHILE, Lexemes.FOR, Lexemes.PASS, Lexemes.RETURN],
    "DefList" : [Lexemes.DEF],
    "StatementList" : [Lexemes.IF, Lexemes.WHILE, Lexemes.FOR, Lexemes.PASS, Lexemes.RETURN],
    "Def" : [Lexemes.DEF],
    "TypedVarList" : [Tag.ID],
    "Type" : [Lexemes.INT, Lexemes.STR, Lexemes.LSBRACKET],
    "TypedVar" : [Tag.ID],
    "Return" : [Lexemes.INT, Lexemes.STR, Lexemes.LSBRACKET],
    "Block" : ["NEWLINE"],
    "TypedVarListTail" : [Lexemes.COMMA],
    "Statement" : [Lexemes.IF, Lexemes.WHILE, Lexemes.FOR, Lexemes.PASS, Lexemes.RETURN],
    "SimpleStatement" : [Lexemes.PASS, Lexemes.RETURN],
    "Expr" : [Lexemes.ARROW_ASSIGN],
    "ElifList" : [Lexemes.ELIF],
    "Else" : [Lexemes.ELSE],
    "Elif" : [Lexemes.ELIF],
    "SSTail" : [Lexemes.EQUAL],
    "ReturnExpr" : [],
    "orExpr" : [],
    "ExprPrime" : [Lexemes.IF],
    "andExpr" : [],
    "orExprPrime" : [Lexemes.OR],
    "notExpr" : [],
    "andExprPrime" : [Lexemes.AND],
    "CompExpr" : [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "notExprPrime" : [Lexemes.NOT],
    "IntExpr" : [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "CompExprPrime" : [],
    "CompOp" : [],
    "Term" : [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "IntExprPrime" : [Lexemes.ADD, Lexemes.MINUS],
    "Factor" : [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "TermPrime" : [Lexemes.MULT],
    "//" : [],
    "%" : [],
    "Name" : [Tag.ID],
    "Literal" : [],
    "List" : ["["],
    "NameTail" : [Lexemes.LSBRACKET, Lexemes.LPAREN],
    "ExprList" : [],
    "ExprListTail" : [Lexemes.COMMA]
}

INDENT_SIZE = 4