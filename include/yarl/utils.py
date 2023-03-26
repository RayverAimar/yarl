def print_error(error):
    print(f'  File "{error["filename"]}", line {error["lineno"]}')
    if error["content"][-1] == "\n":
        error["content"] = error["content"][:-1]
    print("\t", error["content"])
    point_out_error = " " * error["idx_error"] + prt_red("^" + "~" * (len(error["content"]) - error["idx_error"]))
    print("\t", point_out_error)
    print("LexicalError: ", end="")
    print(error["msg"])
    print()

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
    return BOLD + RED + text + RESET

def prt_green(text):
    return BOLD + GREEN + text + RESET

def prt_yellow(text):
    return BOLD + YELLOW + text + RESET

def prt_blue(text): 
    return BOLD + BLUE + text + RESET

def prt_violet(text): 
    return BOLD + VIOLET + text + RESET

def prt_beige(text): 
    return BOLD + BEIGE + text + RESET

def prt_white(text): 
    return BOLD + WHITE + text + RESET

def prt_cyan(text):
    return BOLD + CYAN + text + RESET