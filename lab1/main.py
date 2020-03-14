# object oriented version

import sys

from scanner import Scanner  # Scanner needs to be provided manually

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print(f"Cannot open {filename} file")
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    lexer.build()

    # Give the lexer some input
    lexer.input(text)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        line_number, token_type, token_value = tok.lineno, tok.type, tok.value
        print(f"({line_number}): {token_type}({token_value})")
