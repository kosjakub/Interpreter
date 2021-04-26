import scanner
import ply.yacc as yacc
import time 
import AST as c
import TreePrinter
tokens = scanner.tokens

precedence = (
    ("right", ","),
    ("right", "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN", "="),
    ("left", "EQ", "NOTEQ", "GREATEREQ", "LESSEREQ", ">", "<"),
    ('left', '+', '-', 'DOTADD', 'DOTMINUS'),
    ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
    ("right", "'"),
    ("nonassoc",  "{", "}")
)

def p_program(p):
    '''program : statement_list '''
    
    p[0] = c.Statements(p[1])

def p_primary_expression(p):
    '''primary_expression   : ID
                            | INTNUM
                            | FLOATNUM
                            | '(' expression ')'
                            | '[' ']'
                            | '[' index_expression_list ']' '''
    if len(p) > 2:
        if p[1] == '[' and p[2] == ']':
            p[0] = "[]"
        elif p[1] == '[' and p[3] == ']':
            p[0] = c.Matrix(p[2] if isinstance(p[2][0], c.Vector) else [c.Vector(p[2])])
    elif isinstance(p[1], str):
        p[0] = c.Id(p[1])
    elif isinstance(p[1], (int, float)) :
        p[0] = c.Constant(p[1])
    

def p_postfix_expression(p):
    '''postfix_expression   : primary_expression
                            | array_expression
                            | postfix_expression "'" '''
    
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = c.UnaryExp("'", p[1])
    
def p_index_expression(p):
    '''index_expression     : ':'
                            | expression '''
    p[0] = p[1]

def p_index_expression_list(p):
    '''index_expression_list : index_expression 
                             | index_expression_list ',' index_expression
                             | index_expression_list ';' index_expression_list '''
    #print("\n\n\n")
    if len(p) == 2:      
        p[0] = [p[1]] 
    elif p[2] == ",": 
        p[0] = p[1] 
        p[0].append(p[3])
    elif p[2] == ";":  
        p[0] = [c.Vector(p[1])]
        
        
        if isinstance(p[3][0], c.Vector):
            for v in p[3]:
                p[0].append(v)
        else:
            p[0].append(c.Vector(p[3]))
        
            
def p_print_index_expression_list(p):
    '''print_index_expression_list  : ID
                                    | print_index_expression_list ',' ID  '''
    if len(p) == 2:
        p[0] = [c.Id(p[1])] 
    elif p[2] == ",":
        p[0] = p[1] 
        p[0].append(c.Id(p[3]))
        pass
        
def p_array_expression(p):
    '''array_expression : ID '(' index_expression_list ')' 
                        | ID '[' index_expression_list ']' 
                        '''
    if p[2] == '(' and p[4] == ')':
        p[0] = c.ArrayExp(c.Id(p[1]), p[3])
    elif p[2] == '[' and p[4] == ']':
        p[0] = c.ArrayExp(c.Id(p[1]), p[3])
   


def p_unary_expression(p):
    '''unary_expression     : postfix_expression
                            | '-' postfix_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = c.UnaryExp("-", p[2])

      
def p_multiplicative_expression(p):
    '''multiplicative_expression    : unary_expression
                                    | multiplicative_expression '*' unary_expression
                                    | multiplicative_expression '/' unary_expression 
                                    | multiplicative_expression DOTMUL unary_expression
                                    | multiplicative_expression DOTDIV unary_expression '''
    if len(p) > 2:
        if p[2] == '*':
            p[0] = c.OperationExp(p[1], '*', p[3])
        elif p[2] == '/':
            p[0] = c.OperationExp(p[1], '/', p[3])
        elif p[2] == ".*":
            p[0] = c.MatrixExp(p[1], '.*', p[3])
        elif p[2] == "./":
            p[0] = c.MatrixExp(p[1], './', p[3])
    else:
        p[0] = p[1]

def p_additive_expression(p):
    '''additive_expression  : multiplicative_expression
                            | additive_expression '+' multiplicative_expression
                            | additive_expression '-' multiplicative_expression
                            | additive_expression DOTADD multiplicative_expression
                            | additive_expression DOTMINUS multiplicative_expression                            '''

    
    
    
    if len(p) > 2:
        if p[2] == '+':
            p[0] = c.OperationExp(p[1], '+', p[3])
        elif p[2] == '-':
            p[0] = c.OperationExp(p[1], '-', p[3])
        elif p[2] == ".+":
            p[0] = c.MatrixExp(p[1], '.+', p[3])
        elif p[2] == ".-":
            p[0] = c.MatrixExp(p[1], '.-', p[3])
    else:
        p[0] = p[1]  

def p_relational_expression(p):
    '''relational_expression    : additive_expression
                                | relational_expression '<' additive_expression
                                | relational_expression '>' additive_expression
                                | relational_expression LESSEREQ additive_expression
                                | relational_expression GREATEREQ additive_expression '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "<":
        p[0] = c.RelationalExp(p[1], "<", p[3])
    elif p[2] == ">":
        p[0] = c.RelationalExp(p[1], ">", p[3])
    elif p[2] == "<=":
        p[0] = c.RelationalExp(p[1], "<=", p[3])
    elif p[2] == ">=":
        p[0] = c.RelationalExp(p[1], ">=", p[3])
    
