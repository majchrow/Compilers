from AST import *


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            print("NO GENERIC VISITOR FOR GIVEN NODE")
        # else:
        #     for child in node.children:
        #         if isinstance(child, list):
        #             for item in child:
        #                 if isinstance(item, AstNode):
        #                     self.visit(item)
        #         elif isinstance(child, AstNode):
        #             self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_AstNode(self, node: AstNode):
        pass

    def visit_Statement(self, node: Statement):
        pass

    def visit_Statements(self, node: Statements):
        pass

    def visit_Expr(self, node: Expr):
        pass

    def visit_Matrix(self, node: Matrix):
        pass

    def visit_Id(self, node: Id):
        pass

    def visit_Variable(self, node: Variable):
        pass

    def visit_SpecialMatrix(self, node: SpecialMatrix):
        pass

    def visit_SimpleMatrix(self, node: SimpleMatrix):
        pass

    def visit_Block(self, node: Block):
        pass

    def visit_If(self, node: If):
        pass

    def visit_While(self, node: While):
        pass

    def visit_ForExpr(self, node: ForExpr):
        pass

    def visit_PrintExpr(self, node: PrintExpr):
        pass

    def visit_For(self, node: For):
        pass

    def visit_Print(self, node: Print):
        pass

    def visit_Assignment(self, node: Assignment):
        pass

    def visit_ControlExpr(self, node: ControlExpr):
        pass

    def visit_Break(self, node: Break):
        pass

    def visit_Continue(self, node: Continue):
        pass

    def visit_Return(self, node: Return):
        pass

    def visit_BinOp(self, node: BinOp):
        pass
