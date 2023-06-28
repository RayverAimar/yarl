epsilon = "ε"

grammar = """
Program -> DefList StatementList
DefList -> Def DefList 
DefList -> ε
Def -> def ID ( TypedVarList ) Return : Block
TypedVar -> ID : Type
Type -> int
Type -> str
Type -> [ Type ]
TypedVarList -> ε
TypedVarList -> TypedVar TypedVarListTail
TypedVarListTail -> , TypedVar TypedVarListTail
TypedVarListTail -> ε
Return -> ε
Return -> -> Type
Block -> NEWLINE INDENT Statement StatementList DEDENT
StatementList -> Statement StatementList
StatementList -> ε
Statement -> SimpleStatement NEWLINE
Statement -> if Expr : Block ElifList Else
Statement -> while Expr : Block
Statement -> for ID in Expr : Block
ElifList -> Elif ElifList
ElifList -> ε
Elif -> elif Expr : Block
Else -> ε
Else -> else : Block
SimpleStatement -> Expr SSTail
SSTail -> ε
SSTail -> = Expr
SimpleStatement -> pass
SimpleStatement -> return ReturnExpr
ReturnExpr -> Expr
ReturnExpr -> ε
Expr -> orExpr ExprPrime
ExprPrime -> if andExpr else andExpr ExprPrime
ExprPrime -> ε
orExpr -> andExpr orExprPrime
orExprPrime -> or andExpr orExprPrime
orExprPrime -> ε
andExpr -> notExpr andExprPrime
andExprPrime -> and notExpr andExprPrime
andExprPrime -> ε
notExpr -> CompExpr notExprPrime
notExprPrime -> not CompExpr notExprPrime
notExprPrime -> ε
CompExpr -> IntExpr CompExprPrime
CompExprPrime -> CompOp IntExpr CompExprPrime
CompExprPrime -> ε
IntExpr -> Term IntExprPrime
IntExprPrime -> + Term IntExprPrime
IntExprPrime -> - Term IntExprPrime
IntExprPrime -> ε
Term -> Factor TermPrime
TermPrime -> * Factor TermPrime
TermPrime -> // Factor TermPrime
TermPrime -> % Factor TermPrime
TermPrime -> ε
Factor -> Name
Factor -> Literal
Factor -> List
Factor -> ( Expr )
Name -> ID NameTail
NameTail -> ε
NameTail -> ( ExprList )
NameTail -> List
Literal -> None
Literal -> True
Literal -> False
Literal -> INTEGER
Literal -> STRING
List -> [ ExprList ]
ExprList -> ε
ExprList -> Expr ExprListTail
ExprListTail -> ε
ExprListTail -> , Expr ExprListTail
CompOp -> == 
CompOp -> != 
CompOp -> < 
CompOp -> > 
CompOp -> <= 
CompOp -> >= 
CompOp -> is

"""