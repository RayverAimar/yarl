from include.scanner.scanner import Scanner

scanner = Scanner()
tokens = scanner.scan("./samples/sample.txt")
line = 1
for token in tokens:
    if token.line != line:
        line = token.line
        print()
    print(token, end=" ")

