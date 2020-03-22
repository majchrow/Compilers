import os

import ply.yacc as yacc

from lexer import Lexer


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Parser(object):
    tokens = Lexer.tokens

    precedence = (
        ('left', 'LCURLY', 'RCURLY'),
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('left', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'),
        ('nonassoc', 'GE', 'GEQ', 'LE', 'LEQ', 'EQ', 'NEQ'),
        ('left', 'ADD', 'SUB', 'DOTADD', 'DOTSUB', 'COMMA'),
        ('left', 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', 'UTRANS'),
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

    def p_expression(self, p):
        """expression : expression ADD expression
                      | expression SUB expression
                      | expression DIV expression
                      | expression MUL expression
                      | expression DOTADD expression
                      | expression DOTSUB expression
                      | expression DOTDIV expression
                      | expression DOTMUL expression
                      | expression GE expression
                      | expression GEQ expression
                      | expression LE expression
                      | expression LEQ expression
                      | expression EQ expression
                      | expression NEQ expression
        """

    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""

    def p_expression_variable(self, p):
        """expression : variable"""

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
        """ print_expression : variable COMMA print_expression
                             | variable
        """

    def p_control_expression(self, p):
        """control_expression : BREAK
                              | CONTINUE
                              | RETURN INTNUM
        """

    def p_assignment(self, p):
        """assignment : ID assign_op expression
                      | ID matrix_ref assign_op expression
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
        """matrix_rows : matrix_row SEMICOL matrix_rows
                       | matrix_row
        """

    def p_matrix_row(self, p):
        """matrix_row : variable COMMA matrix_row
                      | variable
        """
