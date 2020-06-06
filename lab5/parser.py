import os

import ply.yacc as yacc

from AST import *
from Exceptions import ReturnValueException
from Interpreter import Interpreter
from TypeChecker import TypeChecker
from scanner import Scanner


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Parser(object):
    tokens = Scanner.tokens

    precedence = (  # Higher position will be executed later in case of conflicts
        ('right', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('nonassoc', 'GE', 'GEQ', 'LE', 'LEQ', 'EQ', 'NEQ'),
        ('left', 'ADD', 'SUB', 'DOTADD', 'DOTSUB'),
        ('left', 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
        ('left', 'TRANS'),
        ('right', 'UMINUS'),
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE')
    )

    def __init__(self, start="program", outputdir="logs", tabmodule="baseparsetab"):
        create_dir(outputdir)
        self.ast = False
        self.type_check = False
        self.interpretation = False
        self.scanner = Scanner()
        self.type_checker = TypeChecker()
        self.interpreter = Interpreter()
        self.parser = yacc.yacc(module=self, start=start, tabmodule=tabmodule, outputdir=outputdir)
        self.error = False

    def parse(self, text, ast=False, type_check=False, interpretation=False):
        self.ast = ast
        self.type_check = type_check
        self.interpretation = interpretation
        self.error = False
        self.parser.parse(text)

    def p_error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}, column {self.scanner.find_tok_column(p)}:"
                  f"LexToken({p.type}, {p.value})")
        else:
            print("Unexpected end of input")
        self.error = True

    def p_empty(self, p):
        """empty :"""
        pass

    def p_program(self, p):
        """program : statements"""
        p[0] = p[1]
        if self.ast:
            if not self.error:
                p[0].printTree()
            else:
                print(f"Provided program has Syntax error, AST Tree won't be printed")
        if self.type_check:
            if not self.error:
                self.type_checker.visit(p[0])  # Prints all Type Errors (Syntax Errors are not allowed here)
            else:
                print(f"Provided program has Syntax error, Type Check won't be executed")
        if self.interpretation:
            if not self.type_check:
                print(f"Type Check is necessary for Interpretation, Interpretation won't be executed")
            else:
                if self.error:
                    print(f"Provided program has Syntax error, Interpretation won't be executed")
                elif self.type_checker.error:
                    print(f"Provided program has Type Error, Interpretation won't be executed")
                else:
                    try:
                        p[0].accept(self.interpreter)
                        print(f"No return statement found during interpretation")
                    except ReturnValueException as e:
                        print(f"Interpretation finished with exit code {e.value}")

    def p_statements(self, p):
        """statements : empty
                      | LCURLY statements RCURLY statements
                      | statement statements
        """
        if len(p) == 2:
            p[0] = Statements([])
        elif len(p) == 3:
            sts = p[2] if p[2] else Statements([])
            sts.statements = [p[1]] + sts.statements
            p[0] = sts
        else:
            outer = p[4] if p[4] else Statements([])
            inner = p[2] if p[2] else Statements([])
            outer.statements = [inner] + outer.statements
            p[0] = outer

    def p_block(self, p):
        """block : statement
                 | LCURLY statements RCURLY
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_statement(self, p):
        """statement : IF expression block %prec IFX
                     | IF expression block ELSE block
                     | WHILE expression block
                     | FOR for_expression block
                     | PRINT expressions SEMICOL
                     | control_expression SEMICOL
        """
        if p[1] == "if":
            p[0] = If(p[2], Block(p[3])) if len(p) == 4 else If(p[2], Block(p[3]), Block(p[5]),
                                                                lineno=self.scanner.lexer.lineno)
        elif p[1] == "while":
            p[0] = While(p[2], Block(p[3]), lineno=self.scanner.lexer.lineno)
        elif p[1] == "for":
            p[0] = For(p[2], Block(p[3]), lineno=self.scanner.lexer.lineno)
        elif p[1] == "print":
            p[0] = Print(p[2], lineno=self.scanner.lexer.lineno)
        else:  # control expression
            p[0] = p[1]

    def p_statement_assignments(self, p):
        """statement : assignments SEMICOL"""
        p[0] = Assignments(p[1], lineno=self.scanner.lexer.lineno)

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
        p[0] = BinOp(p[1], p[2], p[3], lineno=self.scanner.lexer.lineno)

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
        p[0] = Variable(p[1], lineno=self.scanner.lexer.lineno)

    def p_variable_id(self, p):
        """variable : ID"""
        p[0] = Variable(Id(p[1]), lineno=self.scanner.lexer.lineno)

    def p_variable_uminus(self, p):
        """variable : SUB variable %prec UMINUS"""
        p[0] = Variable(p[2].value, p[2].minus + 1, p[2].trans, lineno=self.scanner.lexer.lineno)

    def p_variable_trans(self, p):
        """variable : variable TRANS"""
        p[0] = Variable(p[1].value, p[1].minus, p[1].trans + 1, lineno=self.scanner.lexer.lineno)

    def p_const(self, p):
        """const : STRING
                 | FLOATNUM
                 | INTNUM
        """
        p[0] = p[1]

    def p_for_expression(self, p):
        """ for_expression : ID ASSIGN expression RANGE expression"""
        p[0] = ForExpr(Id(p[1]), p[3], p[5], lineno=self.scanner.lexer.lineno)

    def p_expressions(self, p):
        """ expressions : expression COMMA expressions
                        | expression
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_expressions_empty(self, p):
        """ expressions : empty """
        p[0] = []

    def p_control_expression(self, p):
        """control_expression : BREAK
                              | CONTINUE
                              | RETURN expressions
        """
        if p[1] == "break":
            p[0] = Break(lineno=self.scanner.lexer.lineno)
        elif p[1] == "continue":
            p[0] = Continue(lineno=self.scanner.lexer.lineno)
        else:  # RETURN
            p[0] = Return(p[2], lineno=self.scanner.lexer.lineno)

    def p_assignments(self, p):
        """assignments : assignment COMMA assignments
                       | assignment
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_assignments_empty(self, p):
        """assignments : empty """
        p[0] = []

    def p_assignment(self, p):
        """assignment : ID assign_op expression
                      | ID LBRACKET expressions RBRACKET assign_op expression
        """
        if len(p) == 7:
            p[0] = Assignment(Id(p[1]), p[5], p[6], p[3], lineno=self.scanner.lexer.lineno)
        else:
            p[0] = Assignment(Id(p[1]), p[2], p[3], lineno=self.scanner.lexer.lineno)

    def p_assign_op(self, p):
        """assign_op : ASSIGN
                     | ADDASSIGN
                     | SUBASSIGN
                     | MULASSIGN
                     | DIVASSIGN
        """
        p[0] = p[1]

    def p_matrix_special(self, p):
        """matrix : EYE LPAREN expressions RPAREN
                  | ZEROS LPAREN expressions RPAREN
                  | ONES LPAREN expressions RPAREN
        """
        p[0] = SpecialMatrix(p[1], p[3], lineno=self.scanner.lexer.lineno)

    def p_matrix(self, p):
        """matrix : vector"""
        p[0] = SimpleMatrix(p[1], lineno=self.scanner.lexer.lineno)

    def p_vector(self, p):
        """vector : LBRACKET outer_list RBRACKET"""
        p[0] = p[2]

    def p_outerlist(self, p):
        """outer_list : outer_list SEMICOL inner_list
                      | inner_list
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + [';'] + p[3]  # Keep track of SEMICOL, for inputs like [1;2,3,4]

    def p_innerlist(self, p):
        """inner_list : inner_list COMMA elem
                      | elem
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_innerlist_empty(self, p):
        """inner_list : empty """
        p[0] = []

    def p_elem(self, p):
        """elem : const
                | vector
        """
        p[0] = p[1]

    def p_elem_id(self, p):
        """elem : ID"""
        p[0] = Id(p[1], lineno=self.scanner.lexer.lineno)
