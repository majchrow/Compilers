from AST import *
from SymbolTable import *


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        print("FAILED")
        print(node.__class__.__name__)
        # if isinstance(node, list):
        #     for elem in node:
        #         self.visit(elem)
        # else:
        # else:
        #     for child in node.children:
        #         if isinstance(child, list):
        #             for item in child:
        #                 if isinstance(item, AstNode):
        #                     self.visit(item)
        #         elif isinstance(child, AstNode):
        #             self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.table = SymbolTable()

    @staticmethod
    def flatten(matrix):
        new_matrix = []
        last = len(matrix)-1
        
        for i,vector in enumerate(matrix):
            if not isinstance(vector, list):
                new_matrix.append(vector)
            else:
                for el in vector:
                    new_matrix.append(el)
            if i != last:    
                new_matrix.append(';')
        
        return new_matrix

    @staticmethod
    def rows_have_same_size(vector):
        semicolons = [i for i, el in enumerate(vector) if el == ';']
        semicolons = semicolons + [len(vector)]
        tmp = [0] + list(map(lambda x: x+1, semicolons[:-1]))
        row_sizes = [i - j for i, j in zip(semicolons, tmp)]
        return all(el == row_sizes[0] for el in row_sizes)

    def visit_Statements(self, node: Statements):
        for statement in node.statements:
            if isinstance(statement, Statements):
                scope = self.table.set_scope_name(SCOPE.LOCAL)
                self.table.push_scope()
                self.visit(statement)
                self.table.pop_scope()
                self.table.set_scope_name(scope)
            else:
                self.visit(statement)

    def visit_Variable(self, node: Variable):
        if isinstance(node.value, Matrix):
            self.visit(node.value)
            var_type = type(Matrix)
        elif isinstance(node.value, Id):
            try:
                var_type = self.table.get(node.value.value)
            except KeyError:
                var_type = None
                print("id not defined in given scope")
        else:
            if node.trans:
                print("Transpose error")
            var_type = type(node.value)

        if isinstance(node.value, str) and node.minus:
            print("minus")

        return var_type

    def visit_SpecialMatrix(self, node: SpecialMatrix):
        if len(node.expressions) != 1:
            print("1 argument expected")
            return
        var_type = self.visit(node.expressions[0])
        if var_type != int:
            print("Expected int")

    def visit_Assignments(self, node: Assignments):
        for assignment in node.assignments:
            self.visit(assignment)

    def visit_SimpleMatrix(self, node: SimpleMatrix):
        vector = self.flatten(node.vector) if ';' not in node.vector else node.vector 
        if self.rows_have_same_size(vector):
            for el in vector:
                if el == ';':
                    continue
                if isinstance(el, Id):
                    try:
                        symbol = self.table.get(el.value)
                        if symbol.sym_type not in (int, float):
                            print("TypeError")
                    except KeyError:
                        print("id not defined in given scope")
                if isinstance(el, list):
                    print("TypeError")
        else:
            print("Rows have different sizes")

    def visit_Block(self, node: Block):
        self.visit(node.statements)  # just propagate, scope will if block is within scope it will be done by Statements

    def visit_If(self, node: If):
        self.visit(node.cond_expr)
        self.visit(node.if_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_While(self, node: While):
        scope = self.table.set_scope_name(SCOPE.LOOP)
        self.visit(node.cond_expr)
        self.visit(node.while_block)
        self.table.set_scope_name(scope)

    def visit_ForExpr(self, node: ForExpr):
        scope = self.table.set_scope_name(SCOPE.LOOP)
        self.visit(node.start_expr)
        self.visit(node.end_expr)
        self.table.set_scope_name(scope)

    def visit_Return(self, node: Return):
        if len(node.expressions) != 1:
            print("1 argument expected")
            return
        var_type = self.visit(node.expressions[0])
        if var_type != int:
            print("Returning ", var_type, " forbidden")

    def visit_For(self, node: For):
        self.visit(node.iteration)
        self.visit(node.for_block)

    def visit_Print(self, node: Print):
        for expr in node.expressions:
            self.visit(expr)

    def visit_Assignment(self, node: Assignment):
        var_type = self.visit(node.expression)
        self.table.put(node.assign_id.value, var_type)

    def visit_Break(self, node: Break):
        if self.table.current_scope_name != SCOPE.LOOP:
            print("Forbidden scope break")

    def visit_Continue(self, node: Continue):
        if self.table.current_scope_name != SCOPE.LOOP:
            print("Forbidden scope continue")

    def visit_BinOp(self, node: BinOp):
        left_var_type = self.visit(node.left_expr)
        right_var_type = self.visit(node.right_expr)
        if left_var_type != right_var_type:
            print(left_var_type, "!=", right_var_type)
            return None
        return left_var_type
