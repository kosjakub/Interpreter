import sys
import ply.lex as lex

reserved = {
    'if'       : 'IF'      ,
    'else'     : 'ELSE'    ,
    'for'      : 'FOR'     ,
    'while'    : 'WHILE'   ,
    'break'    : 'BREAK'   ,
    'continue' : 'CONTINUE',
    'return'   : 'RETURN'  ,
    'eye'      : 'EYE'     ,
    'zeros'    : 'ZEROS'   ,
    'ones'     : 'ONES'    ,
    'print'    : 'PRINT'   
}


tokens = ['DOTADD', 'DOTMINUS', 'DOTMUL', 'DOTDIV', 'ADDASSIGN', 'SUBASSIGN',
        'MULASSIGN', 'DIVASSIGN', 'LESSEREQ', 'GREATEREQ', 'NOTEQ', 'EQ',
        'INTNUM', 'FLOATNUM', 'ID'] + list(reserved.values())
  
t_DOTADD    = r'\.\+'
t_DOTMINUS  = r'\.\-'
t_DOTMUL    = r'\.\*'
t_DOTDIV    = r'\.\/'
t_ADDASSIGN = r'\+\='
t_SUBASSIGN = r'\-\='
t_MULASSIGN = r'\*\='
t_DIVASSIGN = r'\/\='
t_LESSEREQ  = r'\<\='
t_GREATEREQ = r'\>\='
t_NOTEQ     = r'\!\='
t_EQ        = r'\=\='

  
literals = "+-*/()[]{}':;,=<>"

def t_FLOATNUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value,'ID')
    return t

    
t_ignore = '  \t'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_python_comment(t):
    r'(\'\'\'(.|\n)*?\'\'\')|(\#.*)'
    pass

def t_error(t):
    print("line [%d]: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
  
if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = lex.lex() 
    lexer.input(text) # Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break    # No more input
        column = find_column(text,tok)
        print("(%d : %d): %s(%s)" %(tok.lineno, column, tok.type, tok.value))

        