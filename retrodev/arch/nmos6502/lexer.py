import ply.lex as lex
from .common import instruction_set, tokens, directives

# Token literals
literals = [',', ':', '#', '(', ')', '=']

t_ignore = ' \t'
# Token regex for simple types
t_HEX = r'\$[0-9a-fA-F]{1,4}'
t_STRING = r'\".*?[^\\]\"'
t_NUMBER = r'\-?\d+'


def t_COMMENT(t):
    r';.*'
    pass

def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    if t.value in ['A', 'X', 'Y']:
        t.type = 'REGISTER'
    elif t.value.upper() in instruction_set:
        t.type = 'INSTRUCTION'
        t.value = t.value.upper()
    return t

def t_DIRECTIVE(t):
    r'\.\w+'
    if t.value[1:].upper() in directives:
        t.value = t.value[1:].upper()
    return t

# Track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print "Parsing error on: {0}".format(t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
