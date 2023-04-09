class Token(object):
    def __init__(self, lexeme, tag, line):
        self.lexeme = lexeme
        self.tag = tag
        self.line = line
    
    def found_at(self) -> str:
        return "({}, {})".format(self.line, '0')