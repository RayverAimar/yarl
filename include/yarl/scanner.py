from yarl.definitions import Lexemes, Tag, lexeme_to_tag, compound_symbols, INDENT_SIZE
from yarl.token import Token

class Scanner:
    def __init__(self):
        self.lineno = 1
        self.linecontent = ""
        self.current_atom = ""
        self.text = ""
        self.idx = 0
        self.looking_for_indents = True
        self.last_indents = 0
        self.current_indents = 0
    
    def scan(self, filename):
        self.__open_file(filename=filename)
        return self.__get_tokens()


    def __check_for_indents(self):
        indents_dedents = []
        if(self.idx == (INDENT_SIZE * self.current_indents)+1): # No changes of indentation
            return
        if(self.idx == (INDENT_SIZE * (self.current_indents+1)) + 1 ): # There may only exist one more indentation at most per line
            self.current_indents+=1
            indents_dedents.append(Token(lexeme="", tag=Tag.INDENT,line=self.lineno, idx=INDENT_SIZE+1))
            return indents_dedents
        spaces = self.idx - 1
        if spaces % INDENT_SIZE != 0: # Number of spaces not compatible with fixed INDENT SIZE
            raise SyntaxError("Unindent amount does not match previous indent")
        last_indentation_spaces = (self.current_indents * INDENT_SIZE) + 1
        spaces = last_indentation_spaces - self.idx
        dedents = spaces // INDENT_SIZE
        for i in range(dedents): # Append necessary dedents as there may be more than one per line
            self.current_indents-=1
            indents_dedents.append(Token(lexeme="", tag=Tag.DEDENT, line=self.lineno, idx=(INDENT_SIZE*i)+1))
        return indents_dedents

    def __get_complete_str(self):
        '''
            Returns Token of the complete string if finds its closure, otherwise it may raise SyntaxError
            for not having found closure or having found invalid characters inside string  
        '''
        idx = self.idx
        colon_assign = False
        if self.__look_back_for(Lexemes.COLON_ASSIGN):
            colon_assign = True
        self.__get_next_char()
        lexeme = self.current_atom
        while self.current_atom != "\n" and self.current_atom != Lexemes.QUOTE and self.current_atom:
            if self.__next_char() == '\\':
                self.__get_next_char()
                lexeme+=self.__get_next_char()
                lexeme+=self.__get_next_char()
                continue
            lexeme+=self.__get_next_char()
        
        if not self.current_atom or self.current_atom == "\n":
            self.idx = self.__get_str_start_position()
            raise SyntaxError("unterminated string literal")
        if not all(32 <= ord(char) <= 126 for char in lexeme):
            raise SyntaxError("invalid character in string")
        
        return Token(lexeme=lexeme[:-1], tag= (Tag.ID if colon_assign else Tag.STR), line=self.lineno, idx=idx)

    def __get_next_char(self):
        ''' Returns next char in the buffer '''
        self.current_atom = self.text.read(1)
        self.linecontent += self.current_atom
        self.idx += 1
        return self.current_atom

    def __get_str_start_position(self):
        ''' Returns the starting position of the string for later pointing out of error '''
        for i, atom in enumerate(self.linecontent[::-1]):
            if atom == Lexemes.QUOTE:
                return len(self.linecontent) - i - 1
        return None

    def __is_valid_line(self): # A valid line may be detected if we find another character different than "#" " " "\n"
        ''' 
            Returns True if next line is valid .
            A line is considered 'valid' if it has content different than only line comments, only spaces, only a newline
        '''
        begin = self.text.tell()
        cur_char = self.current_atom
        first_char = ""
        while cur_char != "\n" and cur_char:
            if cur_char != " ":
                first_char = cur_char
                break
            cur_char = self.text.read(1)
        self.text.seek(begin)
        if first_char == "": # Line with only spaces is not a valid line
            return False
        if first_char == "#": # Line with only line comments is not a valid line
            return False
        return True

    def __get_token(self):
        current_tokens = []
        
        if self.current_atom == Lexemes.NEWLINE:
            if len(self.linecontent.strip()) == 0: # Void line
                self.__reset_values()
                return
            lineno = self.lineno
            idx = self.idx
            self.__reset_values()
            current_tokens.append(Token(lexeme=" ", tag='NEWLINE', line=lineno, idx=idx))
            return current_tokens

        if self.current_atom.isspace():
            return

        if len(self.linecontent.strip()) == 1:
            indent_dedents = self.__check_for_indents()
            if indent_dedents:
                for unique_token in indent_dedents:
                    current_tokens.append(unique_token)

        if not self.current_atom: # Not a token neither a lexical error
            return
        
        lexeme = self.current_atom
        idx = self.idx            

        if lexeme == Lexemes.EOL_COMMENT: # Comments are not errors
            lineno = self.lineno
            idx = self.idx
            linecontent = self.linecontent
            self.__jump_to_endline()
            if linecontent.strip()[0] == Lexemes.EOL_COMMENT:
                return current_tokens
            else:
                return Token(lexeme=" ", tag='NEWLINE', line=lineno, idx=idx)

        if lexeme == Lexemes.QUOTE:
            current_tokens.append(self.__get_complete_str())
            return current_tokens
        
        if compound_symbols.get(lexeme):
            if self.__next_char() == compound_symbols.get(lexeme):
                self.current_atom = self.__get_next_char()
                lexeme+=self.current_atom
                current_tokens.append(Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno, idx=idx))
                return current_tokens

        if lexeme_to_tag.get(lexeme):
            current_tokens.append(Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno, idx=self.idx))
            return current_tokens
        
        if lexeme.isnumeric():
            if lexeme == '0' and self.__next_char().isnumeric():
                raise SyntaxError("invalid number")
            while self.__next_char().isnumeric():
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            if (int(lexeme) > 2147483647):
                self.idx -= 1
                raise OverflowError("integer overflow")
            current_tokens.append(Token(lexeme=lexeme, tag=Tag.NUM, line=self.lineno, idx=idx))
            return current_tokens
        
        if lexeme.isalpha():
            while self.__next_char().isalpha() or self.__next_char().isnumeric() or self.__next_char() == '_':
                self.current_atom = self.__get_next_char()
                lexeme += self.current_atom
            if lexeme == 'int':
                current_tokens.append(Token(lexeme=lexeme, tag='INT', line=self.lineno, idx=idx))
                return current_tokens
            if lexeme == Lexemes.BOOL:
                current_tokens.append(Token(lexeme=lexeme, tag='BOOL', line=self.lineno, idx=idx))
                return current_tokens
            if lexeme_to_tag.get(lexeme):
                current_tokens.append(Token(lexeme=lexeme, tag=lexeme_to_tag.get(lexeme), line=self.lineno, idx=idx))
                return current_tokens
            current_tokens.append(Token(lexeme=lexeme, tag=Tag.ID, line=self.lineno, idx=idx))
            return current_tokens
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
                idx_error = self.idx
                line_content = self.__jump_to_endline()
                tokens.append(Token(lexeme=" ", tag='NEWLINE', line=self.lineno, idx=self.idx))
                errors.append({
                    "msg" : str(ex),
                    "content" : line_content[::], 
                    "lineno" : self.lineno,
                    "idx_error": idx_error if idx_error > 0 else idx_error
                    }) # Should skip line for security
        # Check if theres a NEWLINE at the end of the code
        if tokens[-1].tag != Tag.NEWLINE:
            tokens.append(Token(lexeme=" ", tag='NEWLINE', line=self.lineno, idx=self.idx))
        
        # Check if there were pending DEDENTS
        if self.current_indents > 0:
            for i in range(self.current_indents):
                tokens.append(Token(lexeme="", tag=Tag.DEDENT, line=self.lineno + 1, idx=(INDENT_SIZE*i)+1))
        return tokens, errors

    def __look_back_for(self, atom):
        ''' 
            Look for the index of a certain character
            Args:
                atom : char
            Returns:
                Index of atom if found
        '''
        for i in self.linecontent[-2::-1]:
            if i.isspace():
                continue
            if i == atom:
                return i
            else:
                return None

    def __next_char(self):
        ''' Peeks next char '''
        old_line = self.text.tell()
        next_char = self.text.read(1)
        self.text.seek(old_line)
        return next_char

    def __open_file(self, filename):
        self.text = open(file=filename, mode='r')

    def __reset_values(self):
        ''' 
            Once current_atom reaches the end of line, it will make reset all values in the scanner
            Returns:
                previous line content
        '''
        self.lineno += 1
        current_line_text_backup = self.linecontent
        self.idx = 0
        self.linecontent = ""
        self.looking_for_indents = True
        return current_line_text_backup

    def __jump_to_endline(self):
        '''
            Skips current line
            Returns: Previous line content
        '''
        while self.current_atom != "\n" and self.current_atom:
            self.current_atom = self.__get_next_char()
        return self.__reset_values()
    
    def __skip_spaces(self, omit_last = True):
        '''
            Skip only spaces in a line and reachs up to a next valid/unvalid character
            Args:
                omit_last : bool
                    If set True, it also skips the next character different than spaces (useful for skipping newlines)
        '''
        while self.current_atom.isspace() and self.current_atom and self.current_atom != "\n":
            self.current_atom = self.__get_next_char()
        if not omit_last:
            last_idx = self.text.tell()
            self.text.seek(last_idx - 1)

    def __skip_unvalid_lines(self):
        '''
            Check if next line is valid and skip it if it's not
        '''
        while not self.__is_valid_line():
            self.__jump_to_endline()
            if self.__next_char():
                self.__get_next_char()
            else:
                break
