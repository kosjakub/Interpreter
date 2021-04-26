import VariableSymbol as vs
import AST as ast

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        # print(method)
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def __init__(self):
        self.table = vs.SymbolTable(None, "root")
        self.error = False

    def visit_Id(self, node):
        return 'string'
   
    def visit_Constant(self, node):
        if type(node.constant) is int:
            return 'int'
        else:
            return 'float'

    def visit_Variable(self, node):
        #print("ID: " + node.id)
        definition = self.table.getGlobal(node.id)
        if definition is None:
            print ("Undefined symbol {0} in line {1}".format(node.id, node.lineno))
            self.error = True
            return False
        else:
            return definition.type

    def visit_Matrix(self, node):
        vector = []
        vec_len = 0        
        vec_len = len(self.visit(node.vectors[0]))     
        for i, v in enumerate(node.vectors):
            vector.append(self.visit(v))           
            if vec_len != len(self.visit(v)):
                print("Wrong vectors size for matrix in line {}".format(node.lineno))
                self.error = True
                return False
            vec_len = len(self.visit(v))
        return (len(node.vectors), vec_len)

    def visit_Vector(self, node):
        value = []
        for i, v in enumerate(node.values):
            value.append(self.visit(v))
        return node.values
   
    def visit_ArrayExp(self, node):
        t = self.visit(node.id)
        if not t:
            return False

        if len(node.vector) != len(t):
            print("Wrong dimensions for array in line {}".format(node.lineno))
            self.error = True
            return False

        for i in range(len(node.vector)):
            if isinstance(node.vector[i], ast.Constant):
                x = node.vector[i].constant
                
            if x <= t[i]:
                continue
            else:
                print("Out of bound in line {}".format(node.lineno))
                self.error = True
                return False    
        return 'float'

    def visit_OperationExp(self, node):
        lexp = self.visit(node.lexp)
        rexp = self.visit(node.rexp)
        # print("lexp: " + str(lexp))
        # print("rexp: " + str(rexp))
        if (lexp == 'int' or lexp == 'float') and (rexp == 'int' or rexp == 'float'):
            if lexp == 'int' and rexp == 'int':
                return 'int'
            else:
                return 'float'
        elif isinstance(lexp, tuple) and isinstance(rexp, tuple):
            if node.operator == "+" or node.operator == "-":
                if lexp == rexp:
                    return lexp
                else:
                    print("Wrong matrixes sizes in line {}".format(node.lineno))
                    self.error = True
                    return False
            elif node.operator == "*":
                if lexp[1] == rexp[0]:
                    return (lexp[0], rexp[1])
                else:
                    print("Wrong matrixes sizes in line {}".format(node.lineno))
                    self.error = True
                    return False
            print ("Wrong types in line {}".format(node.lineno))
            self.error = True
            return False
        else:
            print ("Wrong types in line {}".format(node.lineno))
            self.error = True
            return False

    def visit_InitExpression(self, node):
        
        lexp = self.visit(node.lexp)     # type1 = node.left.accept(self)
        rexp = self.visit(node.rexp)
        # print("REXP: " + str(rexp))
        if not rexp:
            # print ("Error with symbol {} in line {}".format(node.lexp.id, node.lineno))
            pass
        else:
            operator = node.operator
            self.table.put(node.lexp.id, vs.VariableSymbol(node.lexp.id, rexp))

    def visit_AssignmentExpression(self, node):
        
        lexp = self.visit(node.lexp)     # type1 = node.left.accept(self) 
        rexp = self.visit(node.rexp)
        operator = node.operator
        if lexp is None:
            print ("Used undefined symbol {} in line {}".format(node.lexp, node.line))
            self.error = True
            return False
    def visit_RelationalExp(self, node):
        lexp = self.visit(node.lexp)
        rexp = self.visit(node.rexp)
        if (lexp == 'int' or lexp == 'float') and (rexp == 'int' or rexp == 'float'): 
            return True
        print("Wrong types in line {}".format(node.lineno))
        self.error = True
        return False

    def visit_MatrixExp(self, node):
        lexp = self.visit(node.lexp)
        rexp = self.visit(node.rexp)
        if (lexp == 'int' or lexp == 'float') and (isinstance(rexp, tuple)):
            return rexp
        elif (rexp == 'int' or rexp == 'float') and (isinstance(lexp, tuple)):
            return lexp
        else:
            print("Wrong types in line {}".format(node.lineno))
            self.error = True
            return False
    
    def visit_UnaryExp(self, node):
        val_type = self.visit(node.val)
        if node.operator == '-':
            if val_type == 'int' or val_type == 'float':
                return val_type
            else:
                print("Wrong types in line {}".format(node.lineno))
                self.error = True
                return False
        elif node.operator == "'":
            if isinstance(val_type, tuple):
                return (val_type[1], val_type[0])
            else:
                print("Wrong types in line {}".format(node.lineno))
                self.error = True
                return False


    def visit_ForStatement(self, node):
        self.table = self.table.pushScope(node)
        # print(self.table.name)
        exp = self.visit(node.exp)
        for s in node.stat_list:
            self.visit(s)  
        self.table = self.table.popScope()

    def visit_WhileStatement(self, node):
        self.table = self.table.pushScope(node)
        # print(self.table.name)
        exp = self.visit(node.condition)
        
        for s in node.stat_list:
            self.visit(s)  

        self.table = self.table.popScope()

    def visit_IfStatement(self, node):
        self.visit(node.exp)
        for x in node.stat_list:
            self.visit(x)

    def visit_IfElseStatement(self, node):
        pass

    def visit_Range(self, node):
        self.visit(node.start)
        self.visit(node.end)
        return 'int'

    def visit_Continue(self, node):
        if isinstance(self.table.name, (ast.ForStatement, ast.WhileStatement)):
            return True
        else:
            print("Continue not in for/while in line {}".format(node.lineno))
            self.error = True
            return False

    def visit_Break(self, node):
        if isinstance(self.table.name, (ast.ForStatement, ast.WhileStatement)):
            return True
        else:
            print("Break not in for/while in line {}".format(node.lineno))
            self.error = True
            return False

    def visit_Print(self, node):
        if isinstance(node.exp, str):
            pass
        else:
            self.visit(node.exp)

    def visit_Return(self, node):
        self.visit(node.exp)

    def visit_Zeros(self, node):
        t = []
        for i in node.exp:
            t.append(self.visit(i))
        # t = self.visit(node.exp)
        # print("t: " + str(t))
        # print("ZEROS node exp: " + str(node.exp))
        if not t[0]:
            return False
        if len(node.exp) > 2 and not t[1]:
            return False
        if len(node.exp) == 1:
            if isinstance(node.exp[0], ast.Constant):
                return (node.exp[0].constant, node.exp[0].constant)
            elif isinstance(node.exp[0], ast.Variable):
                variable = self.table.getGlobal(node.exp[0].id)
                val = variable.type
                return (val, val)
        elif len(node.exp) >= 2:
            v = []
            for i in range(len(node.exp)):
                if isinstance(node.exp[i], ast.Constant):
                    v.append(node.exp[i].constant)
                elif isinstance(node.exp[i], ast.Variable):
                    variable = self.table.getGlobal(node.exp[0].id)
                    v.append(variable.type)
            return tuple(v)
        else:
            print ("Wrong zeros init type for {} ".format(t)) 
            self.error = True
            return False

    def visit_Eye(self, node):
        t = []
        for i in node.exp:
            t.append(self.visit(i))
        # t = self.visit(node.exp)
        # print("t: " + str(t))
        # print("ZEROS node exp: " + str(node.exp))
        if not t[0]:
            return False
        if len(node.exp) > 2 and not t[1]:
            return False
        if len(node.exp) == 1:
            if isinstance(node.exp[0], ast.Constant):
                return (node.exp[0].constant, node.exp[0].constant)
            elif isinstance(node.exp[0], ast.Variable):
                variable = self.table.getGlobal(node.exp[0].id)
                val = variable.type
                return (val, val)
        elif len(node.exp) >= 2:
            v = []
            for i in range(len(node.exp)):
                if isinstance(node.exp[i], ast.Constant):
                    v.append(node.exp[i].constant)
                elif isinstance(node.exp[i], ast.Variable):
                    variable = self.table.getGlobal(node.exp[0].id)
                    v.append(variable.type)
            return tuple(v)
        else:
            print ("Wrong eye init type for {} ".format(t)) 
            self.error = True
            return False

    def visit_Ones(self, node):
        t = []
        for i in node.exp:
            t.append(self.visit(i))
        # t = self.visit(node.exp)
        # print("t: " + str(t))
        # print("ZEROS node exp: " + str(node.exp))
        if not t[0]:
            return False
        if len(node.exp) > 2 and not t[1]:
            return False
        if len(node.exp) == 1:
            if isinstance(node.exp[0], ast.Constant):
                return (node.exp[0].constant, node.exp[0].constant)
            elif isinstance(node.exp[0], ast.Variable):
                variable = self.table.getGlobal(node.exp[0].id)
                val = variable.type
                return (val, val)
        elif len(node.exp) >= 2:
            v = []
            for i in range(len(node.exp)):
                if isinstance(node.exp[i], ast.Constant):
                    v.append(node.exp[i].constant)
                elif isinstance(node.exp[i], ast.Variable):
                    variable = self.table.getGlobal(node.exp[0].id)
                    v.append(variable.type)
            return tuple(v)
        else:
            print ("Wrong ones init type for {} ".format(t)) 
            self.error = True
            return False
        
        
    