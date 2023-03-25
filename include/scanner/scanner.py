from definitions import Tag, lexeme_to_tag, compound_symbols
from include.token.token import Token

class Scanner:
    def __init__(self):
        self.current_line = 1
        self.current_line_text = ""
        self.current_atom = ""
        self.text = ""
    
    def scan(self, filename):
        self.__open_file(filename=filename)
        return self.__get_tokens()

    def __open_file(self, filename):
        self.text = open(file=filename, mode='r')
    
    def __get_next_char(self):
        self.current_atom = self.text.read(1)
        self.current_line_text += self.current_atom
        return self.current_atom
    
    def __next_char(self):
        old_line = self.text.tell()
        next_char = self.text.read(1)
        self.text.seek(old_line)
        return next_char
    
    def __skip_endl(self):
        self.current_line += 1
        self.current_line = ""

    def __skip_spaces(self):
        while self.current_atom.isspace():
            self.current_atom = self.__get_next_char()

    def __get_token(self):
        self.__skip_spaces()
        lexeme = self.current_atom

        if compound_symbols.get(lexeme):
            if self.__next_char() == compound_symbols.get(lexeme):
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme))

        if lexeme_to_tag.get(lexeme):
            return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme))
        
        if lexeme.isnumeric():
            while self.__next_char().isnumeric():
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            return Token(lexeme=lexeme, tag=Tag.NUM)
        
        if lexeme.isalpha():
            while self.__next_char().isalpha() or self.__next_char().isnumeric() or self.__next_char() == '_':
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            if lexeme_to_tag.get(lexeme):
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme))
            return Token(lexeme=lexeme, tag=Tag.ID)
        return Token(None, None)

    def __get_tokens(self):
        tokens = []
        while self.__get_next_char():
            token = self.__get_token()
            tokens.append(token)
        return tokens

scanner = Scanner()
tokens = scanner.scan("D:/dev/repositories/yarl/samples/sample.txt")
for token in tokens:
    print(token.lexeme, " ", token.tag)
