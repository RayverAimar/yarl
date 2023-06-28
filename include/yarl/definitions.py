
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

first = {
    "Program": ["$", Lexemes.DEF, Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.IF, Lexemes.WHILE, Lexemes.FOR, Lexemes.PASS, Lexemes.RETURN],
    "DefList": [Lexemes.DEF],
    "StatementList": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.IF, Lexemes.WHILE, Lexemes.FOR, Lexemes.PASS, Lexemes.RETURN],
    "Def": [Lexemes.DEF],
    "TypedVarList": [Tag.ID],
    "Type": [Lexemes.INT, Lexemes.STR, Lexemes.LSBRACKET],
    "TypedVar": [Tag.ID],
    "Return": [Lexemes.INT, Lexemes.STR, Lexemes.LSBRACKET],
    "Block": ["NEWLINE"],
    "TypedVarListTail": [Lexemes.COMMA],
    "Statement": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.IF, Lexemes.WHILE, Lexemes.FOR, Lexemes.PASS, Lexemes.RETURN],
    "SimpleStatement": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.PASS, Lexemes.RETURN],
    "Expr": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.ARROW_ASSIGN],
    "ElifList": [Lexemes.ELIF],
    "Else": [Lexemes.ELSE],
    "Elif": [Lexemes.ELIF],
    "SSTail": [Lexemes.EQUAL],
    "ReturnExpr": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET],
    "orExpr": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET],
    "ExprPrime": [Lexemes.IF],
    "andExpr": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET],
    "orExprPrime": [Lexemes.OR],
    "notExpr": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET],
    "andExprPrime": [Lexemes.AND],
    "CompExpr": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "notExprPrime": [Lexemes.NOT],
    "IntExpr": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "CompExprPrime": [],
    "CompOp": ["==", "!=", "<", ">", "<=", ">=", "is"],
    "Term": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "IntExprPrime": [Lexemes.ADD, Lexemes.MINUS],
    "Factor": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET, Lexemes.MINUS],
    "TermPrime": [Lexemes.MULT, Lexemes.DIV_INT, Lexemes.MOD],
    "Name": [Tag.ID],
    "Literal": ["None", "True", "False", "INTEGER", "STRING"],
    "List": [Lexemes.LSBRACKET],
    "NameTail": [Lexemes.LSBRACKET, Lexemes.LPAREN],
    "ExprList": [Tag.ID, Lexemes.LPAREN, Lexemes.LSBRACKET],
    "ExprListTail": [Lexemes.COMMA],
}

INDENT_SIZE = 4