def p_equality_expression(p):
    '''equality_expression  : relational_expression
                            | equality_expression EQ relational_expression
                            | equality_expression NOTEQ relational_expression '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "==":
        p[0] = c.RelationalExp(p[1], "==", p[3])
    elif p[2] == "!=":
        p[0] = c.RelationalExp(p[1], "!=", p[3])
    
def p_special_expression(p):
    '''special_expression   : equality_expression
                            | ZEROS '(' additive_expression ')'
                            | ONES '(' additive_expression ')'
                            | EYE '(' additive_expression ')' 
                            | PRINT print_index_expression_list 
                            | PRINT NORMSTRING 
                            | RETURN postfix_expression
                            | CONTINUE
                            | BREAK'''
    if len(p) == 2:
       p[0] = p[1]
    elif len(p) > 2:
       if p[1] == "zeros":
           p[0] = c.Zeros(p[3])
       elif p[1] == "ones":
           p[0] = c.Ones(p[3])
       elif p[1] == "eye":
           p[0] = c.Eye(p[3])
       elif p[1] == "print":
           p[0] = c.Print(p[2])
       elif p[1] == "return":
           p[0] = c.Return(p[2])
       elif p[1] == "continue":
           p[0] = c.Continue()
       elif p[1] == "break":
           p[0] = c.Break()
            
            
def p_expression(p):
    '''expression   : special_expression
                    | expression ':' special_expression '''
    
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = c.Range(p[1], p[3])
    
def p_assignment_expression(p):
    '''assignment_expression    : postfix_expression '=' expression
                                | postfix_expression ADDASSIGN expression
                                | postfix_expression SUBASSIGN expression
                                | postfix_expression MULASSIGN expression
                                | postfix_expression DIVASSIGN expression'''
    if p[2] == "=":
        p[0] = c.AssignmentExpression(p[1], "=", p[3])
    elif p[2] == "+=":
        p[0] = c.AssignmentExpression(p[1], "+=", p[3])
    elif p[2] == "-=":                                 
        p[0] = c.AssignmentExpression(p[1], "-=", p[3])
    elif p[2] == "*=":                                 
        p[0] = c.AssignmentExpression(p[1], "*=", p[3])
    elif p[2] == "/=":                                 
        p[0] = c.AssignmentExpression(p[1], "/=", p[3])
        
def p_eostmt(p):
    '''eostmt   :  ','
                |  ';' '''
    p[0] = c.Eostmt(";")

def p_statement(p):
    '''statement    : assignment_statement
                    | expression_statement
                    | selection_statement
                    | iteration_statement '''
    
    p[0] = p[1]
    
    
def p_statement_list(p):
    '''statement_list    : statement
                         | statement statement_list '''
    
    if len(p) == 2:
        p[0] = c.Statement(p[1])
    else:
        p[0] = [c.Statement(p[1])]
        p[0].append(c.Statements(p[2]))
 
def p_expression_statement(p):
    '''expression_statement     : eostmt
                                | expression eostmt'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1]]
        p[0].append(p[2])
        
def p_assignment_statement(p):
    '''assignment_statement     : assignment_expression eostmt '''    
    p[0] = p[1]
 
def p_selection_statement(p):
    '''selection_statement  : IF '(' expression ')' statement 
                            | IF '(' expression ')' statement ELSE statement 
                            | IF '(' expression ')' '{' statement_list '}'
                            | IF '(' expression ')' '{' statement_list '}' ELSE '{' statement_list '}'
                            '''
    
    if len(p) == 6:
        p[0] = c.IfStatement(p[3], [p[5]])
    elif len(p) == 8 and p[6] == 'else':
        p[0] = c.IfElseStatement(p[3], p[5], p[7])
    elif len(p) == 8 and p[6] != 'else':
        p[0] = c.IfStatement(p[3], p[6] if isinstance(p[6], list) else [p[6]])
    
        
def p_iteration_statement(p):
    '''iteration_statement  : WHILE '(' expression ')' '{' statement_list '}'
                            | FOR ID '=' expression '{' statement_list '}' 
                            | FOR '(' ID '=' expression ')' '{' statement_list '}'  '''
    if p[1] == "while":
        p[0] = c.WhileStatement(p[3], p[6] if isinstance(p[6], list) else [p[6]])
    elif p[1] == "for" and p[2] == '(':
        p[0] = c.ForStatement(c.Id(p[3]), p[5], p[8])
    else:
        p[0] = c.ForStatement(c.Id(p[2]), p[4], p[6])
        
# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error - line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, 0, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()
