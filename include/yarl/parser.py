from yarl.definitions import Tag, Lexemes, first
from yarl.scanner import Scanner
from yarl.consolehandler import ConsoleHandler

from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter


def render_tree(root : object):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

with_expr = True

class RecursiveDescentParser:

    error_node = Node('Error')

    def __init__(self, eof, file_path):
        self.buffer = []
        self.scanner = Scanner()
        self.file_path = file_path
        tokens, errors = self.scanner.scan(file_path)
        self.tokens = tokens
        for token in tokens:
            if token.tag == 'INT':
                self.buffer.append(token.lexeme)
            elif token.tag == 'STR':
                self.buffer.append('str')
            elif token.tag == 'BOOL':
                self.buffer.append(token.lexeme)
            elif token.tag == 'ID':
                self.buffer.append(token.tag)
            elif token.tag == 'NUM':
                self.buffer.append('ID')
            elif token.tag in ['NEWLINE', 'DEDENT', 'INDENT']:
                self.buffer.append(token.tag)
            else:
                self.buffer.append(token.lexeme)

        self.eof = "$"
        self.error = ""
        self.index = 0
        self.current_token = self.buffer[self.index]
        self.errors = []
        self.lineno = 1
        self.recovery = False
    
    def parse(self):
        self.RootAST = Node('Program')
        self.program(self.RootAST)
        print(RenderTree(self.RootAST).by_attr())
        UniqueDotExporter(self.RootAST).to_picture("TreeImg.png")
        

    def add_error(self, message):
        self.errors.append(message)

    def program(self, parent:Node):
        while self.current_token in first["DefList"]:
            DefNonTerminalAST = Node("DEF_STATEMENT", parent=parent)
            self.Def(DefNonTerminalAST)
            
        while self.current_token in first["StatementList"]:
            self.StatementList(parent)

        console_handler = ConsoleHandler()
        if self.errors:
            print("\n--> Incorrect Program")
            console_handler.scan_debug_panel(self.errors, self.file_path, False)
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

    def HandlingError(self, func, parent):
        while self.current_token != Tag.NEWLINE:
            self.next_token()
        self.lineno+=1
        return func(parent)
        
    def Def(self, parent:Node):
        if self.current_token != Lexemes.DEF and not self.recovery:
            self.add_error(f'Expected \'{Lexemes.DEF}\' at line {self.tokens[self.index].line}.')
            return self.error
        self.def_node_AST = Node('def', parent=parent)
        self.next_token()
        if self.current_token != Tag.ID and not self.recovery:
            Node('ERROR', parent)
            self.add_error(f'Expected Identifier at line {self.tokens[self.index].line}')
            Block_Node = Node('BLOCK', parent=parent)
            return self.HandlingError(self.Block, Block_Node)
        Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
        if self.current_token != Lexemes.LPAREN and not self.recovery: 
            Node('ERROR', parent)
            self.add_error(f'Expected \'{Lexemes.LPAREN}\' at line {self.tokens[self.index].line}')
            Block_Node = Node('BLOCK', parent=parent)
            return self.HandlingError(self.Block, Block_Node)
        self.L_Paren_node_AST = Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
        if self.current_token in first["TypedVarList"]:
            TypedVar_Node_AST = Node('TYPED_VAR', parent=parent)
            self.TypedVarList(TypedVar_Node_AST)
            self.next_token()
            while self.current_token == Lexemes.COMMA:
                self.Comma_Node_AST = Node(str(self.tokens[self.index].lexeme), parent=parent)
                self.next_token()
                TypedVar_Node_AST = Node('TYPED_VAR', parent=parent)
                self.TypedVar(TypedVar_Node_AST)
                self.next_token()
        if self.current_token != Lexemes.RPAREN and not self.recovery:
            Node('ERROR', parent)
            self.add_error(f'Expected \'{Lexemes.RPAREN}\' at line {self.tokens[self.index].line}')
            Block_Node = Node('BLOCK', parent=parent)
            return self.HandlingError(self.Block, Block_Node)
        Node(Lexemes.RPAREN, parent=parent)
        self.next_token()
        if self.current_token == Lexemes.ARROW_ASSIGN:
            Node(Lexemes.ARROW_ASSIGN, parent=parent)
            self.next_token()
            self.Type(parent)
            self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            Node('ERROR', parent)
            self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
            Block_Node = Node('BLOCK', parent=parent)
            return self.HandlingError(self.Block, Block_Node)
        Node(Lexemes.COLON_ASSIGN, parent=parent)
        self.next_token()
        Block_Node = Node('BLOCK', parent=parent)
        self.Block(Block_Node)
        
    
    def synchronize(self, parent:Node=None):
        if self.recovery:
            self.recovery = False

    def Block(self, parent:Node=None):
        if self.current_token != Tag.NEWLINE and not self.recovery:
            print("There were an error")
            return self.error
                        #Node(Tag.NEWLINE, parent=parent)
        self.lineno+=1
        self.next_token()
        if self.current_token != Tag.INDENT and not self.recovery:
            print("There were an error")
            return self.error
                        #Node(Tag.INDENT, parent=parent)
        self.next_token()
        if self.current_token not in first["Statement"] and not self.recovery:
            print("There were an error")
            return self.error
        Statement_Node = Node('STATEMENT', parent=parent)
        self.Statement(Statement_Node)
        while self.current_token in first["StatementList"]:
            Statement_Node = Node('STATEMENT', parent=parent)
            self.StatementList(Statement_Node)
        if self.current_token != Tag.DEDENT and self.current_token != self.eof and not self.recovery:
            print("There were an error")
            return self.error
                        #Node(Tag.DEDENT, parent=parent)
        self.next_token()

    def Statement(self, parent:Node=None):
        if self.current_token == Lexemes.IF:
            Node(Lexemes.IF, parent)
            self.next_token()
            if with_expr:
                Expr_Node = Node('EXPR', parent=parent)
                self.Expr(Expr_Node)
            else:
                self.Expr(parent)
            if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
                Node('ERROR', parent)
                self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
                Block_Node = Node('BLOCK', parent=parent)
                return self.HandlingError(self.Block, Block_Node)
            Node(Lexemes.COLON_ASSIGN, parent)
            self.next_token()
            Block_Node = Node('BLOCK', parent)
            self.Block(Block_Node)
            while self.current_token == Lexemes.ELIF:
                self.Elif(parent)
            if self.current_token == Lexemes.ELSE:
                self.Else(parent)
        elif self.current_token == Lexemes.WHILE:
            Node(Lexemes.WHILE, parent=parent)
            self.next_token()
            if with_expr:
                Expr_Node = Node('EXPR', parent=parent)
                self.Expr(Expr_Node)
            else:
                self.Expr(parent)
            if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
                Node('ERROR', parent)
                self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
                Block_Node = Node('BLOCK', parent=parent)
                return self.HandlingError(self.Block, Block_Node)
            Node(Lexemes.COLON_ASSIGN, parent=parent)
            self.next_token()
            Block_Node = Node('BLOCK', parent=parent)
            self.Block(Block_Node)
        elif self.current_token == Lexemes.FOR:
            Node(Lexemes.FOR, parent)
            self.next_token()
            if self.current_token != Tag.ID and not self.recovery:
                print("There were an error")
                return self.error
            Node(str(self.tokens[self.index].lexeme), parent)
            self.next_token()
            if self.current_token != Lexemes.IN and not self.recovery:
                print("There were an error")
                return self.error
            Node(Lexemes.IN, parent)
            self.next_token()
            if with_expr:
                Expr_Node = Node('EXPR', parent=parent)
                self.Expr(Expr_Node)
            else:
                self.Expr(parent)
            if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
                Node('ERROR', parent)
                self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
                Block_Node = Node('BLOCK', parent=parent)
                return self.HandlingError(self.Block, Block_Node)
            Node(Lexemes.COLON_ASSIGN, parent)
            self.next_token()
            Block_Node = Node('BLOCK', parent)
            self.Block(Block_Node)
        elif self.current_token in first["SimpleStatement"]:
            self.SimpleStatement(parent)
            if self.current_token != Tag.NEWLINE and self.current_token != self.eof and not self.recovery:
                print("There were an error")
                return self.error
            self.next_token()
            self.lineno+=1
            self.synchronize()
        else:
            print("There were an error")
            return self.error

    def SimpleStatement(self, parent:Node=None):
        if self.current_token in first["Expr"]:
            if with_expr:
                Expr_Node = Node('EXPR', parent=parent)
                self.Expr(Expr_Node)
            else:
                self.Expr(parent)
            while self.current_token == Lexemes.EQUAL:
                Node(Lexemes.EQUAL, parent=parent)
                self.SSTail(parent)
        elif self.current_token == Lexemes.PASS:
            Node(Lexemes.PASS, parent)
            self.next_token()
        elif self.current_token == Lexemes.RETURN:
            Node(Lexemes.RETURN, parent)
            self.next_token()
            self.ReturnExpr(parent)
            self.next_token()
        else:
            print("There were an error")
            return self.error
    
    def ReturnExpr(self, parent:Node=None):
        if self.current_token not in [Lexemes.TRUE, Lexemes.FALSE, Lexemes.NONE, Tag.ID]:
            print('There was an error. Expected True/False or None')
        Node(str(self.tokens[self.index].lexeme), parent)

    def SSTail(self, parent:Node=None):
        if self.current_token != Lexemes.EQUAL and not self.recovery:
            print("There were an error")
            return self.error
        self.next_token()
        if with_expr:
            Expr_Node = Node('EXPR', parent=parent)
            self.Expr(Expr_Node)
        else:
            self.Expr(parent)
    
    def StatementList(self, parent:Node=None):
        if self.current_token not in first["Statement"] and not self.recovery:
            print("There were an error")
            return self.error
        Statement_Node = Node('STATEMENT', parent)
        self.Statement(Statement_Node)
    
    def Elif(self, parent:Node=None):
        if self.current_token != Lexemes.ELIF and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.ELIF, parent)
        self.next_token()
        if with_expr:
            Expr_Node = Node('EXPR', parent=parent)
            self.Expr(Expr_Node)
        else:
            self.Expr(parent)
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            Node('ERROR', parent)
            self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
            Block_Node = Node('BLOCK', parent=parent)
            return self.HandlingError(self.Block, Block_Node)
        Node(Lexemes.COLON_ASSIGN, parent)
        self.next_token()
        Block_Node = Node('BLOCK', parent)
        self.Block(Block_Node)

    def Else(self, parent:Node=None):
        if self.current_token != Lexemes.ELSE and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.ELSE, parent)
        self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            Node('ERROR', parent)
            self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
            Block_Node = Node('BLOCK', parent=parent)
            return self.HandlingError(self.Block, Block_Node)
        Node(Lexemes.COLON_ASSIGN, parent)
        self.next_token()
        Block_Node = Node('BLOCK', parent)
        self.Block(Block_Node)

    def TypedVarList(self, parent:Node):
        if self.current_token not in first["TypedVar"] and not self.recovery:
            print("There were an error")
            return self.error
        self.TypedVar(parent)
    
    def TypedVar(self, parent:Node):
        if self.current_token != Tag.ID and not self.recovery:
            print("There were an error")
            return self.error
        Node(str(self.tokens[self.index].lexeme), parent = parent)
        self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.COLON_ASSIGN, parent = parent)
        self.next_token()
        self.Type(parent)
    
    def Type(self, parent:Node):
        if self.current_token == Lexemes.INT:
            Node(Lexemes.INT, parent=parent)
        elif self.current_token == Lexemes.STR:
            Node(Lexemes.STR, parent=parent)
        elif self.current_token == Lexemes.BOOL:
            Node(Lexemes.BOOL, parent=parent)
        elif  self.current_token == Lexemes.LSBRACKET:
            Node(Lexemes.LSBRACKET, parent=parent)
            self.next_token()
            self.Type(parent)
            self.next_token()
            if self.current_token != Lexemes.RSBRACKET and not self.recovery:
                print("There were an error")
                return self.error
            Node(Lexemes.RSBRACKET, parent=parent)
        else:
            print("There were an error")
            return self.error
        
    def Expr(self, parent:Node=None):
        if self.current_token not in first["orExpr"] and not self.recovery:
            print("There were an error")
            return self.error
        self.orExpr(parent)
        while self.current_token in first["ExprPrime"]:
            self.ExprPrime(parent)
    
    def ExprPrime(self, parent:Node=None):
        if self.current_token != Lexemes.IF and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.IF, parent)
        self.next_token()
        self.andExpr(parent)
        if self.current_token != Lexemes.ELSE and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.ELSE, parent)
        self.next_token()
        self.andExpr(parent)
    
    def orExpr(self, parent:Node=None):
        if self.current_token not in first["andExpr"] and not self.recovery:
            print("There were an error")
            return self.error
        self.andExpr(parent)
        while self.current_token in first["orExprPrime"]:
            self.orExprPrime(parent)

    def orExprPrime(self, parent:Node=None):
        if self.current_token != Lexemes.OR and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.OR, parent)
        self.next_token()
        self.andExpr(parent) 

    def andExpr(self, parent:Node=None):
        if self.current_token not in first["notExpr"] and not self.recovery:
            print("There were an error")
            return self.error
        self.notExpr(parent)
        while self.current_token in first["andExprPrime"]:
            self.andExprPrime(parent)
    
    def andExprPrime(self, parent:Node=None):
        if self.current_token != Lexemes.AND and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.AND, parent)
        self.next_token()
        self.notExpr(parent) 

    def notExpr(self, parent:Node=None):
        if self.current_token not in first["CompExpr"] and not self.recovery:
            print("There were an error")
            return self.error
        self.CompExpr(parent)
        while self.current_token in first["notExprPrime"]:
            self.notExprPrime(parent)
    
    def notExprPrime(self, parent:Node=None):
        if self.current_token != Lexemes.NOT and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.NOT, parent)
        self.next_token()
        self.CompExpr(parent)
    
    def CompExpr(self, parent:Node=None):
        if self.current_token not in first["IntExpr"] and not self.recovery:
            print("There were an error")
            return self.error
        self.IntExpr(parent)
        while self.current_token in first["CompOp"]:
            self.CompExprPrime(parent)
    
    def CompExprPrime(self, parent:Node=None):
        if self.current_token not in first["CompOp"] and not self.recovery:
            print("There were an error")
            return self.error
        Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
        self.IntExpr(parent)
    
    def IntExpr(self, parent:Node=None):
        if self.current_token not in first["Term"] and not self.recovery:
            print("There were an error")
            return self.error
        self.Term(parent)
        while self.current_token in first["IntExprPrime"]:
            self.IntExprPrime(parent)
    
    def IntExprPrime(self, parent:Node=None):
        if self.current_token not in first["IntExprPrime"] and not self.recovery:
            print("There were an error")
            return self.error
        Node(str(self.tokens[self.index].lexeme), parent)
        self.next_token()
        self.Term(parent)
    
    def Term(self, parent:Node=None):
        if self.current_token not in first["Factor"] and not self.recovery:
            print("There were an error")
            return self.error
        self.Factor(parent)
        if self.current_token in first["NameTail"]:
            self.NameTail(parent)
        while self.current_token in first["TermPrime"]:
            self.TermPrime()
    
    def TermPrime(self, parent:Node=None):
        if self.current_token not in first["TermPrime"] and not self.recovery:
            print("There were an error")
            return self.error
        self.next_token()
        self.Factor()

    def Factor(self, parent:Node=None):
        if self.current_token in first["Name"]:
            self.Name(parent)
        elif self.current_token in first["Literal"]:
            self.Literal(parent)
        elif self.current_token in first["List"]:
            self.List(parent)
        elif self.current_token == Lexemes.LPAREN:
            Node(Lexemes.LPAREN, parent)
            self.next_token()
            if with_expr:
                Expr_Node = Node('EXPR', parent=parent)
                self.Expr(Expr_Node)
            else:
                self.Expr(parent)
            self.next_token()
            if self.current_token != Lexemes.RPAREN and not self.recovery:
                print("There were an error")
                return self.error
            Node(Lexemes.RPAREN, parent)
            self.next_token()
        else:
            print("There were an error")
            return self.error
    
    def Name(self, parent:Node=None):
        if self.current_token != Tag.ID and not self.recovery:
            print("There were an error")
            return self.error
        Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
    
    def Literal(self, parent:Node=None):
        if self.current_token not in [Lexemes.NONE, Lexemes.TRUE, Lexemes.FALSE, Tag.NUM, Lexemes.STR]  and not self.recovery:
            print("There were an error")
            return self.error
        Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
    
    def List(self, parent:Node=None):
        if self.current_token != Lexemes.LSBRACKET and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.LSBRACKET, parent=parent)
        self.next_token()
        self.ExprList(parent)
        if self.current_token != Lexemes.RSBRACKET and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.RSBRACKET, parent=parent)
        self.next_token()
    
    def NameTail(self, parent:Node=None):
        if self.current_token == Lexemes.LPAREN:
            Node(Lexemes.LPAREN, parent=parent)
            self.next_token()
            self.ExprList(parent)
            if self.current_token != Lexemes.RPAREN and not self.recovery:
                print("There were an error")
                return self.error
            Node(Lexemes.RPAREN, parent=parent)
            self.next_token()
        elif self.current_token in first["List"]:
            self.List(parent)
        else:
            print("There were an error")
            return self.error
        
    def ExprList(self, parent:Node=None):
        if self.current_token in first["Expr"]:
            if with_expr:
                Expr_Node = Node('EXPR', parent=parent)
                self.Expr(Expr_Node)
            else:
                self.Expr(parent)
            while self.current_token in first["ExprListTail"]:
                self.ExprListTail(parent)
    
    def ExprListTail(self, parent:Node=None):
        if self.current_token != Lexemes.COMMA and not self.recovery:
            print("There were an error")
            return self.error
        Node(Lexemes.COMMA, parent=parent)
        self.next_token()
        if with_expr:
            Expr_Node = Node('EXPR', parent=parent)
            self.Expr(Expr_Node)
        else:
            self.Expr(parent)