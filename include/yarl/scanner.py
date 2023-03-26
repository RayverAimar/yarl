from yarl.definitions import Lexemes, Tag, lexeme_to_tag, compound_symbols
from yarl.token import Token
from yarl.utils import print_error
import os

class Scanner:
    def __init__(self):
        self.lineno = 1
        self.linecontent = ""
        self.current_atom = ""
        self.text = ""
        self.idx_error = None
    
    def scan(self, filename):
        self.__open_file(filename=filename)
        tokens, errors = self.__get_tokens()
        if errors:
            for error in errors:
                error["filename"] = os.path.abspath(filename)
                print_error(error)
        else:
            line = 1
            for token in tokens:
                if token.line != line:
                    line = token.line
                    print()
                print(token, end=" ")
        print(f"\n\tFinishing scanning, there were {len(errors)} errors")

    def __open_file(self, filename):
        self.text = open(file=filename, mode='r')
    
    def __get_next_char(self):
        self.current_atom = self.text.read(1)
        self.linecontent += self.current_atom
        return self.current_atom

    def __look_back_for(self, atom):
        for i in self.linecontent[-2::-1]:
            if i.isspace():
                continue
            if i == atom:
                return i
            else:
                return None

    def __get_str_start_position(self):
        for i, atom in enumerate(self.linecontent[::-1]):
            if atom == Lexemes.QUOTE:
                return len(self.linecontent) - i - 1
        return None

    def __get_complete_str(self):
        colon_assign = False
        if self.__look_back_for(Lexemes.COLON_ASSIGN):
            colon_assign = True
        self.__get_next_char()
        lexeme = self.current_atom
        while self.current_atom != "\n" and self.current_atom != Lexemes.QUOTE and self.current_atom:
            lexeme+=self.__get_next_char()
        if not self.current_atom or self.current_atom == "\n":
            self.idx_error = self.__get_str_start_position()
            raise SyntaxError("unterminated string literal")
        return Token(lexeme=lexeme[:-1], tag= (Tag.ID if colon_assign else Tag.STR), line=self.lineno)

    def __next_char(self):
        old_line = self.text.tell()
        next_char = self.text.read(1)
        self.text.seek(old_line)
        return next_char
    
    def __skip_line(self):
        while self.current_atom != "\n" and self.current_atom:
            self.current_atom = self.__get_next_char()
        return self.__skip_endl()

    def __skip_endl(self):
        self.lineno += 1
        current_line_text_backup = self.linecontent
        self.linecontent = ""
        return current_line_text_backup

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
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno)

        if lexeme_to_tag.get(lexeme):
            return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno)
        
        if lexeme.isnumeric():
            while self.__next_char().isnumeric():
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            return Token(lexeme=lexeme, tag=Tag.NUM, line=self.lineno)
        
        if lexeme.isalpha():
            while self.__next_char().isalpha() or self.__next_char().isnumeric() or self.__next_char() == '_':
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            if lexeme_to_tag.get(lexeme):
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno)
            return Token(lexeme=lexeme, tag=Tag.ID, line=self.lineno)
        self.idx_error = len(self.linecontent) - 1
        raise SyntaxError("invalid character") # invalid sintax (SyntaxError)

    def __get_tokens(self):
        tokens = []
        errors = []
        while self.__get_next_char():
            try:
                token = self.__get_token()
                if token:
                    tokens.append(token)
            except Exception as ex:
                line_content = self.__skip_line()
                idx_error = self.idx_error
                self.idx_error = None
                errors.append({
                    "msg" : str(ex),
                    "content" : line_content, 
                    "lineno" : self.lineno,
                    "idx_error": idx_error
                    }) # Should skip line for security
                
        return tokens, errors