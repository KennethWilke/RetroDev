from .lexer import lexer
from .common import tokens
import ply.yacc as yacc

def p_expressionlist_expressionlist(p):
    'expressionlist : expressionlist expression'
    p[0] = p[1] + [p[2]]

def p_expressionlist_expression(p):
    'expressionlist : expression'
    p[0] = [p[1]]

def p_expression_directive(p):
    'expression : DIRECTIVE argument'
    p[0] = (p[1], p[2])

def p_expression_label(p):
    "expression : IDENTIFIER ':'"
    p[0] = ('LABEL', p[1])

def p_assignment_set(p):
    "expression : IDENTIFIER '=' argument"
    p[0] = ('ASSIGNMENT', (p[1], p[3]))

def p_expression_instruction_noargs(p):
    'expression : INSTRUCTION'
    p[0] = (p[1], ())

def p_expression_instruction_immediate(p):
    "expression : INSTRUCTION '#' argument"
    p[0] = (p[1], ('IMMEDIATE', p[3]))

def p_expression_instruction_absolute(p):
    'expression : INSTRUCTION argument'
    p[0] = (p[1], ('ABSOLUTE', p[2]))

def p_expression_instruction_indirect(p):
    "expression : INSTRUCTION '(' argument ')'"
    p[0] = (p[1], ('INDIRECT', p[3]))

def p_expression_instruction_register(p):
    'expression : INSTRUCTION REGISTER'
    p[0] = (p[1], ('REGISTER', p[2]))

def p_expression_instruction_offset(p):
    "expression : INSTRUCTION argument ',' REGISTER"
    p[0] = (p[1], ('OFFSET', p[4], p[2]))

def p_expression_instruction_indirect_offset(p):
    "expression : INSTRUCTION '(' argument ',' REGISTER ')' "
    p[0] = (p[1], ('INDIRECT', p[5], p[3]))

def p_expression_instruction_indirect_offset2(p):
    "expression : INSTRUCTION '(' argument ')' ',' REGISTER "
    p[0] = (p[1], ('INDIRECT', p[6], p[3]))

def p_argument_hex(p):
    'argument : HEX'
    p[0] = int(p[1][1:], 16)

def p_argument_binary(p):
    'argument : BINARY'
    p[0] = int(p[1][1:], 2)

def p_argument_identifier(p):
    'argument : IDENTIFIER'
    p[0] = ('IDENTIFIER', p[1])

def p_argument_string(p):
    'argument : STRING'
    p[0] = p[1][1:-1]

def p_argument_number(p):
    'argument : NUMBER'
    p[0] = int(p[1])

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input! -- " + str(p)

# Build the parser
parser = yacc.yacc()
