import argparse
import os
import sys

from parser import Parser


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--filename',
        help='File to perform parsing',
        type=str,
        required=True
    )
    parser.add_argument(
        '--disable_ast',
        help='Disable performing ast printing',
        action='store_true',
        default=False)
    parser.add_argument(
        '--disable_type_check',
        help='Disable performing type checking',
        action='store_true',
        default=False)
    parser.add_argument(
        '--disable_interpretation',
        help='Disable performing interpretation',
        action='store_true',
        default=False)
    return parser


if __name__ == '__main__':
    FLAGS = create_parser().parse_args()
    try:
        file = open(FLAGS.filename, "r")
    except IOError:
        print(f"Cannot open {FLAGS.filename} file")
        sys.exit(0)
    try:
        import TreePrinter  # Add printTree to AST class dynamically
    except ImportError:
        print(f"TreePrinter not found in {os.path.dirname(os.path.realpath(__file__))}")
        sys.exit(0)
    parser = Parser()
    text = file.read()
    parser.parse(text,
                 ast=not FLAGS.disable_ast,
                 type_check=not FLAGS.disable_type_check,
                 interpretation=not FLAGS.disable_interpretation
                 )
