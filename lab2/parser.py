import os

import ply.yacc as yacc

from lexer import Lexer


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Parser(object):
    tokens = Lexer.tokens + ('UMINUS',)

    precedence = (  # TODO Fill
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'GE', 'GEQ', 'LE', 'LEQ', 'EQ', 'NEQ'),
        ('left', 'ADD', 'SUB', 'COMMA'),
        ('left', 'MUL', 'DIV'),
        ('right', 'UMINUS'),
        ('left', 'LPAREN', 'RPAREN'),
        ('left', 'LCURLY', 'RCURLY'),
    )

    def __init__(self, start="statements", outputdir="logs", tabmodule="baseparsetab"):
        create_dir(outputdir)
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, start=start, tabmodule=tabmodule, outputdir=outputdir)

    def parse(self, text):
        self.text = text
        self.parser.parse(text)

    def p_error(self, p):  # Syntax error handler
        if p:
            print(f"Syntax error at line {p.lineno}, column {self.lexer.find_tok_column(self.text, p)}:"
                  f"LexToken({p.type}, {p.value})")
        else:
            print("Unexpected end of input")

    def p_empty(self, p):  # Empty production
        """empty :"""
        pass

    def p_statements(self, p):
        """statements : empty
                      | LCURLY statements RCURLY
                      | statement statements
        """

    def p_statement(self, p):
        """statement : IF expression block %prec IFX
                     | IF expression block ELSE block
                     | WHILE expression block
                     | FOR for_expression block
                     | PRINT print_expression SEMICOL
                     | expressions SEMICOL
        """

    def p_block(self, p):
        """block : statement
                 | LCURLY statements RCURLY
        """

    def p_expressions(self, p):
        """expressions : assign_expression
                       | control_expression
        """

    def p_expr_uminus(self, p):
        """expression : SUB expression %prec UMINUS"""

    def p_for_expression(self, p):
        """ for_expression : ID ASSIGN idnum RANGE idnum"""

    def p_idnum(self, p):
        """ idnum : ID
                  | INTNUM
        """

    def p_print_expression(self, p):
        """ print_expression : STRING
                             | term
                             | print_expression COMMA print_expression
        """

    def p_assign_expression(self, p):
        """assign_expression : ID assign_op expression
        """

    def p_control_expression(self, p):
        """control_expression : BREAK
                              | CONTINUE
                              | RETURN INTNUM
        """

    def p_expression(self, p):
        """expression : expression op expression
                      | LPAREN expression RPAREN
                      | term
        """

    def p_assign_op(self, p):
        """assign_op : ASSIGN
                     | ADDASSIGN
                     | SUBASSIGN
                     | MULASSIGN
                     | DIVASSIGN
        """

    def p_op(self, p):
        """op : bin_op
              | rel_op
        """

    def p_bin_op(self, p):
        """bin_op : ADD
                  | SUB
                  | DIV
                  | MUL
        """

    def p_rel_op(self, p):
        """rel_op : GE
                  | GEQ
                  | LE
                  | LEQ
                  | EQ
                  | NEQ
        """

    def p_term(self, p):
        """term : ID
                | INTNUM
                | FLOATNUM
                | UMINUS term
        """
