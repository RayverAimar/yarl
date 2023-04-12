class Token(object):
    def __init__(self, lexeme, tag, line, idx):
        self.lexeme = lexeme
        self.tag = tag
        self.line = line
        self.idx = idx
    
    def found_at(self) -> str:
        return "({}, {})".format(self.line, '0')