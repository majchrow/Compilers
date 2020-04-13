import ply.lex as lex


class Scanner(object):
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT'
    }

    tokens = ['ASSIGN', 'SUB', 'ADD', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'ID',
              'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 'ADDASSIGN', 'SUBASSIGN',
              'MULASSIGN', 'DIVASSIGN', 'GE', 'GEQ', 'LE', 'LEQ', 'NEQ', 'EQ',
              'LBRACKET', 'RBRACKET', 'LCURLY', 'RCURLY', 'RANGE', 'TRANS',
              'COMMA', 'SEMICOL', 'INTNUM', 'FLOATNUM', 'STRING'] + list(reserved.values())

    t_ASSIGN = r'='
    t_SUB = r'-'
    t_ADD = r'\+'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_DOTADD = r'\.\+'
    t_DOTSUB = r'\.-'
    t_DOTMUL = r'\.\*'
    t_DOTDIV = r'\./'
    t_ADDASSIGN = r'\+='
    t_SUBASSIGN = r'\-='
    t_MULASSIGN = r'\*='
    t_DIVASSIGN = r'/='
    t_GE = r'>'
    t_GEQ = r'>='
    t_LE = r'<'
    t_LEQ = r'<='
    t_NEQ = r'!='
    t_EQ = r'=='
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_RANGE = r':'
    t_TRANS = r'\''
    t_COMMA = r'\,'
    t_SEMICOL = r';'
    t_IF = r'if'
    t_ELSE = r'else'
    t_FOR = r'for'
    t_WHILE = r'while'
    t_BREAK = r'break'
    t_CONTINUE = r'continue'
    t_RETURN = r'return'
    t_EYE = r'eye'
    t_ZEROS = r'zeros'
    t_ONES = r'ones'
    t_PRINT = r'print'

    t_ignore = ' \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_FLOATNUM(self, t):
        r'\d+\.\d*|\.\d+'
        t.value = float(t.value)
        return t

    def t_INTNUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_](\w|_)*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_STRING(self, t):
        r'\".*\"|\'.*\''
        return t

    def t_COMMENT(self, t):  # ignore comments
        r'\#.*'
        pass

    def t_newline(self, t):
        r'\r?\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"({t.lexer.lineno}): ERROR: Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    def find_tok_column(self, token):
        line_start = self.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
