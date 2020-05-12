import sys
import os
from parser import Parser

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    try:
        file = open(filename, "r")
    except IOError:
        print(f"Cannot open {filename} file")
        sys.exit(0)
    try:
        import TreePrinter  # Add printTree to AST class dynamically
    except ImportError:
        print(f"TreePrinter not found in {os.path.dirname(os.path.realpath(__file__))}")
        sys.exit(0)
    parser = Parser()
    text = file.read()
    parser.parse(text, ast=False, type_check=False)
