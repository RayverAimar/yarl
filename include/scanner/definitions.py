
class Lexemes:
    AND = "and"
    ARROW_ASSIGN = "->"
    AS = "as"
    ASSERT = "assert"
    ASSIGN = "="
    ASYNC = "async"
    AWAIT = "await"
    BREAK = "break"
    CLASS = "class"
    COLON = ":"
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
    QUOTE = ' " '
    RAISE = "raise"
    RSBRACKET = "]"
    RPAREN = ")"
    RETURN = "return"
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
    DIFF = "ARITHMETIC_OPERATOR"
    DIV_INT = "ARITHMETIC_OPERATOR"
    DIV_FLOAT = "ARITHMETIC_OPERATOR"
    ID = "ID"
    MULT = "ARITHMETIC_OPERATOR"
    NUM = "NUM"
    STR = "STR"
    SUM = "ARITHMETIC_OPERATOR"


lexeme_to_tag = {
    Lexemes.AND: Tag.AND,
    Lexemes.ARROW_ASSIGN : Tag.ARROW_ASSIGN,
    Lexemes.ASSIGN : Tag.ASSIGN,
    Lexemes.DIFF : Tag.DIFF,
    Lexemes.MULT : Tag.MULT,
    Lexemes.SUM : Tag.SUM,
}