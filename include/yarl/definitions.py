
class Lexemes:
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
    ML_COMMENT = '"""'
    MOD = "%"
    MULT = "*"
    NE = "!="
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
    BIN_OPERATOR = "BIN_OPERATOR"
    BIN_VALUE = "BIN_VALUE"
    COLON_ASSIGN = "COLON_ASSIGN"
    COMMA = "COMMA"
    COMPARISON_OPERATOR = "COMPARISON_OPERATOR"
    EOL_COMMENT = "EOL_COMMENT"
    ID = "ID"
    KEYWORD = "KEYWORD"
    LSBRACKET = "LSBRACKET"
    LPAREN = "LPAREN"
    ML_COMMENT = "ML_COMMENT"
    NUM = "NUM"
    QUOTE = "QUOTE"
    RSBRACKET = "RSBRACKET"
    RPAREN = "RPAREN"
    STR = "STR"


lexeme_to_tag = {
    Lexemes.AND:            Tag.BIN_OPERATOR,
    Lexemes.ARROW_ASSIGN:   Tag.ARROW_ASSIGN,
    Lexemes.AS:             Tag.ASSIGN,
    Lexemes.ASSIGN:         Tag.ASSIGN,
    Lexemes.ASYNC:          Tag.KEYWORD,
    Lexemes.AWAIT:          Tag.KEYWORD,
    Lexemes.BOOL:           Tag.ID,
    Lexemes.BREAK:          Tag.KEYWORD,
    Lexemes.CLASS:          Tag.KEYWORD,
    Lexemes.COLON_ASSIGN:   Tag.COLON_ASSIGN,
    Lexemes.COMMA:          Tag.COMMA,
    Lexemes.CONTINUE:       Tag.KEYWORD,
    Lexemes.DEF:            Tag.KEYWORD,
    Lexemes.DEL:            Tag.KEYWORD,
    Lexemes.DIFF:           Tag.ARITHMETIC_OPERATOR,
    Lexemes.DIV_FLOAT:      Tag.ARITHMETIC_OPERATOR,
    Lexemes.DIV_INT:        Tag.ARITHMETIC_OPERATOR,
    Lexemes.EQ:             Tag.COMPARISON_OPERATOR,
    Lexemes.ELIF:           Tag.KEYWORD,
    Lexemes.ELSE:           Tag.KEYWORD,
    Lexemes.EOL_COMMENT:    Tag.EOL_COMMENT,
    Lexemes.EXCEPT:         Tag.KEYWORD,
    Lexemes.FALSE:          Tag.ID,
    Lexemes.FINALLY:        Tag.KEYWORD,
    Lexemes.FOR:            Tag.KEYWORD,
    Lexemes.GLOBAL:         Tag.KEYWORD,
    Lexemes.GE:             Tag.COMPARISON_OPERATOR,
    Lexemes.GT:             Tag.COMPARISON_OPERATOR,
    Lexemes.IF:             Tag.KEYWORD,
    Lexemes.IMPORT:         Tag.KEYWORD,
    Lexemes.IN:             Tag.KEYWORD,
    Lexemes.INT:            Tag.ID,
    Lexemes.IS:             Tag.KEYWORD,
    Lexemes.LAMBDA:         Tag.KEYWORD,
    Lexemes.LSBRACKET:      Tag.LSBRACKET,
    Lexemes.LE:             Tag.COMPARISON_OPERATOR,
    Lexemes.LPAREN:         Tag.LPAREN,
    Lexemes.LT:             Tag.COMPARISON_OPERATOR,
    Lexemes.ML_COMMENT:     Tag.ML_COMMENT,
    Lexemes.MOD:            Tag.ARITHMETIC_OPERATOR,
    Lexemes.MULT:           Tag.ARITHMETIC_OPERATOR,
    Lexemes.NE:             Tag.COMPARISON_OPERATOR,
    Lexemes.NONE:           Tag.KEYWORD,
    Lexemes.NONLOCAL:       Tag.KEYWORD,
    Lexemes.NOT:            Tag.BIN_OPERATOR,
    Lexemes.OR:             Tag.BIN_OPERATOR,
    Lexemes.PASS:           Tag.KEYWORD,
    Lexemes.PRINT:          Tag.ID,
    Lexemes.QUOTE:          Tag.QUOTE,
    Lexemes.RAISE:          Tag.KEYWORD,
    Lexemes.RSBRACKET:      Tag.RSBRACKET,
    Lexemes.RPAREN:         Tag.RPAREN,
    Lexemes.RETURN:         Tag.KEYWORD,
    Lexemes.STR:            Tag.STR,
    Lexemes.SUM:            Tag.ARITHMETIC_OPERATOR,
    Lexemes.TRUE:           Tag.ID,
    Lexemes.TRY:            Tag.KEYWORD,
    Lexemes.WHILE:          Tag.KEYWORD,
    Lexemes.WITH:           Tag.KEYWORD,
    Lexemes.YIELD:          Tag.KEYWORD
}

compound_symbols = {
    "!" : Lexemes.ASSIGN,
    Lexemes.ASSIGN : Lexemes.ASSIGN,
    Lexemes.GT : Lexemes.ASSIGN,
    Lexemes.LT : Lexemes.ASSIGN,
    Lexemes.DIFF : Lexemes.GT
}