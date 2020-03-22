import os

import ply.yacc as yacc

from lexer import Lexer


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Parser(object):
    tokens = Lexer.tokens + ('UMINUS',)

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('nonassoc', 'GE', 'GEQ', 'LE', 'LEQ', 'EQ', 'NEQ'),
        ('left', 'ADD', 'SUB', 'DOTADD', 'DOTSUB', 'COMMA'),
        ('left', 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'),
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

    def p_block(self, p):
        """block : statement
                 | LCURLY statements RCURLY
        """

    def p_statement(self, p):
        """statement : IF boolean_expression block %prec IFX
                     | IF boolean_expression block ELSE block
                     | WHILE boolean_expression block
                     | FOR for_expression block
                     | PRINT print_expression SEMICOL
                     | assign_id SEMICOL
                     | control_expression SEMICOL
        """

    def p_boolean_expression(self, p):
        """boolean_expression : term GE term
                              | term GEQ term
                              | term LE term
                              | term LEQ term
                              | term EQ term
                              | term NEQ term
        """

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

    def p_assign_id_factor(self, p):
        """assign_id : ID ASSIGN factor
                     | ID ADDASSIGN factor
                     | ID SUBASSIGN factor
                     | ID MULASSIGN factor
                     | ID DIVASSIGN factor
        """

    def p_assign_id_matrix(self, p):
        """assign_id : ID ASSIGN matrix_expression
                     | ID ASSIGN matrix
                     | ID ASSIGN ID TRANS
                     | ID LBRACKET INTNUM COMMA INTNUM RBRACKET ASSIGN term
        """

    def p_control_expression(self, p):
        """control_expression : BREAK
                              | CONTINUE
                              | RETURN INTNUM
        """

    def p_expression(self, p):  # It does not produce ID without expression
        """expression : factor ADD factor
                      | factor SUB factor
                      | factor DIV factor
                      | factor MUL factor
        """

    def p_factor(self, p):
        """factor : expression
                  | LPAREN expression RPAREN
                  | term
                  | SUB factor %prec UMINUS
        """

    def p_term(self, p):
        """term : ID
                | INTNUM
                | FLOATNUM
                | UMINUS term
        """

    def p_matrix_special(self, p):
        """matrix : EYE LPAREN INTNUM RPAREN
                  | ZEROS LPAREN INTNUM RPAREN
                  | ONES LPAREN INTNUM RPAREN
        """

    def p_matrix(self, p):
        """matrix : LBRACKET matrix_rows RBRACKET
        """

    def p_matrix_rows(self, p):
        """matrix_rows : matrix_rows SEMICOL matrix_row
                       | matrix_row
        """

    def p_matrix_row(self, p):
        """matrix_row : matrix_row COMMA term
                      | term
        """

    def p_matrix_expression(self, p):
        """matrix_expression : matrix_factor DOTADD matrix_factor
                             | matrix_factor DOTSUB matrix_factor
                             | matrix_factor DOTDIV matrix_factor
                             | matrix_factor DOTMUL matrix_factor
        """

    def p_matrix_factor(self, p):
        """matrix_factor : matrix_expression
                         | LPAREN matrix_expression RPAREN
                         | ID
        """
