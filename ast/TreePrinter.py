from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    
    @addToClass(AST.Id)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("id " + self.id)
        pass
    
    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("variable" + self.id)
        pass

    @addToClass(AST.Constant)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print(str(self.constant))
        pass

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("matrix")
        #print(self.vectors)
        for v in self.vectors:
            #print(v)
            v.printTree(indent + 1)
            
        pass
    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("vector")
       
        for v in self.values:
            v.printTree(indent + 1)   
        pass
        
    @addToClass(AST.ArrayExp)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("ref")
        self.id.printTree(indent + 1)
        for c in self.vector:
            c.printTree(indent + 1)
        pass        
        
    @addToClass(AST.Zeros)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("zeros")  
        self.exp.printTree(indent + 1)
        pass
        
    @addToClass(AST.Ones)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("ones")  
        self.exp.printTree(indent + 1)
        pass
        
    @addToClass(AST.Eye)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("eye")  
        self.exp.printTree(indent + 1)
        pass
        
    @addToClass(AST.Print)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("print") 
        #print(type(self.exp))
        #print(self.exp)
        #print(self.exp)
        for e in self.exp:
            #print(e)
            e.printTree(indent + 1)
        
        pass
        
    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        pass
        
    @addToClass(AST.Break)
    def printTree(self, indent=0):
        pass
    
    @addToClass(AST.Range)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("range")    
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)
        pass
        
    @addToClass(AST.Return)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("return")    
        self.exp.printTree(indent + 1)
        
        pass
    
    @addToClass(AST.AssignmentExpression)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print(self.operator)
        self.lexp.printTree(indent + 1)
        self.rexp.printTree(indent + 1)
        
        pass

    @addToClass(AST.InitExpression)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print(self.operator)
        self.lexp.printTree(indent + 1)
        self.rexp.printTree(indent + 1)
        
        pass

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("if")
        #print(self.exp)
        self.exp.printTree(indent + 1)
        for i in range(indent):
            print("| ", end ='')
        print("then")
        #print(self.exp) 
        #print(len(self.stat_list))
        for s in self.stat_list:
            #print(s)
            s.printTree(indent + 1)
        
        pass
        
    @addToClass(AST.IfElseStatement)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("if")
        #print(self.exp)
        self.exp.printTree(indent + 1)
        for i in range(indent):
            print("| ", end ='')
        print("then")
        #print(self.stat_list)   
        self.stat_list.printTree(indent + 1)
        for i in range(indent):
            print("| ", end ='')
        print("else")
        self.else_stat_list.printTree(indent + 1)
        pass
        

    @addToClass(AST.WhileStatement)
    def printTree(self, indent=0):
        print("while")
        self.condition.printTree(indent + 1)
        for s in self.stat_list:
            s.printTree(indent + 1)
        pass
        
    @addToClass(AST.ForStatement)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print("for")
        self.id.printTree(indent + 1)
        self.exp.printTree(indent + 1)
        if isinstance(self.stat_list, list):
            for s in self.stat_list:
                s.printTree(indent+1)
        else:
            self.stat_list.printTree(indent+1)
            
        pass
        
    @addToClass(AST.OperationExp)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
            
        print(self.operator)
        self.lexp.printTree(indent + 1)
        self.rexp.printTree(indent + 1)
        
        pass
        
    @addToClass(AST.MatrixExp)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print(self.operator)
        self.lexp.printTree(indent + 1)
        self.rexp.printTree(indent + 1)
        
        pass
        
    @addToClass(AST.RelationalExp)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        print(self.relation)    
        self.lexp.printTree(indent + 1)
        self.rexp.printTree(indent + 1)
        pass
        
    @addToClass(AST.Statements)
    def printTree(self, indent=0):
        
        if isinstance(self.statements, list):
            for s in self.statements:
                s.printTree(indent)
        else:
            self.statements.printTree(indent)
        
    @addToClass(AST.Statement)
    def printTree(self, indent=0):  
        #print(type(self.statement))
        if isinstance(self.statement, list):
            for s in self.statement:
                s.printTree(indent)
        else:
            self.statement.printTree(indent)
        pass
              
    @addToClass(AST.UnaryExp)
    def printTree(self, indent=0):
        for i in range(indent):
            print("| ", end ='')
        if self.operator == "'":    
            print("transopse")
        elif self.operator == "-":
            print("uminus")
        self.val.printTree(indent + 1)
        pass
    @addToClass(AST.Eostmt)
    def printTree(self, indent=0):
        pass    
        
'''
    @addToClass(AST.Error)
    def printTree(self, indent=0):
        return "|"    
        # fill in the body
'''

    # define printTree for other classes
    # ...


