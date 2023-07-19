from yarl.definitions import Tag, Lexemes, first
from yarl.scanner import Scanner
from yarl.consolehandler import ConsoleHandler

from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter


def render_tree(root : object):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

class RecursiveDescentParser:

    error_node = Node('Error')

    def __init__(self, eof, file_path):
        self.buffer = []
        self.scanner = Scanner()
        self.file_path = file_path
        tokens, errors = self.scanner.scan(file_path)
        self.tokens = tokens
        self.scanner_errors = errors
        for i in range(len(tokens)):
            if self.tokens[i].tag == 'INT':
                self.buffer.append(self.tokens[i].lexeme)
            elif self.tokens[i].tag == 'STR':
                self.buffer.append('str')
            elif self.tokens[i].tag == 'BOOL':
                self.buffer.append(self.tokens[i].lexeme)
            elif self.tokens[i].tag == 'ID':
                self.buffer.append(self.tokens[i].tag)
            elif self.tokens[i].tag == 'NUM':
                self.buffer.append('ID')
            elif self.tokens[i].tag in ['NEWLINE', 'DEDENT', 'INDENT']:
                if self.tokens[i- 1]. tag == 'NEWLINE' and self.tokens[i]. tag == "NEWLINE":
                    continue
                self.buffer.append(self.tokens[i].tag)
            else:
                self.buffer.append(self.tokens[i].lexeme)

        self.eof = eof
        self.error = ""
        self.index = 0
        self.current_token = self.buffer[self.index]
        self.errors = []
    def parse(self):
        print(self.buffer)
        self.RootAST = Node('Program')
        self.program(self.RootAST)
        print()
        
        UniqueDotExporter(self.RootAST).to_picture("./output/Abstract_Syntax_Tree.png")
        console_handler = ConsoleHandler()
        console_handler.print_title()

        if self.scanner_errors:
            console_handler.scan_debug_panel(self.scanner_errors, self.file_path)
            console_handler.console.print(f'\nFinishing scanning with [b red]{len(self.scanner_errors)}[/b red] errors\n', justify="center")
            console_handler.console.print(f'\nForcing parse. There were [b red]{len(self.scanner_errors)}[/b red] errors during scanning.\n', justify="center")
            #return
        else:
            console_handler.scan_debug_table(self.tokens)
            console_handler.console.print(f'\nFinishing scanning with [b red]{len(self.scanner_errors)}[/b red] errors\n', justify="center")

        print(RenderTree(self.RootAST).by_attr())

        if self.errors:
            console_handler.scan_debug_panel(self.errors, self.file_path, False)
            print("\n--> Incorrect Program")
        else:
            print("\n--> Accepted Program")

    def add_error(self, message):
        self.errors.append(message)
    
    def program(self, parent:Node):
        while self.current_token == Lexemes.DEF:
            Def_Statement_Node = Node("DEF_STATEMENT", parent=parent)
            Node('def', parent=Def_Statement_Node)
            self.next_token()
            if not self.Def(Def_Statement_Node):
                if not self.panic_mode(None, 'DEDENT', parent):
                    return False
                
        while self.current_token in first["Statement"]:
            if not self.Statement(parent):
                self.panic_mode(None, 'STATEMENT', parent)
                self.next_token()
        return True

    def panic_mode(self, msg, func_to_syncronize, parent:Node):
        Node('ERROR', parent)
        if msg:
            self.add_error(msg)
        if func_to_syncronize == 'BLOCK':
            Block_Node = Node(func_to_syncronize, parent)
            return self.HandlingError(self.Block, Block_Node)
        elif func_to_syncronize == 'STATEMENT':
            while self.current_token != Tag.NEWLINE:
                if not self.next_token():
                    return False
            return True
        elif func_to_syncronize ==  'DEDENT':
            while self.current_token != Tag.DEDENT:
                if not self.next_token():
                    return False
            if not self.next_token():
                return False
            return True

    def next_token(self):
        
        if self.index < len(self.buffer) - 1:
            self.index+=1
            self.current_token = self.buffer[self.index]
            return True
        else:
            self.current_token = self.eof
            return False

    def HandlingError(self, func, parent):
        while self.current_token != Tag.NEWLINE:
            self.next_token()
        return func(parent)
        
    def Def(self, parent:Node):
        if self.current_token != Tag.ID:
            msg = f'Expected Identifier at line {self.tokens[self.index].line}'
            return self.panic_mode(msg, 'BLOCK', parent)
        Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
        
        if self.current_token != Lexemes.LPAREN:
            msg = f'Expected \'{Lexemes.LPAREN}\' at line {self.tokens[self.index].line}'
            return self.panic_mode(msg, 'BLOCK', parent)
        Node(Lexemes.LPAREN, parent=parent)
        self.next_token()
        
        if self.current_token == Tag.ID:
            TypedVar_Node_AST = Node('TYPED_VAR', parent)
            if not self.TypedVar(TypedVar_Node_AST):
                return self.panic_mode(None, 'BLOCK', parent)
            self.next_token()
            while self.current_token == Lexemes.COMMA:
                self.Comma_Node_AST = Node(str(self.tokens[self.index].lexeme), parent=parent)
                self.next_token()
                TypedVar_Node_AST = Node('TYPED_VAR', parent=parent)
                if not self.TypedVar(TypedVar_Node_AST):
                    return self.panic_mode(None, 'BLOCK', parent)
                self.next_token()
        
        if self.current_token != Lexemes.RPAREN:
            msg = f'Expected \'{Lexemes.RPAREN}\' at line {self.tokens[self.index].line}'
            return self.panic_mode(msg, 'BLOCK', parent)
        Node(Lexemes.RPAREN, parent=parent)
        self.next_token()

        if self.current_token == Lexemes.ARROW_ASSIGN:
            Node(Lexemes.ARROW_ASSIGN, parent=parent)
            self.next_token()
            if not self.Type(parent):
                msg = f'Expected \'{Lexemes.RPAREN}\' at line {self.tokens[self.index].line}'
                return self.panic_mode(msg, 'BLOCK', parent)
            self.next_token()

        if self.current_token != Lexemes.COLON_ASSIGN:
            Node('ERROR', parent)
            self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
            Block_Node = Node('BLOCK', parent=parent)
            return self.HandlingError(self.Block, Block_Node)
        Node(Lexemes.COLON_ASSIGN, parent=parent)
        self.next_token()
        Block_Node = Node('BLOCK', parent=parent)

        if not self.Block(Block_Node):
            return self.panic_mode(None, 'DEDENT', parent)
        return True

    def Block(self, parent:Node=None):
        if self.current_token != Tag.NEWLINE:
            self.add_error(f'Expected Line Break at line {self.tokens[self.index].line}.')
            self.panic_mode(None, 'STATEMENT', parent)
        self.next_token()

        if self.current_token != Tag.INDENT:
            self.add_error(f'Expected indentation at line {self.tokens[self.index].line}.')
            return self.panic_mode(None, 'STATEMENT', parent)
            #return False # Should enter in panic mode until find a DEDENT
        self.next_token()

        if not self.Statement(parent): 
            self.panic_mode(None, 'STATEMENT', parent)
            self.next_token()
        
        while self.current_token in first["Statement"]:
            if not self.Statement(parent):
                self.panic_mode(None, 'STATEMENT', parent)
                self.next_token()

        if self.current_token != Tag.DEDENT and self.current_token != self.eof:
            self.add_error(f'Expected dedent at line {self.tokens[self.index].line}.')
            return False
        self.next_token()
        return True

    def Statement(self, parent:Node=None):
        statement_Node = Node('STATEMENT', parent)
        parent = statement_Node
        if self.current_token == Lexemes.IF:
            Node(Lexemes.IF, parent)
            self.next_token()
            Expr_Node = Node('EXPR', parent=parent)
            if not self.Expr(Expr_Node):
                return self.panic_mode(None, 'BLOCK', parent)
            if self.current_token != Lexemes.COLON_ASSIGN:
                msg = f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}'
                return self.panic_mode(msg, 'BLOCK', parent)
            Node(Lexemes.COLON_ASSIGN, parent)
            self.next_token()
            Block_Node = Node('BLOCK', parent)
            if not self.Block(Block_Node):
                self.panic_mode(None, 'DEDENT', parent)
            while self.current_token == Lexemes.ELIF:
                if not self.Elif(parent):
                    self.panic_mode(None, 'DEDENT', parent)
            if self.current_token == Lexemes.ELSE:
                if not self.Else(parent):
                    self.panic_mode(None, 'DEDENT', parent)
            return True

        elif self.current_token == Lexemes.WHILE:
            Node(Lexemes.WHILE, parent=parent)
            self.next_token()
            Expr_Node = Node('EXPR', parent=parent)
            if not self.Expr(Expr_Node):
                return self.panic_mode(None, 'BLOCK', parent)
            if self.current_token != Lexemes.COLON_ASSIGN:
                msg = f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}'
                return self.panic_mode(msg, 'BLOCK', parent)
            Node(Lexemes.COLON_ASSIGN, parent=parent)
            self.next_token()
            Block_Node = Node('BLOCK', parent=parent)
            if not self.Block(Block_Node):
                return self.panic_mode(None, 'DEDENT', parent)
            return True

        elif self.current_token == Lexemes.FOR:
            Node(Lexemes.FOR, parent)
            self.next_token()
            if self.current_token != Tag.ID:
                msg = f'Expected Identifier at line {self.tokens[self.index].line}'
                return self.panic_mode(msg, 'BLOCK', parent)
            Node(str(self.tokens[self.index].lexeme), parent)
            self.next_token()
            if self.current_token != Lexemes.IN:
                msg = f'Expected Lexeme \'{Lexemes.IN}\' at line {self.tokens[self.index].line}'
                return self.panic_mode(msg, 'BLOCK', parent)
            Node(Lexemes.IN, parent)
            self.next_token()
            Expr_Node = Node('EXPR', parent=parent)
            if not self.Expr(Expr_Node):
                return self.panic_mode(msg, 'BLOCK', parent)
            if self.current_token != Lexemes.COLON_ASSIGN:
                msg = f'Expected Lexeme \'{Lexemes.IN}\' at line {self.tokens[self.index].line}'
                return self.panic_mode(msg, 'BLOCK', parent)
            Node(Lexemes.COLON_ASSIGN, parent)
            self.next_token()
            Block_Node = Node('BLOCK', parent)
            if not self.Block(Block_Node):
                return self.panic_mode(None, 'DEDENT', parent)
            return True

        elif self.current_token in first["SimpleStatement"]:
            if not self.SimpleStatement(parent):
                self.panic_mode(None, 'STATEMENT', parent)
            if self.current_token != Tag.NEWLINE and self.current_token != self.eof:
                self.add_error(f'Expected Line Break at line {self.tokens[self.index].line}.')
                return False
            self.next_token()
            return True
        else:
            return False

    def SimpleStatement(self, parent:Node=None):
        if self.current_token in first["Expr"]:
            Expr_Node = Node('EXPR', parent=parent)
            if not self.Expr(Expr_Node):
                return False
            while self.current_token == Lexemes.EQUAL:
                Node(Lexemes.EQUAL, parent=parent)
                if not self.SSTail(parent):
                    return False
            return True
        
        elif self.current_token == Lexemes.PASS:
            Node(Lexemes.PASS, parent)
            self.next_token()
            return True
        
        elif self.current_token == Lexemes.RETURN:
            Node(Lexemes.RETURN, parent)
            self.next_token()
            if self.current_token in first['Expr']:
                Expr_Node = Node('EXPR', parent=parent)
                if not self.Expr(Expr_Node):
                    return False
                #self.next_token()
            return True
        
        else:
            return False
    
    def SSTail(self, parent:Node=None):
        self.next_token()
        Expr_Node = Node('EXPR', parent=parent)
        if not self.Expr(Expr_Node):
            return False
        return True
    
    def Elif(self, parent:Node=None):
        Node(Lexemes.ELIF, parent)
        self.next_token()
        Expr_Node = Node('EXPR', parent=parent)
        if not self.Expr(Expr_Node):
            return self.panic_mode(None, 'BLOCK', parent)
        if self.current_token != Lexemes.COLON_ASSIGN:
            msg = f'Expected Lexeme \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}'
            return self.panic_mode(msg, 'BLOCK', parent)
        Node(Lexemes.COLON_ASSIGN, parent)
        self.next_token()
        Block_Node = Node('BLOCK', parent)
        if not self.Block(Block_Node):
            return False
        return True

    def Else(self, parent:Node=None):
        Node(Lexemes.ELSE, parent)
        self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN:
            msg = f'Expected Lexeme \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}'
            return self.panic_mode(msg, 'BLOCK', parent)
        Node(Lexemes.COLON_ASSIGN, parent)
        self.next_token()
        Block_Node = Node('BLOCK', parent)
        if not self.Block(Block_Node):
            return False
        return True

    def TypedVar(self, parent:Node):
        Node(str(self.tokens[self.index].lexeme), parent)
        self.next_token()
        if self.current_token != Lexemes.COLON_ASSIGN:
            self.add_error(f'Expected \'{Lexemes.COLON_ASSIGN}\' at line {self.tokens[self.index].line}')
            return False
        Node(Lexemes.COLON_ASSIGN, parent)
        self.next_token()
        return self.Type(parent)
    
    def Type(self, parent:Node):
        if self.current_token == Lexemes.INT:
            Node(Lexemes.INT, parent)
            return True
        elif self.current_token == Lexemes.STR:
            Node(Lexemes.STR, parent)
            return True
        elif self.current_token == Lexemes.BOOL:
            Node(Lexemes.BOOL, parent)
            return True
        elif  self.current_token == Lexemes.LSBRACKET:
            Node(Lexemes.LSBRACKET, parent)
            self.next_token()
            self.Type(parent)
            self.next_token()
            if self.current_token != Lexemes.RSBRACKET:
                self.add_error(f'Expected \'{Lexemes.RPAREN}\' at line {self.tokens[self.index].line}.')
                return False
            Node(Lexemes.RSBRACKET, parent)
            return True
        else:
            self.add_error(f'\'{self.current_token}\' at line {self.tokens[self.index].line} is not a handeable Type.')
            return False
        
    def Expr(self, parent:Node=None):
        if self.current_token not in first["orExpr"]:
            return False
        if not self.orExpr(parent):
            return False
        while self.current_token in Lexemes.IF:
            if not self.ExprPrime(parent):
                return False
        return True
    
    def ExprPrime(self, parent:Node=None):
        Node(Lexemes.IF, parent)
        self.next_token()
        if not self.andExpr(parent):
            return False
        if self.current_token != Lexemes.ELSE:
            self.add_error(f'Expected {Lexemes.ELSE} at line {self.tokens[self.index].line}')
            return False
        Node(Lexemes.ELSE, parent)
        self.next_token()
        if not self.andExpr(parent):
            return False
        return True
    
    def orExpr(self, parent:Node=None):
        if self.current_token not in first["andExpr"]:
            return False
        if not self.andExpr(parent):
            return False
        while self.current_token in first["orExprPrime"]:
            if not self.orExprPrime(parent):
                return False
        return True

    def orExprPrime(self, parent:Node=None):
        if self.current_token != Lexemes.OR:
            return False
        Node(Lexemes.OR, parent)
        self.next_token()
        if not self.andExpr(parent):
            return False
        return True

    def andExpr(self, parent:Node=None):
        if self.current_token not in first["notExpr"]:
            return False
        if not self.notExpr(parent):
            return False
        while self.current_token in Lexemes.AND:
            Node(Lexemes.AND, parent)
            self.next_token()
            if not self.notExpr(parent):
                return False
        return True

    def notExpr(self, parent:Node=None):
        if self.current_token not in first["CompExpr"]:
            self.add_error(f'Not expected lexeme at line {self.tokens[self.index].line}.')
            return False
        if not self.CompExpr(parent):
            return False
        while self.current_token in Lexemes.NOT:
            Node(Lexemes.NOT, parent)
            self.next_token()
            if not self.CompExpr(parent):
                return False
        return True
    
    def CompExpr(self, parent:Node=None):
        if self.current_token not in first["IntExpr"]:
            self.add_error(f'Not expected lexeme at line {self.tokens[self.index].line}.')
            return False
        if not self.IntExpr(parent):
            return False
        while self.current_token in first["CompOp"]:
            Node(str(self.tokens[self.index].lexeme), parent=parent)
            self.next_token()
            if not self.IntExpr(parent):
                return False
        return True
    
    def IntExpr(self, parent:Node=None):
        if self.current_token not in first["Term"]:
            self.add_error(f'Not expected lexeme at line {self.tokens[self.index].line}.')
            return False
        if not self.Term(parent):
            return False
        while self.current_token in first["IntExprPrime"]:
            Node(str(self.tokens[self.index].lexeme), parent)
            self.next_token()
            if not self.Term(parent):
                return False
        return True
    
    def Term(self, parent:Node=None):
        if self.current_token not in first["Factor"]:
            return False
        if not self.Factor(parent):
            return False
        if self.current_token in first["NameTail"]:
            if not self.NameTail(parent):
                return False
        while self.current_token in first["TermPrime"]:
            Node(str(self.tokens[self.index].lexeme), parent)
            self.next_token()
            if not self.Factor(parent):
                return False
        return True

    def Factor(self, parent:Node=None):
        if self.current_token == Tag.ID:
            return self.Name(parent)
        elif self.current_token in first["Literal"]:
            return self.Literal(parent)
        elif self.current_token == Lexemes.LSBRACKET:
            return self.List(parent)
        elif self.current_token == Lexemes.LPAREN:
            Node(Lexemes.LPAREN, parent)
            self.next_token()
            Expr_Node = Node('EXPR', parent=parent)
            if not self.Expr(Expr_Node):
                return False
            self.next_token()
            if self.current_token != Lexemes.RPAREN:
                self.add_error(f'Expected \'{Lexemes.RPAREN}\' at line {self.tokens[self.index].line}')
                return False
            Node(Lexemes.RPAREN, parent)
            self.next_token()
            return True
        else:
            self.add_error(f'Not a handleable Factor. Expected Identifier, Literal or List at line {self.tokens[self.index].line}')
            return False
    
    def Name(self, parent:Node=None):
        Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
        return True
    
    def Literal(self, parent:Node=None):
        Node(str(self.tokens[self.index].lexeme), parent=parent)
        self.next_token()
        return True
    
    def List(self, parent:Node=None):
        Node(Lexemes.LSBRACKET, parent=parent)
        self.next_token()
        if not self.ExprList(parent):
            return False
        if self.current_token != Lexemes.RSBRACKET:
            self.add_error(f'Expected \'{Lexemes.RSBRACKET}\' at line {self.tokens[self.index].line}')
            return False
        Node(Lexemes.RSBRACKET, parent=parent)
        self.next_token()
        return True
    
    def NameTail(self, parent:Node=None):
        if self.current_token == Lexemes.LPAREN:
            Node(Lexemes.LPAREN, parent=parent)
            self.next_token()
            if not self.ExprList(parent):
                return False
            if self.current_token != Lexemes.RPAREN:
                self.add_error(f'Expected \'{Lexemes.RPAREN}\' at line {self.tokens[self.index].line}')
                return False
            Node(Lexemes.RPAREN, parent=parent)
            self.next_token()
            return True
        elif self.current_token == Lexemes.LSBRACKET:
            return self.List(parent)
        else:
            self.add_error(f'Not expected lexeme at line {self.tokens[self.index].line}.')
            return False
        
    def ExprList(self, parent:Node=None):
        if self.current_token in first["Expr"]:
            Expr_Node = Node('EXPR', parent=parent)
            if not self.Expr(Expr_Node):
                return False
            while self.current_token == Lexemes.COMMA:
                if not self.ExprListTail(parent):
                    return False
        return True
    
    def ExprListTail(self, parent:Node=None):
        Node(Lexemes.COMMA, parent=parent)
        self.next_token()
        Expr_Node = Node('EXPR', parent=parent)
        if not self.Expr(Expr_Node):
            return False
        return True