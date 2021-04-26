import scanner as scann
import ply as ply


class Node(object):
    def __init__(self, lineno):
        self.lineno = lineno
    def accept(self, visitor):
        return visitor.visit(self)

class Variable(Node):
    def __init__(self, id, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.id = id
  
class Id(Node):
    def __init__(self, id):
        self.id = id
        
class Constant(Node):
    def __init__(self, constant):
        self.constant = constant
        
class Matrix(Node):
    def __init__(self, vectors, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.vectors = vectors
        
class Vector(Node):
    def __init__ (self, values):
        self.values = values
    def add_value(self, x):
        self.values.append(x)
    
    
class ArrayExp(Node):
    def __init__ (self, id, vector, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.id = id
        self.vector = vector

class Range(Node):
    def __init__ (self, start, end):
        self.start = start
        self.end = end
        
class Zeros(Node):
    def __init__(self, exp):
        self.exp = exp

class Ones(Node):
    def __init__(self, exp):
        self.exp = exp

class Eye(Node):
    def __init__(self, exp):
        self.exp = exp

class Print(Node):
    def __init__(self, exp):
        self.exp = exp
        
class Return(Node):
    def __init__(self, exp):
        self.exp = exp
          
class Continue(Node):
    def __init__(self, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
    
class Break(Node):
    def __init__(self, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
    
class AssignmentExpression(Node):
    def __init__(self, lexp, operator, rexp):
        self.lexp = lexp
        self.operator = operator
        self.rexp = rexp

class InitExpression(Node):
    def __init__(self, lexp, operator, rexp, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.lexp = lexp
        self.operator = operator
        self.rexp = rexp        
        
class IfStatement(Node):
    def __init__(self, exp, stat_list):
        self.exp = exp
        self.stat_list = stat_list

class IfElseStatement(Node):
    def __init__(self, exp, stat_list, else_stat_list):
        self.exp = exp
        self.stat_list = stat_list
        self.else_stat_list = else_stat_list
        
class WhileStatement(Node):
    def __init__(self, condition, stat_list):
        self.condition = condition
        self.stat_list = stat_list
        

class ForStatement(Node):
    def __init__(self, exp, stat_list):
        self.exp = exp 
        self.stat_list = stat_list
        
class OperationExp(Node):
    def __init__(self, lexp, operator, rexp, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.lexp = lexp
        self.operator = operator
        self.rexp = rexp

class MatrixExp(Node):
    def __init__(self, lexp, operator, rexp, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.lexp = lexp
        self.operator = operator
        self.rexp = rexp
        
class RelationalExp(Node):
    def __init__(self, lexp, relation, rexp, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.lexp = lexp
        self.relation = relation
        self.rexp = rexp
  
class Statements(Node):
    def __init__(self, statements):
        self.statements = statements
        
class Statement(Node):
    def __init__(self, statement):
        self.statement = statement

class UnaryExp(Node):
    def __init__(self, operator, val, p):
        for x in p.__dict__.get('slice'):
            if isinstance(x, ply.lex.LexToken):
                self.lineno = x.lineno
        self.operator = operator
        self.val = val
        
class Eostmt(Node):
    def __init__(self, sign):
        self.sign = sign