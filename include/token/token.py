class Token(object):
    def __init__(self, lexeme, tag, line):
        self.lexeme = lexeme
        self.tag = tag
        self.line = line
    
    def __str__(self) -> str:
        return "<{}, {}, {}>".format(self.lexeme, self.tag, self.line)