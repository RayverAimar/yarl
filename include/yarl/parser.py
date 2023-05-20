from yarl.definitions import Tag, Lexemes, first

class RecursiveDescentParser:
    def __init__(self, grammar, epsilon, eof):
        self.current_token = ""
        self.grammar = grammar
        self.epsilon = epsilon
        self.eof = eof
        self.error = ""
    
    def program(self):
        if self.current_token not in first["DefList"]:
            return self.error
        self.DefList()

    def next_token(self):
        pass

    def DefList(self):
        if self.current_token in first["Def"]:
            self.Def()
        
    
    def Def(self):
        if self.current_token != Lexemes.DEF:
            return self.error
        self.next_token()
        if self.current_token != Tag.ID:
            return self.error
        self.next_token()
        if self.current_token != Lexemes.LPAREN:
            return self.error
        if self.current_token not in first["TypedVarList"]:
            return self.error
        self.TypedVarList()
    
    def TypedVarList(self):
        pass

    def defs(self):
        '''
        if(cur_token in first(var_def))
            self.var_def()
        else if(cur_token in first(func_def))
            self.func_def()
        else if(cur_token in first(class_def))
            self.class_def()
        else Nothing # It is not an error as it may be epsilon
        '''
        
        self.insider_defs()
        self.class_def()
        pass

    def var_def(self):
        pass

    def func_def(self):
        '''
        if self.current_token != Token.def:
            return error
        self.get_next_token()
        if self.current_token != Token.ID:
            return error #Expected ID, found self.current_token
        self.get_next_token()
        if self.current_token != Token.OPEN_PARENTHESES:
            return error
        self.get_next_token()
        if not self.typed_var_list():
            return error
        self.get_next_token()
        if self.current_token != Token.CLOSE_PARENTHESES:
            return error
        if self.current_token == "->":
            self.get_next_token()
            if not self.type()
                return error
            self.get_next_token()
        if self.current_token != ':':
            return error
        self.get_next_token()
        if self.current_token != Token.NEWLINE:
            return error
        self.get_next_token()
        if self.current_token != Token.INDENT:
            return error
        self.get_next_token()
        self.func_body()
        if self.current_token != Token.DEDENT:
            return error     
        self.get_next_token()   
        '''
        pass

    def func_body(self):
        '''
        while self.current_token in first([global_decl, nonlocal_decl, var_def, func_def]):
            if self.current_token == first(global_decl):
                self.global_decl()
            elif self.current_token == first(nonlocal_decl):
                self.nonlocal_decl()
            elif self.current_token == first(var_def):
                self.var_def()
            elif self.current_token == first(func_def):
                self.func_def()
        if not self.stmt()
            return error
        while self.current_token in first(stmt):
            if not self.stmt():
                return error
        '''
        pass

    def stmt(self):
        '''
        if self.current_token in first(simple_stmt):
            self.simple_stmt()
            if self.current_token != Token.NEWLINE:
                return error
        elif self.current_token in first(if_stmt):
            self.if_stmt():
        elif self.current_token in first(while_stmt):
            self.while_stmt()
        elif self.current_token in first(for_stmt):
            self.for_stmt()
        '''

    def insider_defs(self):
        pass

    def class_def(self):
        pass

