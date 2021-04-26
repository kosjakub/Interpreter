
import AST as AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np
import warnings

warnings.filterwarnings('error')

sys.setrecursionlimit(10000)

func_table = {'+' : lambda x, y : x + y,
              '-' : lambda x, y : np.subtract(x, y),
              '*' : lambda x, y : np.multiply(x, y),
              '/' : lambda x, y : np.divide(x, y),
              '.+' : lambda x, y : x + y,
              '.-' : lambda x, y : np.subtract(x, y),
              '.*' : lambda x, y : np.multiply(x, y),
              './' : lambda x, y : np.divide(x, y),
              '+=' : lambda x, y : np.add(x, y),
              '-=' : lambda x, y : np.subtract(x, y),
              '*=' : lambda x, y : np.multiply(x, y),
              '/=' : lambda x, y : np.divide(x, y),
              "'" : lambda x : np.transpose(x),
              "<" : lambda x, y : x < y,
              ">" : lambda x, y : x > y,
              "<=" : lambda x, y : x <= y,
              ">=" : lambda x, y : x >= y,
              "==" : lambda x, y : x == y,
              "!=" : lambda x, y : x != y
}

class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Constant)
    def visit(self, node):
        if isinstance(node.constant, int):
            return int(node.constant)
        return float(node.constant)

    @when(AST.Variable)
    def visit(self, node):
        return self.memoryStack.get(node.id)

    @when(AST.Matrix)
    def visit(self, node):
        vec = []
        for v in node.vectors:
            tmp_vec = []
            for x in v.values:
                tmp_val = x.accept(self)
                tmp_vec.append(tmp_val)
            vec.append(tmp_vec)
        # print np.matrix(vec)
        return np.matrix(vec)
    
    @when(AST.Zeros)
    def visit(self, node):
        return np.zeros(node.exp)

    @when(AST.Eye)
    def visit(self, node):
        return np.eye(node.exp)

    @when(AST.Ones)
    def visit(self, node):
        return np.ones(node.exp)
            
    @when(AST.Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return range(start, end)

    @when(AST.Print)
    def visit(self, node):
        if isinstance(node.exp, str):
            print node.exp
        else:
            tmp_list = []
            for x in node.exp:
                tmp_list.append(x.accept(self))
            print tmp_list


    @when(AST.OperationExp)
    def visit(self, node):
        r1 = node.lexp.accept(self)
        r2 = node.rexp.accept(self)
        try:
            return func_table[node.operator](r1, r2)
        except RuntimeWarning as e:
            print e, " in line ", node.lexp.lineno
        except TypeError as e:
            print e, " in line ", node.lexp.lineno

    @when(AST.InitExpression)
    def visit(self, node):
        expr = node.rexp.accept(self)
        self.memoryStack.insert(node.lexp.id, expr)
        return expr

    @when(AST.AssignmentExpression)
    def visit(self, node):
        lexp = node.lexp.accept(self)
        rexp = node.rexp.accept(self)
        if isinstance(node.lexp, AST.ArrayExp):
            tmp_val = node.lexp.id.accept(self)
            tmp_tab = []
            for x in node.lexp.vector:
                tmp = x.accept(self) - 1
                tmp_tab.append(tmp)
            tmp_val.put(tmp_tab, rexp)
            self.memoryStack.insert(lexp[0], tmp_val)
        else:
            try:
                tmp_val = func_table[node.operator](lexp, rexp)
                self.memoryStack.insert(node.lexp.id, tmp_val)
            except RuntimeWarning as e:
                print e, " in line ", node.lexp.lineno
            except TypeError as e:
                print e, " in line ", node.lexp.lineno
            
            

    @when(AST.MatrixExp)
    def visit(self, node):
        r1 = node.lexp.accept(self)
        r2 = node.rexp.accept(self)
        try:
            return func_table[node.operator](r1, r2)
        except RuntimeWarning as e:
            print e, " in line ", node.lexp.lineno
        except TypeError as e:
            print e, " in line ", node.lexp.lineno

    @when(AST.ArrayExp)
    def visit(self, node):
        tmp_tab = []
        for x in node.vector:
            tmp = x.accept(self) - 1
            tmp_tab.append(tmp)
        tmp_tuple = tuple(tmp_tab)
        tmp_val = node.id.accept(self).item(tmp_tuple)
        return (node.id.id, tmp_val)

    @when(AST.UnaryExp)
    def visit(self, node):
        if node.operator == "-":
            tmp_val = node.val.accept(self)
            return -tmp_val
        return func_table[node.operator](node.val.accept(self))

    @when(AST.RelationalExp)
    def visit(self, node):
        lexp = node.lexp.accept(self)
        rexp = node.rexp.accept(self)
        return func_table[node.relation](lexp, rexp)


    @when(AST.Zeros)
    def visit(self, node):
        tmp_vec = []
        for x in node.exp:
            tmp_val = x.accept(self)
            tmp_vec.append(tmp_val)
        if len(tmp_vec) == 1:
            tmp_vec.append(tmp_vec[0]) 
        return np.zeros(tmp_vec)

    @when(AST.Eye)
    def visit(self, node):
        tmp_vec = []
        for x in node.exp:
            tmp_val = x.accept(self)
            tmp_vec.append(tmp_val)
        if len(tmp_vec) == 1:
            tmp_vec.append(tmp_vec[0]) 
        return np.eye(tmp_vec[0])
    
    @when(AST.Ones)
    def visit(self, node):
        tmp_vec = []
        for x in node.exp:
            tmp_val = x.accept(self)
            tmp_vec.append(tmp_val)
        if len(tmp_vec) == 1:
            tmp_vec.append(tmp_vec[0]) 
        return np.ones(tmp_vec)

    @when(AST.IfStatement)
    def visit(self, node):
        memory = Memory("if")
        self.memoryStack.push(memory)
        if node.exp.accept(self):
            for s in node.stat_list:
                    tmp = s.accept(self)
        self.memoryStack.pop()

    @when(AST.IfElseStatement)
    def visit(self, node):
        memory = Memory("if")
        self.memoryStack.push(memory)
        if node.exp.accept(self):
            for s in node.stat_list:
                    tmp = s.accept(self)
            self.memoryStack.pop()
        else:
            memory = Memory("else")
            self.memoryStack.push(memory)
            if node.exp.accept(self):
                for s in node.else_stat_list:
                    tmp = s.accept(self)
            self.memoryStack.pop()

    @when(AST.ForStatement)
    def visit(self, node):
        exp = node.exp.accept(self)
        memory = Memory("for")
        self.memoryStack.push(memory)
        if isinstance(exp, list):
            try:
                for i in exp:
                    self.memoryStack.insert(node.exp.lexp.id, i)
                    for s in node.stat_list:
                        tmp = s.accept(self)
            except BreakException as e:
                    self.memoryStack.pop()
                    return 
            except ContinueException as e:
                    pass
            self.memoryStack.pop()
        else:
            while node.exp.accept(self):
                try:
                    for s in node.stat_list:
                        tmp = s.accept(self)
                except BreakException as e:
                    self.memoryStack.pop()
                    return
                except ContinueException as e:
                    pass
            self.memoryStack.pop()

    @when(AST.WhileStatement)
    def visit(self, node):
            r = None
            memory = Memory("for")
            self.memoryStack.push(memory)
            while node.condition.accept(self):
                try:
                    for s in node.stat_list:
                        tmp = s.accept(self)
                except BreakException as e:
                    self.memoryStack.pop()
                    return
                except ContinueException as e:
                    pass
            self.memoryStack.pop()
       
    @when(AST.Break)
    def visit(self, node):
        raise BreakException

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException

    @when(AST.Return)
    def visit(self, node):
        exp = node.exp.accept(self)
        raise ReturnValueException(exp)

