def print_error(error):
    print(f'  File "{error["filename"]}", line {error["lineno"]}')
    if error["content"][-1] == "\n":
        error["content"] = error["content"][:-1]
    print("\t", error["content"])
    
    idx_error = error["idx_error"]
    highlight_number = 0 if "invalid" in error["msg"] else len(error["content"])-idx_error
    point_out_error = " " * idx_error + prt_red("^" + "~" * highlight_number)
    
    print("\t", point_out_error)
    print("  LexicalError: ", end="")
    print(error["msg"])
    print()

# Globals


# Prettier Output
BOLD   = '\33[1m'
RED    = '\33[31m'
GREEN  = '\33[32m'
YELLOW = '\33[33m'
BLUE   = '\33[34m'
VIOLET = '\33[35m'
BEIGE  = '\33[36m'
WHITE  = '\33[37m'
CYAN    = '\033[96m'
RESET = '\033[00m'

def prt_red(text):
    return BOLD + RED + str(text) + RESET

def prt_green(text):
    return BOLD + GREEN + str(text) + RESET

def prt_yellow(text):
    return BOLD + YELLOW + str(text) + RESET

def prt_blue(text): 
    return BOLD + BLUE + str(text) + RESET

def prt_violet(text): 
    return BOLD + VIOLET + str(text) + RESET

def prt_beige(text): 
    return BOLD + BEIGE + str(text) + RESET

def prt_white(text): 
    return BOLD + WHITE + str(text) + RESET

def prt_cyan(text):
    return BOLD + CYAN + str(text) + RESET