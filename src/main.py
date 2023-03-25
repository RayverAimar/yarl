from include.scanner.scanner import Scanner

scanner = Scanner()
tokens = scanner.scan("./samples/sample.txt")
for token in tokens:
    print(token.lexeme, " ", token.tag)
