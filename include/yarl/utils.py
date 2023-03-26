def print_error(error):
    print(f'  File "{error["filename"]}", line {error["lineno"]}')
    if error["content"][-1] == "\n":
        error["content"] = error["content"][:-1]
    print("\t", error["content"])
    point_out_error = " " * error["idx_error"] + "^"
    print("\t", point_out_error)
    print("LexicalError: ", end="")
    print(error["msg"])
    print()