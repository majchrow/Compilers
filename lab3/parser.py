import os

import ply.yacc as yacc

from AST import *
from scanner import Scanner


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Parser(object):
    tokens = Scanner.tokens

    precedence = (
        ('left', 'LCURLY', 'RCURLY'),
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('left', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'),
        ('nonassoc', 'GE', 'GEQ', 'LE', 'LEQ', 'EQ', 'NEQ'),
        ('left', 'ADD', 'SUB', 'DOTADD', 'DOTSUB'),
        ('left', 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', 'UTRANS'),
    )

    def __init__(self, start="program", outputdir="logs", tabmodule="baseparsetab"):
        create_dir(outputdir)
        self.ast = False
        self.scanner = Scanner()
        self.parser = yacc.yacc(module=self, start=start, tabmodule=tabmodule, outputdir=outputdir)

    def parse(self, text, ast=False):
        self.ast = ast
        self.parser.parse(text)

    def p_error(self, p):  # Syntax error handler
        if p:
            print(f"Syntax error at line {p.lineno}, column {self.scanner.find_tok_column(p)}:"
                  f"LexToken({p.type}, {p.value})")
        else:
            print("Unexpected end of input")

    def p_empty(self, p):  # Empty production
        """empty :"""
        pass

    def p_program(self, p):
        """program : statements"""
        p[0] = p[1]
        if self.ast:
            p[0].printTree()

    def p_statements(self, p):
        """statements : empty
                      | LCURLY statements RCURLY
                      | statement statements
        """
        if len(p) == 2:
            p[0] = Statements()
        elif len(p) == 3:
            sts = p[2] if p[2] else Statements()
            sts.statements.append(p[1])
            p[0] = sts
        else:
            p[0] = p[2] if p[2] else Statements()

    def p_block(self, p):
        """block : statement
                 | LCURLY statements RCURLY
        """
        if len(p) == 2:
            p[0] = Statements([p[1]])
        else:
            p[0] = p[2]

    def p_statement(self, p):
        """statement : IF expression block %prec IFX
                     | IF expression block ELSE block
                     | WHILE expression block
                     | FOR for_expression block
                     | PRINT print_expression SEMICOL
                     | assignment SEMICOL
                     | control_expression SEMICOL
        """
        if p[1] == "if":
            p[0] = If(p[2], p[3]) if len(p) == 4 else If(p[2], p[3], p[5])
        elif p[1] == "while":
            p[0] = While(p[2], p[3])
        elif p[1] == "for":
            p[0] = For(p[2], p[3])
        elif p[1] == "print":
            p[0] = Print(p[2])
        else:  # assignment or control expression
            p[0] = p[1]

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
        p[0] = BinOp(p[1], p[2], p[3])

    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_expression_variable(self, p):
        """expression : variable"""
        p[0] = p[1]

    def p_variable(self, p):
        """variable : const
                    | matrix
        """
        p[0] = p[1]

    def p_variable_id(self, p):
        """variable : ID"""
        p[0] = Variable(Id(p[1]), Id)

    def p_variable_uminus(self, p):
        """variable : SUB variable %prec UMINUS"""
        p[0] = Variable(p[2].value, p[2].var_type, not p[2].minus, p[2].trans)

    def p_variable_trans(self, p):
        """variable : variable TRANS %prec UTRANS"""
        p[0] = Variable(p[1].value, p[1].var_type, p[1].minus, not p[1].trans)

    def p_const(self, p):
        """const : STRING
                 | FLOATNUM
                 | INTNUM
        """
        p[0] = Variable(p[1], type(p[1]))

    def p_for_expression(self, p):
        """ for_expression : ID ASSIGN variable RANGE variable"""
        p[0] = ForExpr(p[1], p[3], p[5])

    def p_print_expression(self, p):
        """ print_expression : variable COMMA print_expression
                             | variable
        """
        if len(p) == 2:
            p[0] = PrintExpr(p[1])
        else:
            p[3].variables.append(p[1])
            p[0] = p[3]

    def p_control_expression(self, p):
        """control_expression : BREAK
                              | CONTINUE
                              | RETURN variable
        """
        if p[1] == "break":
            p[0] = Break()
        elif p[1] == "continue":
            p[0] = Continue()
        else:  # RETURN
            p[0] = Return(p[2])

    def p_assignment(self, p):
        """assignment : ID assign_op expression
                      | ID LBRACKET variable COMMA variable RBRACKET assign_op expression
        """
        if len(p) == 9:
            p[0] = Assignment(p[1], p[7], p[8], (p[3], p[5]))
        else:
            p[0] = Assignment(p[1], p[2], p[3])

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
        p[0] = SpecialMatrix(p[1], p[3])

    def p_matrix(self, p):
        """matrix : LBRACKET matrix_rows RBRACKET"""
        p[0] = SimpleMatrix(p[2])

    def p_matrix_rows(self, p):
        """matrix_rows : matrix_row SEMICOL matrix_rows
                       | matrix_row
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            rows = p[3] if p[3] else []
            rows.append(p[1])
            p[0] = rows

    def p_matrix_row(self, p):
        """matrix_row : variable COMMA matrix_row
                      | variable
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            row = p[3] if p[3] else []
            row.append(p[1])
            p[0] = row
