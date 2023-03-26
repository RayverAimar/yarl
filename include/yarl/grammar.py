epsilon = "epsilon"

grammar = """
program             : def_list stmt_list
def_list            : defs def_list | epsilon
defs                : insider_defs | class_def
insider_defs        : var_def | func_def
var_def             : typed_var = literal NEWLINE
literal             : None | True | False | INTEGER | IDSTRING | STRING
func_def            : def ID ( typed_var_list ) return_type : NEWLINE INDENT func_body DEDENT
return_type         : -> type | epsilon
typed_var_list      : typed_var typed_var_list_cont | epsilon
typed_var           : ID : type
type                : ID | IDSTRING | [ type ]
typed_var_list_cont : , typed_var typed_var_list_cont | epsilon
func_body           : pre_body_stmts stmt stmt_list
pre_body_stmts      : pre_body_stmt pre_body_stmts | epsilon
pre_body_stmt       : decls | insider_defs
decls               : global_decl | nonlocal_decl
global_decl         : global ID NEWLINE
nonlocal_decl       : nonlocal ID NEWLINE
class_def           : class ID ( ID ) : NEWLINE INDENT class_body DEDENT
class_body          : pass NEWLINE | insider_defs insider_defs_list
insider_defs_list   : insider_defs insider_defs_list | epsilon
stmt_list           : stmt stmt_list | epsilon
stmt                : simple_stmt NEWLINE | if_stmt | while_stmt | for_stmt
simple_stmt         : pass | expr | return expr_eps | target_list expr
expr                : cexpr | not expr | expr and_or expr | expr if expr else expr
cexpr               : ID | literal | [ expr_list ] | ( expr ) | member_expr | index_expr | member_expr ( expr_list ) | ID ( expr_list ) | cexpr bin_op cexpr
expr_list           : expr expr_list_cont | epsilon
expr_list_cont      : , expr expr_list_cont | epsilon
member_expr         : member_expr . ID
index_expr          : cexpr [ expr ]
bin_op              : + | - | + | * | // | % | == | != | <= | >= | < | > | is 
and_or              : and | or
expr_eps            : expr | epsilon
target_list         : target = target_list_cont expr
target_list_cont    : target = | epsilon
target              : ID | member_expr | index_expr
if_stmt             : if expr : block elif_stmt_list else_stmt_eps
block               : NEWLINE INDENT stmt stmt_list DEDENT
elif_stmt_list      : elif_stmt elif_stmt_list | epsilon
elif_stmt           : elif expr : block
else_stmt_eps       : else : block | epsilon
while_stmt          : while expr : block
for_stmt            : for ID in expr : block
"""