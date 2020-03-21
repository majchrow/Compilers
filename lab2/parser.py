import ply.yacc as yacc

from lexer import Lexer


class Parser(object):
    tokens = Lexer.tokens

    precedence = (
        # to fill ...
        # ("left", '+', '-')
        # to fill ...
    )

    # to finish the grammar
    # ....

    def __init__(self, outputdir="logs", start="expression", tabmodule="baseparsetab"):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self,
                                start=start,
                                tabmodule=tabmodule,
                                outputdir=outputdir)

    def parse(self, text):
        self.parse(text)

    def p_error(self, p):
        # if p:
        #     print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
        #                                                                               scanner.find_tok_column(p),
        #                                                                               p.type, p.value))
        # else:
        print("Unexpected end of input")

    def p_program(self, p):
        """program : instructions_opt"""
        return

    def p_instructions_opt_1(self, p):
        """instructions_opt : instructions """

    def p_instructions_opt_2(self, p):
        """instructions_opt : """

    def p_instructions_1(self, p):
        """instructions : instructions instruction """

    def p_instructions_2(self, p):
        """instructions : instruction """
