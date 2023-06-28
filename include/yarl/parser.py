from yarl.definitions import Tag, Lexemes, first
from yarl.scanner import Scanner

class RecursiveDescentParser:
    def __init__(self, eof, file_path):
        self.buffer = []
        self.scanner = Scanner()
        tokens, errors = self.scanner.scan(file_path)
        for token in tokens:
            print(token.lexeme, token.tag)
        for i in range(len(tokens)):
            if tokens[i].tag == Tag.ID:
                self.buffer.append(Tag.ID)
            elif tokens[i].tag == Tag.NEWLINE:
                self.buffer.append(Tag.NEWLINE)
            elif tokens[i].tag == Tag.INDENT:
                self.buffer.append(Tag.INDENT)
            elif tokens[i].tag == Tag.DEDENT:
                self.buffer.append(Tag.DEDENT)
            elif tokens[i].tag == Tag.NUM:
                self.buffer.append("INTEGER")
            elif tokens[i].tag == Tag.STR:
                self.buffer.append("STRING")
            else:
                self.buffer.append(tokens[i].lexeme)
        print(self.buffer)
        self.eof = "$"
        self.error = ""
        #self.buffer = ["def","ID","ID",":","int",",","ID",":","int",")","->","int",":","NEWLINE","INDENT","return","ID","+","ID"]
        self.index = 0
        self.current_token = self.buffer[self.index]
        self.errors = []
        self.lineno = 1
        self.recovery = False
    
    def parse(self):
        parsing = self.program()
        if parsing:
            print("There were errors!")
            

    def add_error(self, message, func):
        message=message+str(self.lineno)
        self.errors.append(message)
        #find newline in buffer
        #find newline in non terminal methods
        #self.recovery = True
        while self.current_token != Tag.NEWLINE and self.index < len(self.buffer):
            self.next_token()
        return func()

    def program(self): #Done
        while self.current_token in first["DefList"]:
            self.Def()
            self.next_token()
            
        while self.current_token in first["StatementList"]:
            self.StatementList()
            self.next_token()
        
        if self.current_token != self.eof:
            return self.error

        if self.errors:
            print("\n--> Incorrect Program")
            for error in self.errors:
                print(error)
        else:
            print("\n--> Accepted Program")

    def next_token(self):
        if self.index <= len(self.buffer):
            print(self.current_token, end=" ")
        self.index+=1
        if self.index >= len(self.buffer):
            self.current_token = self.eof
        else:
            self.current_token = self.buffer[self.index]

    def DefList(self): #Done
        if self.current_token not in first["Def"] and not self.recovery:
            return self.error
        self.Def()
        
    def Def(self): #Done
        # Def -> def ID ( TypedVarList ) Return : Block
        if self.current_token != Lexemes.DEF and not self.recovery:
            return self.error
        self.next_token()
        if self.current_token != Tag.ID and not self.recovery:
            return self.error
        self.next_token()
        if self.current_token != Lexemes.LPAREN and not self.recovery: 
            return self.add_error("Expected '('. Error found at line ", self.Block)
        self.next_token()
        if self.current_token in first["TypedVarList"]:
            self.TypedVarList()
            self.next_token()
            while self.current_token == Lexemes.COMMA:
                self.next_token()
                self.TypedVar()
                self.next_token()
        if self.current_token != Lexemes.RPAREN and not self.recovery:
            return self.error
        self.next_token()
        if self.current_token == Lexemes.ARROW_ASSIGN:
            self.next_token()
            self.Type()
            self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            return self.error
        self.next_token()
        self.Block()
    
    def synchronize(self):
        if self.recovery:
            self.recovery = False

    def Block(self): #Done
        # Block -> NEWLINE INDENT Statement StatementList DEDENT
        if self.current_token != Tag.NEWLINE and not self.recovery:
            return self.error
        self.lineno+=1
        self.next_token()
        #if self.current_token != Tag.INDENT and not self.recovery:
        #    return self.error
        self.next_token()
        print("Current token", self.current_token)
        if self.current_token not in first["Statement"] and not self.recovery:
            return self.error
        self.Statement()
        self.next_token()
        while self.current_token in first["StatementList"]:
            self.StatementList()
            self.next_token()
        if self.current_token != Tag.DEDENT and self.current_token != self.eof and not self.recovery:
            return self.error

    def Statement(self): #Done
        if self.current_token == Lexemes.IF:
            self.next_token()
            self.Expr()
            if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
                return self.error
            self.next_token()
            self.Block()
            self.next_token()
            while self.current_token == Lexemes.ELIF:
                self.Elif()
                self.next_token()
            if self.current_token == Lexemes.ELSE:
                self.Else()
        elif self.current_token == Lexemes.WHILE:
            self.next_token()
            self.Expr()
            self.next_token()
            if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
                return self.error
            self.next_token()
            self.Block()
        elif self.current_token == Lexemes.FOR:
            self.next_token()
            if self.current_token != Tag.ID and not self.recovery:
                return self.error
            self.next_token()
            if self.current_token != Lexemes.IN and not self.recovery:
                return self.error
            self.next_token()
            self.Expr()
            self.next_token()
            if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
                return self.error
            self.Block()
        elif self.current_token in first["SimpleStatement"]:
            self.SimpleStatement()
            if self.current_token != Tag.NEWLINE and self.current_token != self.eof and not self.recovery:
                return self.error
            self.lineno+=1
            self.synchronize()
        else:
            return self.error

    def SimpleStatement(self): #Done
        if self.current_token in first["Expr"]:
            self.Expr()
            self.next_token()
            while self.current_token == Lexemes.EQUAL:
                self.SSTail()
                self.next_token()
        elif self.current_token == Lexemes.PASS:
            self.next_token()
        elif self.current_token == Lexemes.RETURN:
            self.next_token()
            self.ReturnExpr()
            self.next_token()
        else:
            return self.error
    
    def ReturnExpr(self):
        if self.current_token in first["Expr"]:
            self.Expr()

    def SSTail(self): #Done
        if self.current_token != Lexemes.EQUAL and not self.recovery:
            return self.error
        self.next_token()
        self.Expr()
    
    def StatementList(self): #Done
        if self.current_token not in first["Statement"] and not self.recovery:
            return self.error
        self.Statement()
    
    def Elif(self):
        if self.current_token != Lexemes.ELIF and not self.recovery:
            return self.error
        self.next_token()
        self.Expr()
        self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            return self.error
        self.next_token()
        self.Block()

    def Else(self):
        if self.current_token != Lexemes.ELSE and not self.recovery:
            return self.error
        self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            return self.error
        self.next_token()
        self.Block()

    def TypedVarList(self):
        if self.current_token not in first["TypedVar"] and not self.recovery:
            return self.error
        self.TypedVar()
    
    def TypedVar(self):
        if self.current_token != Tag.ID and not self.recovery:
            return self.error
        self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            return self.error
        self.next_token()
        self.Type()
    
    def Type(self):
        if self.current_token == Lexemes.INT:
            pass
        elif self.current_token == Lexemes.STR:
            pass
        elif  self.current_token == Lexemes.LSBRACKET:
            self.next_token()
            self.Type()
            self.next_token()
            if self.next_token != Lexemes.RSBRACKET and not self.recovery:
                return self.error
        else:
            return self.error
        
    def Expr(self):
        if self.current_token not in first["orExpr"] and not self.recovery:
            return self.error
        self.orExpr()
        while self.current_token in first["ExprPrime"]:
            self.ExprPrime()
            self.next_token()
    
    def ExprPrime(self): #Done
        if self.current_token != Lexemes.IF and not self.recovery:
            return self.error
        self.next_token()
        self.andExpr()
        self.next_token()
        if self.current_token != Lexemes.ELSE and not self.recovery:
            return self.error
        self.next_token()
        self.andExpr()
    
    def orExpr(self): #Done
        if self.current_token not in first["andExpr"] and not self.recovery:
            return self.error
        self.andExpr()
        while self.current_token in first["orExprPrime"]:
            self.orExprPrime()
            self.next_token()

    def orExprPrime(self): #Done
        if self.current_token != Lexemes.OR and not self.recovery:
            return self.error
        self.next_token()
        self.andExpr() 

    def andExpr(self): #Done
        if self.current_token not in first["notExpr"] and not self.recovery:
            return self.error
        self.notExpr()
        while self.current_token in first["andExprPrime"]:
            self.andExprPrime()
            self.next_token()
    
    def andExprPrime(self): #Done
        if self.current_token != Lexemes.AND and not self.recovery:
            return self.error
        self.next_token()
        self.notExpr() 

    def notExpr(self): #Done
        if self.current_token not in first["CompExpr"] and not self.recovery:
            return self.error
        self.CompExpr()
        while self.current_token in first["notExprPrime"]:
            self.notExprPrime()
            self.next_token()
    
    def notExprPrime(self): #Done
        if self.current_token != Lexemes.NOT and not self.recovery:
            return self.error
        self.next_token()
        self.CompExpr() 
    
    def CompExpr(self): #Done
        if self.current_token not in first["IntExpr"] and not self.recovery:
            return self.error
        self.IntExpr()
        while self.current_token in first["CompExprPrime"]:
            self.CompExprPrime()
            self.next_token()
    
    def CompExprPrime(self): #Done
        if self.current_token not in first["CompOp"] and not self.recovery:
            return self.error
        self.next_token()
        self.IntExpr()
    
    def IntExpr(self): #Done
        if self.current_token not in first["Term"] and not self.recovery:
            return self.error
        self.Term()
        while self.current_token in first["IntExprPrime"]:
            self.IntExprPrime()
            self.next_token()
    
    def IntExprPrime(self): #Done
        if self.current_token not in first["IntExprPrime"] and not self.recovery:
            return self.error
        self.next_token()
        self.Term()
    
    def Term(self): #Done
        if self.current_token not in first["Factor"] and not self.recovery:
            return self.error
        self.Factor()
        self.next_token()
        if self.current_token in first["NameTail"]:
            self.NameTail()
            self.next_token()
        while self.current_token in first["TermPrime"]:
            self.TermPrime()
            self.next_token()
    
    def TermPrime(self): #Done
        if self.current_token not in first["TermPrime"] and not self.recovery:
            return self.error
        self.next_token()
        self.Factor()

    def Factor(self):
        if self.current_token in first["Name"]:
            self.Name()
        elif self.current_token in first["Literal"]:
            self.Literal()
        elif self.current_token in first["List"]:
            self.List()
        elif self.current_token == Lexemes.LPAREN:
            self.next_token()
            self.Expr()
            self.next_token()
            if self.current_token != Lexemes.RPAREN and not self.recovery:
                return self.error
        else:
            return self.error
    
    def Name(self):
        if self.current_token != Tag.ID and not self.recovery:
            return self.error
    
    def Literal(self):
        if self.current_token not in [Lexemes.NONE, Lexemes.TRUE, Lexemes.FALSE, "INTEGER", "STRING"]  and not self.recovery:
            return self.error
    
    def List(self):
        if self.current_token != Lexemes.LSBRACKET and not self.recovery:
            return self.error
        self.next_token()
        self.ExprList()
        self.next_token()
        if self.current_token != Lexemes.RSBRACKET and not self.recovery:
            return self.error
    
    def NameTail(self):
        if self.current_token == Lexemes.LPAREN:
            self.next_token()
            self.ExprList()
            if self.current_token != Lexemes.RPAREN and not self.recovery:
                return self.error
        elif self.current_token in first["List"]:
            self.next_token()
            self.List()
        else:
            return self.error
        
    def ExprList(self):
        if self.current_token in first["Expr"]:
            self.next_token()
            self.Expr()
            self.next_token()
            while self.current_token in first["ExprListTail"]:
                self.ExprListTail()
                self.next_token()
    
    def ExprListTail(self):
        if self.current_token != Lexemes.COMMA and not self.recovery:
            return self.error
        self.next_token()
        self.Expr()