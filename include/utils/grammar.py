epsilon = "epsilon"

grammar = """

program         : def_list stmt_list
def_list        : defs def_list | epsilon
defs            : var_def | func_def | class_def
stmt_list       : stmt stmt_list | epsilon
func_def        : def IDENTIFIER (typed_var_list) : NEWLINE INDENT func_body DEDENT
typed_var_list  : typed_var typed_var_list | epsilon  
func_body       : stmt stmt_list


"""