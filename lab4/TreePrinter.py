from __future__ import print_function

from AST import *


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def printWithIndent(value, indent_num):
    print("|  " * indent_num + str(value))


class TreePrinter:

    @addToClass(AstNode)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(If)
    def printTree(self, indent=0):
        printWithIndent("IF", indent)
        self.cond_expr.printTree(indent + 1)
        printWithIndent("THEN", indent)
        self.if_block.printTree(indent + 1)
        if self.else_block:
            printWithIndent("ELSE", indent)
            self.else_block.printTree(indent + 1)

    @addToClass(While)
    def printTree(self, indent=0):
        printWithIndent("WHILE", indent)
        self.cond_expr.printTree(indent + 1)
        self.while_block.printTree(indent + 1)

    @addToClass(For)
    def printTree(self, indent=0):
        printWithIndent("FOR", indent)
        self.iteration.printTree(indent + 1)
        self.for_block.printTree(indent + 1)

    @addToClass(Print)
    def printTree(self, indent=0):
        printWithIndent("PRINT", indent)
        self.print_expr.printTree(indent + 1)

    @addToClass(Assignment)
    def printTree(self, indent=0):
        printWithIndent(self.assign_op, indent)
        if self.with_ref:
            printWithIndent("REF", indent + 1)
            printWithIndent(self.assign_id, indent + 2)
            self.with_ref[0].printTree(indent + 2)
            self.with_ref[1].printTree(indent + 2)
        else:
            printWithIndent(self.assign_id, indent + 1)
        self.variable.printTree(indent + 1)

    @addToClass(Break)
    def printTree(self, indent=0):
        printWithIndent("BREAK", indent)

    @addToClass(Continue)
    def printTree(self, indent=0):
        printWithIndent("CONTINUE", indent)

    @addToClass(Return)
    def printTree(self, indent=0):
        printWithIndent("RETURN", indent)
        self.variable.printTree(indent + 1)

    @addToClass(Statements)
    def printTree(self, indent=0):
        for statement in self.statements:
            statement.printTree(indent)

    @addToClass(Variable)
    def printTree(self, indent=0):
        if self.minus:
            printWithIndent("MINUS", indent)
            indent += 1
        if self.trans:
            printWithIndent("TRANSPOSE", indent)
            indent += 1
        try:  # for example X = -ones(3)'
            self.value.printTree(indent + 1)
        except AttributeError:
            printWithIndent(self.value, indent)

    @addToClass(BinOp)
    def printTree(self, indent=0):
        printWithIndent(self.bin_op, indent)
        self.left_expr.printTree(indent + 1)
        self.right_expr.printTree(indent + 1)

    @addToClass(SpecialMatrix)
    def printTree(self, indent=0):
        printWithIndent(self.special, indent)
        self.variable.printTree(indent + 1)

    @addToClass(SimpleMatrix)
    def printTree(self, indent=0):
        def print_vector(vector, indent):
            printWithIndent("VECTOR", indent)
            indent += 1
            for elem in vector:
                if (type(elem) is list):
                    print_vector(elem, indent)
                elif elem == ';':
                    printWithIndent("SEMICOL", indent)
                else:
                    elem.printTree(indent)

        vec = self.vector
        print_vector(vec, indent)

    @addToClass(Id)
    def printTree(self, indent=0):
        printWithIndent(self.value, indent - 1)

    @addToClass(Block)
    def printTree(self, indent=0):
        for statement in self.statements:
            statement.printTree(indent)

    @addToClass(ForExpr)
    def printTree(self, indent=0):
        printWithIndent(self.for_id, indent)
        printWithIndent("RANGE", indent)
        self.start_var.printTree(indent + 1)
        self.end_var.printTree(indent + 1)
