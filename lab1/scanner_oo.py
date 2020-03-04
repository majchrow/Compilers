import ply.lex as lex
import sys


tokens = ( 'ASSIGN', 'SUB', 'ADD', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'ZEROS', 
        'ID', 'ONES', 
        'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 
        'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN','DIVASSIGN',
        'GREATER', 'GEQ', 'LESSER', 'LEQ', 'DIFF', 'EQ', 
        'LBRACKET', 'RBRACKET', 'LCURLY', 'RCURLY', 'RANGE', 
        'TRANS', 'COMMA', 'SEMICOL',
       'IF', 'ELSE', 'FOR', 'WHILE', 'BREAK', 'CONTINUE', 'RETURN', 'EYE', 'ZEROS', 'ONES',
      'PRINT', 'INTNUM', 'FLOATNUM')
      # , 'STRING')

reserved = {
    'if'        : 'IF',
    'else'      : 'ELSE',
    'for'       : 'FOR',
    'while'     : 'WHILE',
    'break'     : 'BREAK',
    'continue'  : 'CONTINUE',
    'return'    : 'RETURN',
    'eye'       : 'EYE',
    'zeros'     : 'ZEROS',
    'ones'      : 'ONES',
    'print'     : 'PRINT'
}
 

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
t_GREATER = r'>'
t_GEQ = r'>='
t_LESSER = r'<'
t_LEQ = r'<='
t_DIFF = r'!='
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


def t_FLOATNUM(t):
    r'(\d+\.\d*|\.\d+)'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_](\w|_)*'
    t.type = reserved.get(t.value,'ID')
    return t

t_ignore= ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno +=len(t.value)

def t_error(t):
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
fh = open(sys.argv[1], "r")
lexer.input( fh.read() )
for token in lexer:
    print("line %d: %s(%s)" %(token.lineno, token.type, token.value))
