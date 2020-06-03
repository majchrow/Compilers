import sys

from AST import *
from visit import *

sys.setrecursionlimit(10000)


class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass

    @when(AstNode)
    def visit(self, node: AstNode):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Statement)
    def visit(self, node: Statement):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Statements)
    def visit(self, node: Statements):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Expr)
    def visit(self, node: Expr):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Matrix)
    def visit(self, node: Matrix):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Id)
    def visit(self, node: Id):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Variable)
    def visit(self, node: Variable):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(SpecialMatrix)
    def visit(self, node: SpecialMatrix):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(SimpleMatrix)
    def visit(self, node: SimpleMatrix):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Block)
    def visit(self, node: Block):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(If)
    def visit(self, node: If):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(While)
    def visit(self, node: While):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(ForExpr)
    def visit(self, node: ForExpr):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(For)
    def visit(self, node: For):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Print)
    def visit(self, node: Print):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Assignment)
    def visit(self, node: Assignment):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Assignments)
    def visit(self, node: Assignments):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(ControlExpr)
    def visit(self, node: ControlExpr):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Break)
    def visit(self, node: Break):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Continue)
    def visit(self, node: Continue):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(Return)
    def visit(self, node: Return):
        print(f"No visitor for node {node.__class__.__name__}")

    @when(BinOp)
    def visit(self, node: BinOp):
        print(f"No visitor for node {node.__class__.__name__}")
