import os

import ply.yacc as yacc

from lexer import Lexer


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Parser(object):
    tokens = Lexer.tokens

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('nonassoc', 'GE', 'GEQ', 'LE', 'LEQ', 'EQ', 'NEQ'),
        ('left', 'ADD', 'SUB', 'DOTADD', 'DOTSUB', 'COMMA'),
        ('left', 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', 'UTRANS'),
        ('left', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'),
        ('left', 'LCURLY', 'RCURLY'),

    )

    def __init__(self, start="statements", outputdir="logs", tabmodule="baseparsetab"):
        create_dir(outputdir)
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, start=start, tabmodule=tabmodule, outputdir=outputdir)

    def parse(self, text):
        self.parser.parse(text)

    def p_error(self, p):  # Syntax error handler
        if p:
            print(f"Syntax error at line {p.lineno}, column {self.lexer.find_tok_column(p)}:"
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

    def p_block(self, p):
        """block : statement
                 | LCURLY statements RCURLY
        """

    def p_statement(self, p):
        """statement : IF expression block %prec IFX
                     | IF expression block ELSE block
                     | WHILE expression block
                     | FOR for_expression block
                     | PRINT print_expression SEMICOL
                     | assignment SEMICOL
                     | control_expression SEMICOL
        """

    def p_boolean_expression(self, p):
        """expression : expression binary_op expression
                      | LPAREN expression RPAREN
                      | variable
        """

    def p_binary_op(self, p):
        """binary_op : ADD
                     | SUB
                     | DIV
                     | MUL
                     | DOTADD
                     | DOTSUB
                     | DOTDIV
                     | DOTMUL
                     | GE
                     | GEQ
                     | LE
                     | LEQ
                     | EQ
                     | NEQ
        """
        p[0] = p[1]

    def p_variable(self, p):
        """variable : ID
                    | const
                    | matrix
        """

    def p_variable_uminus(self, p):
        """variable : SUB variable %prec UMINUS"""

    def p_variable_trans(self, p):
        """variable : variable TRANS %prec UTRANS"""

    def p_const(self, p):
        """const : STRING
                 | FLOATNUM
                 | INTNUM
        """

    def p_for_expression(self, p):
        """ for_expression : ID ASSIGN variable RANGE variable"""

    def p_print_expression(self, p):
        """ print_expression : variable
                             | print_expression COMMA print_expression
        """

    def p_control_expression(self, p):
        """control_expression : BREAK
                              | CONTINUE
                              | RETURN INTNUM
        """

    def p_assignment(self, p):
        """assignment : ID assign_op expression
                      | ID matrix_ref assign_op expression
                      | ID assign_op expression TRANS
        """

    def p_matrix_ref(self, p):
        """matrix_ref : LBRACKET variable COMMA variable RBRACKET"""

    def p_assign_op(self, p):
        """assign_op : ASSIGN
                     | ADDASSIGN
                     | SUBASSIGN
                     | MULASSIGN
                     | DIVASSIGN
        """
        p[0] = p[1]

    def p_matrix_special(self, p):
        """matrix : EYE LPAREN variable RPAREN
                  | ZEROS LPAREN variable RPAREN
                  | ONES LPAREN variable RPAREN
        """

    def p_matrix(self, p):
        """matrix : LBRACKET matrix_rows RBRACKET"""

    def p_matrix_rows(self, p):
        """matrix_rows : matrix_rows SEMICOL matrix_row
                       | matrix_row
        """

    def p_matrix_row(self, p):
        """matrix_row : matrix_row COMMA variable
                      | variable
        """
