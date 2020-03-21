import sys

from parser import Parser

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    try:
        file = open(filename, "r")
    except IOError:
        print(f"Cannot open {filename} file")
        sys.exit(0)

    parser = Parser()
    text = file.read()
    parser.parse(text)
