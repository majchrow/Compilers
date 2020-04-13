from __future__ import print_function
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class TreePrinter:

    @staticmethod
    def printWithIndent(value, indent_num):
        print("| " * indent_num + value)

    @addToClass(AST.AstNode)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        printWithIndent("IF", indent)
        self.cond_expr.printTree(indent+1)
        printWithIndent("THEN", indent)
        self.if_block.printTree(indent+1)
        if self.else_block:
            printWithIndent("ELSE", indent)
            self.else_block.printTree(indent+1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        printWithIndent("WHILE", indent)
        self.cond_expr.printTree(indent+1)
        self.while_block.printTree(indent+1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        printWithIndent("FOR", indent)
        self.iteration.printTree(indent+1)
        self.for_block.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):    
        printWithIndent("PRINT", indent)
        self.print_expr.printTree(indent+1)


    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        printWithIndent(self.assign_op, indent)
        if self.with_ref:
            printWithIndent("REF", indent+1)
            printWithIndent(self.assign_id, indent+2)
            printWithIndent(self.with_ref[0], indent+2)
            printWithIndent(self.with_ref[1], indent+2)
        else:    
            printWithIndent(self.assign_id, indent+1)
        self.variable.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        printWithIndent("BREAK", indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        printWithIndent("CONTINUE", indent)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        printWithIndent("RETURN", indent)
        self.variable.printTree(indent+1)

    @addToClass(AST.Statements)
    def printTree(self, indent=0):
        for statement in self.statements:
            statement.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        printWithIndent(self.value, indent)
        if self.minus:
            printWithIndent("MINUS", indent)
        if self.trans:
            printWithIndent("TRANSPOSE", indent)

    @addToClass(AST.BinOp)
    def printTree(self, indent=0):
        printWithIndent(self.bin_op, indent)
        self.left_expr.printTree(indent+1)
        self.right_expr.printTree(indent+1)
    
    @addToClass(AST.SpecialMatrix)
    def printTree(self, indent=0):
        printWithIndent(self.special, indent)
        self.variable.printTree(indent+1)

    @addToClass(AST.SimpleMatrix)
    def printTree(self, indent=0):
        printWithIndent("VECTOR", indent)
        for row in self.rows:
            printWithIndent("VECTOR", indent+1)
            for var in row:
                var.printTree(indent+2)

    # @addToClass(AST.Id)
    # def printTree(self, indent=0):
    #     printWithIndent("ID", indent)
    #     printWithIndent(self.value, indent+1)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        for statement in self.statements:
            statement.printTree(indent)
    
    @addToClass(AST.ForExpr)
    def printTree(self, indent=0):
        printWithIndent(self.for_id, indent)
        printWithIndent("RANGE", indent)
        printWithIndent(self.start_var, indent+1)
        printWithIndent(self.end_var, indent+1)

    @addToClass(AST.PrintExpr)
    def printTree(self, indent=0):
        for var in self.variables:
            var.printTree(indent)


if __name__ == "__name__":
    println("here")
    tp = TreePrinter()