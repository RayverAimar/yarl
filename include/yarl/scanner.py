from yarl.definitions import Lexemes, Tag, lexeme_to_tag, compound_symbols, INDENT_SIZE
from yarl.token import Token

import os
import math

class Scanner:
    def __init__(self):
        self.lineno = 1
        self.linecontent = ""
        self.current_atom = ""
        self.text = ""
        self.idx = 0
        self.looking_for_indents = True
        self.last_indents = 0
    
    def scan(self, filename):
        self.__open_file(filename=filename)
        return self.__get_tokens()
          
    def __check_for_indents(self):
        self.__skip_spaces(omit_last=False)
        n_indents = math.ceil((self.idx - 1) / INDENT_SIZE)
        delta_indents = n_indents - self.last_indents
        if delta_indents == 0:
            return None
        indents_dedents = []
        self.last_indents = n_indents
        if delta_indents > 0:
            for i in range(delta_indents):
                indents_dedents.append(Token(lexeme="", tag=Tag.INDENT,line=self.lineno, idx=i*INDENT_SIZE+1))
        else:
            delta_indents = abs(delta_indents)
            for i in range(delta_indents):
                indents_dedents.append(Token(lexeme="", tag=Tag.DEDENT,line=self.lineno, idx=i*INDENT_SIZE+1))
        return indents_dedents
        
    def __get_complete_str(self):
        idx = self.idx
        colon_assign = False
        if self.__look_back_for(Lexemes.COLON_ASSIGN):
            colon_assign = True
        self.__get_next_char()
        lexeme = self.current_atom
        while self.current_atom != "\n" and self.current_atom != Lexemes.QUOTE and self.current_atom:
            lexeme+=self.__get_next_char()
        if not self.current_atom or self.current_atom == "\n":
            self.idx = self.__get_str_start_position()
            raise SyntaxError("unterminated string literal")
        return Token(lexeme=lexeme[:-1], tag= (Tag.ID if colon_assign else Tag.STR), line=self.lineno, idx=idx)

    def __get_next_char(self):
        self.current_atom = self.text.read(1)
        self.linecontent += self.current_atom
        self.idx += 1
        return self.current_atom

    def __beginning_line(self):
        return True if len(self.linecontent) == 1 else False

    def __get_str_start_position(self):
        for i, atom in enumerate(self.linecontent[::-1]):
            if atom == Lexemes.QUOTE:
                return len(self.linecontent) - i - 1
        return None

    def __is_valid_line(self): # A valid line may be detected if we find another character different than "#" " " "\n"
        begin = self.text.tell()
        next_char = self.current_atom
        line = ""
        while next_char != "\n" and next_char:
            if next_char != " ":
                line += next_char
            next_char = self.text.read(1)
        self.text.seek(begin)
        if line == "": # Line with only spaces is not a valid line
            return False
        if line[0] == "#": # Line with only line comments is not a valid line
            return False
        return True

    def __get_token(self):
        if self.__beginning_line():
            self.__skip_unvalid_lines()
            if not self.current_atom:
                return
            indents_dedents = self.__check_for_indents()
            if indents_dedents:
                return indents_dedents
        
        self.__skip_spaces()

        if not self.current_atom: # Not a token neither a lexical error
            return

        lexeme = self.current_atom
        idx = self.idx
        
        if lexeme == Lexemes.NEWLINE:
            lineno = self.lineno
            self.__reset_values()
            return Token(lexeme=" ", tag=lexeme_to_tag.get(lexeme), line=lineno, idx=idx)

        if lexeme == Lexemes.EOL_COMMENT: # Comments are not errors
            self.__jump_to_endline()
            return

        if lexeme == Lexemes.QUOTE:
            return self.__get_complete_str()
        
        if compound_symbols.get(lexeme):
            if self.__next_char() == compound_symbols.get(lexeme):
                self.current_atom = self.__get_next_char()
                lexeme+=self.current_atom
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno, idx=idx)

        if lexeme_to_tag.get(lexeme):
            return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno, idx=self.idx)
        
        if lexeme.isnumeric():
            while self.__next_char().isnumeric():
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            return Token(lexeme=lexeme, tag=Tag.NUM, line=self.lineno, idx=idx)
        
        if lexeme.isalpha():
            while self.__next_char().isalpha() or self.__next_char().isnumeric() or self.__next_char() == '_':
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            if lexeme_to_tag.get(lexeme):
                return Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno, idx=idx)
            return Token(lexeme=lexeme, tag=Tag.ID, line=self.lineno, idx=idx)
        self.idx = len(self.linecontent) - 1
        raise SyntaxError("invalid character") # invalid syntax (SyntaxError)

    def __get_tokens(self):
        tokens = []
        errors = []
        while self.__get_next_char():
            try:
                token = self.__get_token()
                if not token:
                    continue
                if type(token) == type(list()):
                    for unique_token in token:
                        tokens.append(unique_token)
                else:
                    tokens.append(token)
            except Exception as ex:
                line_content = self.__jump_to_endline()
                idx_error = self.idx
                self.idx = 0
                errors.append({
                    "msg" : str(ex),
                    "content" : line_content, 
                    "lineno" : self.lineno,
                    "idx_error": idx_error
                    }) # Should skip line for security
        return tokens, errors

    def __look_back_for(self, atom):
        for i in self.linecontent[-2::-1]:
            if i.isspace():
                continue
            if i == atom:
                return i
            else:
                return None

    def __next_char(self):
        old_line = self.text.tell()
        next_char = self.text.read(1)
        self.text.seek(old_line)
        return next_char

    def __open_file(self, filename):
        self.text = open(file=filename, mode='r')

    def __reset_values(self):
        self.lineno += 1
        current_line_text_backup = self.linecontent
        self.idx = 0
        self.linecontent = ""
        self.looking_for_indents = True
        return current_line_text_backup

    def __jump_to_endline(self):
        while self.current_atom != "\n" and self.current_atom:
            self.current_atom = self.__get_next_char()
        return self.__reset_values()
    
    def __skip_spaces(self, omit_last = True):
        while self.current_atom.isspace() and self.current_atom and self.current_atom != "\n":
            self.current_atom = self.__get_next_char()
        if not omit_last:
            last_idx = self.text.tell()
            self.text.seek(last_idx - 1)

    def __skip_unvalid_lines(self):
        while not self.__is_valid_line():
            self.__jump_to_endline()
            if self.current_atom:
                self.__get_next_char()
            else:
                break