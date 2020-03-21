import os

import ply.yacc as yacc

from lexer import Lexer


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Parser(object):
    tokens = Lexer.tokens

    precedence = (  # TODO Fill
        ("nonassoc", 'IF', 'WHILE'),
        ("left", 'LCURLY', 'RCURLY'),
    )

    def __init__(self, start="statements", outputdir="logs", tabmodule="baseparsetab"):
        create_dir(outputdir)
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, start=start, tabmodule=tabmodule, outputdir=outputdir)

    def parse(self, text):
        self.parser.parse(text)

    def p_error(self, p):  # Syntax error handler
        # if p:
        #     print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
        #                                                                               scanner.find_tok_column(p),
        #                                                                               p.type, p.value))
        # else:
        print("Unexpected end of input", p)

    def p_empty(self, p):  # Empty production
        """empty :"""
        pass

    def p_statements(self, p):
        """statements : empty
                      | LCURLY statements RCURLY
                      | statement statements
        """
        print(p)

    def p_statement(self, p):
        """statement : IF expression block
                     | WHILE expression block
                     | FOR for_expression block
                     | PRINT print_expression SEMICOL
                     | expressions SEMICOL
        """
        print(p)

    def p_block(self, p):
        """block : statement
                 | LCURLY statements RCURLY
        """
        print(p)

    def p_expressions(self, p):
        """expressions : assign_expression
                       | control_expression
        """
        print(p)

    def p_for_expression(self, p):  # TODO INTNUM can be ID
        """ for_expression : ID ASSIGN INTNUM RANGE INTNUM"""
        print(p)

    def p_print_expression(self, p):
        """ print_expression : STRING
                             | term
                             | COMMA print_expression
        """
        print(p)

    def p_assign_expression(self, p):
        """assign_expression : ID assign_op expression
        """
        print(p)

    def p_control_expression(self, p):
        """control_expression : BREAK
                              | CONTINUE
                              | RETURN
        """
        print(p)

    def p_expression(self, p):
        """expression : expression op expression
                      | LPAREN expression RPAREN
                      | term
        """
        print(p)

    def p_assign_op(self, p):
        """assign_op : ASSIGN
                     | ADDASSIGN
                     | SUBASSIGN
                     | MULASSIGN
                     | DIVASSIGN
        """
        print(p)

    def p_op(self, p):
        """op : bin_op
              | rel_op
        """
        print(p)

    def p_bin_op(self, p):
        """bin_op : ADD
                  | SUB
                  | DIV
                  | MUL
        """
        print(p)

    def p_rel_op(self, p):
        """rel_op : GE
                  | GEQ
                  | LE
                  | LEQ
                  | EQ
                  | NEQ
        """
        print(p)

    def p_term(self, p):
        """term : ID
                | INTNUM
                | FLOATNUM
        """
        print(p)
