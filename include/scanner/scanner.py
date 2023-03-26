from include.scanner.definitions import Lexemes, Tag, lexeme_to_tag, compound_symbols
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

    def __get_complete_str(self):
        self.__get_next_char()
        lexeme = self.current_atom
        while self.current_atom != "\n" and self.current_atom != Lexemes.QUOTE and self.current_atom:
            lexeme+=self.__get_next_char()
        if not self.current_atom:
            raise SyntaxError("Error: EOF while scanning")

        if self.current_atom == "\n":
            raise SyntaxError("Error: EOL while scanning")
        return Token(lexeme=lexeme[:-1], tag=Tag.STR, line=self.current_line)

    def __next_char(self):
        old_line = self.text.tell()
        next_char = self.text.read(1)
        self.text.seek(old_line)
        return next_char
    
    def __skip_line(self):
        while self.current_atom != "\n" and self.current_atom:
            self.current_atom = self.__get_next_char()
        self.__skip_endl()

    def __skip_endl(self):
        self.current_line += 1
        self.current_line_text = ""

    def __skip_spaces(self):
        while self.current_atom.isspace() and self.current_atom:
            if self.current_atom == "\n":
                self.__skip_endl()
            self.current_atom = self.__get_next_char()
            
    def __get_token(self):
        self.__skip_spaces()

        if not self.current_atom: # Not a token neither a lexical error
            return
        
        lexeme = self.current_atom

        if lexeme == Lexemes.EOL_COMMENT: # Comments are not errors
            self.__skip_line()
            return

        if lexeme == Lexemes.QUOTE:
            return self.__get_complete_str()
        
        if compound_symbols.get(lexeme):
            if self.__next_char() == compound_symbols.get(lexeme):
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.current_line)

        if lexeme_to_tag.get(lexeme):
            return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.current_line)
        
        if lexeme.isnumeric():
            while self.__next_char().isnumeric():
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            return Token(lexeme=lexeme, tag=Tag.NUM, line=self.current_line)
        
        if lexeme.isalpha():
            while self.__next_char().isalpha() or self.__next_char().isnumeric() or self.__next_char() == '_':
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            if lexeme_to_tag.get(lexeme):
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.current_line)
            return Token(lexeme=lexeme, tag=Tag.ID, line=self.current_line)
        return Token(None, None, self.current_line)

    def __get_tokens(self):
        tokens = []
        errors = []
        while self.__get_next_char():
            try:
                token = self.__get_token()
                if token:
                    tokens.append(token)
            except Exception as ex:
                errors.append(str(ex)) # Should skip line for security
        return tokens