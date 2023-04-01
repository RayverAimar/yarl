class Token(object):
    def __init__(self, lexeme, tag, line, idx):
        self.lexeme = lexeme
        self.tag = tag
        self.line = line
        self.idx = idx
    
    def __str__(self) -> str:
        return "{}, {}, {}".format(self.lexeme, self.tag, self.line)