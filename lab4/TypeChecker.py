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

    def visit_Statements(self, node: Statements):
        for statement in node.statements:
            self.visit(statement)

    def visit_Variable(self, node: Variable):
        pass
        # Type checking here

    def visit_SpecialMatrix(self, node: SpecialMatrix):
        self.visit(node.variable)
        pass
        # Type checking here

    def visit_SimpleMatrix(self, node: SimpleMatrix):
        pass
        # Type checking here

    def visit_Block(self, node: Block):
        self.visit(node.statements)

    def visit_If(self, node: If):
        self.visit(node.cond_expr)
        self.visit(node.if_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_While(self, node: While):
        self.visit(node.cond_expr)
        self.visit(node.while_block)

    def visit_ForExpr(self, node: ForExpr):
        self.visit(node.start_var)
        self.visit(node.end_var)

    def visit_PrintExpr(self, node: PrintExpr):
        pass

    def visit_For(self, node: For):
        self.visit(node.iteration)
        self.visit(node.for_block)

    def visit_Print(self, node: Print):
        self.visit(node.print_expr)

    def visit_Assignment(self, node: Assignment):
        self.visit(node.variable)
        # Type checking here

    def visit_Break(self, node: Break):
        pass
        # Type checking here

    def visit_Continue(self, node: Continue):
        pass
        # Type checking here

    def visit_Return(self, node: Return):
        pass
        # Type checking here

    def visit_BinOp(self, node: BinOp):
        self.visit(node.left_expr)
        self.visit(node.right_expr)
        # Type checking here
