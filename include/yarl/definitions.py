
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
    AND = "BIN_OPERATOR"
    ARROW_ASSIGN = "ARROW_ASSIGN"
    ASSIGN = "ASSIGN"
    AS = "AS"
    COLON_ASSIGN = "COLON_ASSIGN"
    DIFF = "ARITHMETIC_OPERATOR"
    DIV_INT = "ARITHMETIC_OPERATOR"
    DIV_FLOAT = "ARITHMETIC_OPERATOR"
    ID = "IDENTIFIER"
    MULT = "ARITHMETIC_OPERATOR"
    NUM = "NUM"
    STR = "STR"
    SUM = "ARITHMETIC_OPERATOR"


lexeme_to_tag = {
    Lexemes.AND: Tag.AND,
    Lexemes.ARROW_ASSIGN : Tag.ARROW_ASSIGN,
    Lexemes.ASSIGN : Tag.ASSIGN,
    Lexemes.BOOL : Tag.ID,
    Lexemes.COLON_ASSIGN : Tag.COLON_ASSIGN,
    Lexemes.DIFF : Tag.DIFF,
    Lexemes.INT : Tag.ID,
    Lexemes.MULT : Tag.MULT,
    Lexemes.SUM : Tag.SUM
}

compound_symbols = {
    "!" : Lexemes.ASSIGN,
    Lexemes.ASSIGN : Lexemes.ASSIGN,
    Lexemes.GT : Lexemes.ASSIGN,
    Lexemes.LT : Lexemes.ASSIGN,
}