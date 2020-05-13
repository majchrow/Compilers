from AST import *
from SymbolTable import *


class NodeVisitor(object):

    @staticmethod
    def _get_type(var):
        try:
            return var.__name__
        except:
            return None

    @staticmethod
    def _wrap_with_lineno(node, msg):
        print(f"Line {node.lineno}, {msg}")

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        print("No visitor for node ", node.__class__.__name__)
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            children = getattr(node, 'children', [])
            for child in children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AstNode):
                            self.visit(item)
                elif isinstance(child, AstNode):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.table = SymbolTable()

    def visit_Statements(self, node: Statements):
        for statement in node.statements:
            if isinstance(statement, Statements):  # if we are in new { } push new scope
                scope = self.table.set_scope_name(SCOPE.LOCAL)
                self.table.push_scope()
                self.visit(statement)
                self.table.pop_scope()
                self.table.set_scope_name(scope)
            else:
                self.visit(statement)

    def visit_Variable(self, node: Variable):
        if isinstance(node.value, Matrix):
            var_type = self.visit(node.value)
        elif isinstance(node.value, Id):
            try:
                var_type = self.table.get(node.value.value)
            except KeyError:
                var_type = None
                self._wrap_with_lineno(node, f"NameError: {node.value.value} is not defined in given scope")
        else:
            var_type = type(node.value)

        if node.trans > 0 and var_type != Matrix:
            self._wrap_with_lineno(node, f"TypeError: bad operand for unary ': {self._get_type(var_type)}")

        if node.minus > 0 and var_type not in {float, int}:
            self._wrap_with_lineno(node, f"TypeError: bad operand for unary -: {self._get_type(var_type)}")

        return var_type

    def visit_SpecialMatrix(self, node: SpecialMatrix):
        if len(node.expressions) != 1:
            self._wrap_with_lineno(node, f"TypeError: expected 1 argument got {len(node.expressions)}")
            return None
        var_type = self.visit(node.expressions[0])
        if var_type != int:
            self._wrap_with_lineno(node, f"TypeError: bad operand for {node.special}: {self._get_type(var_type)}")
            return None
        return Matrix

    def visit_Assignments(self, node: Assignments):
        for assignment in node.assignments:  # One or multiple assignments separated by commas are allowed
            self.visit(assignment)

    def visit_SimpleMatrix(self, node: SimpleMatrix):
        def flatten(matrix):
            new_matrix = []
            last = len(matrix) - 1

            for i, vector in enumerate(matrix):
                if not isinstance(vector, list):
                    new_matrix.append(vector)
                else:
                    for el in vector:
                        new_matrix.append(el)
                if i != last:
                    new_matrix.append(';')

            return new_matrix

        def get_indexes_of_semicolons(vector):
            return [i for i, el in enumerate(vector) if el == ';']

        def rows_have_same_size(vector):
            semicolons = get_indexes_of_semicolons(vector)
            semicolons = semicolons + [len(vector)]
            tmp = [0] + list(map(lambda x: x + 1, semicolons[:-1]))
            row_sizes = [i - j for i, j in zip(semicolons, tmp)]
            return all(el == row_sizes[0] for el in row_sizes)

        vector = flatten(node.vector) if ';' not in node.vector else node.vector
        if (len(vector) == len(get_indexes_of_semicolons(vector))):
            self._wrap_with_lineno(node, "TypeError: matrix rows cannot be empty")
            return None
        if rows_have_same_size(vector):
            for el in vector:
                if el == ';':
                    continue
                if isinstance(el, Id):
                    try:
                        var_type = self.table.get(el.value)
                        if var_type not in {int, float}:
                            self._wrap_with_lineno(node,
                                                   f"TypeError: bad operand for matrix element: {self._get_type(var_type)}")
                            return None
                    except KeyError:
                        self._wrap_with_lineno(node, f"NameError: {el.value} is not defined in given scope")
                        return None
                if isinstance(el, list):
                    self._wrap_with_lineno(node, "TypeError: matrix element cannot be a list")
                    return None
        else:
            self._wrap_with_lineno(node, "TypeError: matrix rows are not in the same size")
            return None
        return Matrix

    def visit_Block(self, node: Block):
        self.visit(node.statements)

    def visit_If(self, node: If):
        var_type = self.visit(node.cond_expr)
        if var_type != bool:
            self._wrap_with_lineno(node, f"TypeError: boolean condition expected, got: {self._get_type(var_type)}")
        self.visit(node.if_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_While(self, node: While):
        scope = self.table.set_scope_name(SCOPE.LOOP)
        var_type = self.visit(node.cond_expr)
        if var_type != bool:
            self._wrap_with_lineno(node, f"TypeError: boolean condition expected, got: {self._get_type(var_type)}")
        self.visit(node.while_block)
        self.table.set_scope_name(scope)

    def visit_ForExpr(self, node: ForExpr):
        scope = self.table.set_scope_name(SCOPE.LOOP)
        var_start_type = self.visit(node.start_expr)
        var_end_type = self.visit(node.end_expr)
        if var_start_type != int and var_end_type != int:
            self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for iteration expression, got: "
                                         f"{self._get_type(var_start_type)} and {self._get_type(var_end_type)}")
            var_type = None
        else:
            var_type = int

        self.table.put(node.for_id.value, var_type)
        self.table.set_scope_name(scope)

    def visit_Return(self, node: Return):
        if len(node.expressions) != 1:
            self._wrap_with_lineno(node, f"TypeError: expected 1 argument got {len(node.expressions)}")
            return
        var_type = self.visit(node.expressions[0])
        if var_type != int:
            self._wrap_with_lineno(node, f"TypeError: bad operand for return: {self._get_type(var_type)}")

    def visit_For(self, node: For):
        self.table.push_scope()  # push scope in case of shadowing variable there
        self.visit(node.iteration)
        scope = self.table.set_scope_name(SCOPE.LOOP)
        self.visit(node.for_block)
        self.table.set_scope_name(scope)
        self.table.pop_scope()

    def visit_Print(self, node: Print):
        if len(node.expressions) == 0:
            self._wrap_with_lineno(node, f"TypeError: expected at least 1 argument for statement")
        for expr in node.expressions:
            self.visit(expr)

    def visit_Assignment(self, node: Assignment):
        ops = {'+=', '-=', '/=', '*='}
        var_type = self.visit(node.expression)
        if node.with_ref:
            try:
                var_id = self.table.get(node.assign_id.value)
            except:
                var_id = None
                self._wrap_with_lineno(node, f"NameError: {node.assign_id.value} is not defined in given scope")
            if node.assign_op != "=":
                self._wrap_with_lineno(node, f"TypeError: unsupported operator reference assignment: {node.assign_op}")
            if len(node.with_ref) != 2:
                self._wrap_with_lineno(node,
                                       f"TypeError: expected 2 arguments for reference assignment, got: {len(node.with_ref)}")
            if var_id != Matrix:
                self._wrap_with_lineno(node,
                                       f"TypeError: reference only possible for Matrix, got: {self._get_type(var_id)}")
            if var_type == Matrix:
                self._wrap_with_lineno(node, f"TypeError: cannot assign Matrix with reference assignment")
            for refs in node.with_ref:
                ref_type = self.visit(refs)
                if ref_type not in {int, float}:
                    self._wrap_with_lineno(node,
                                           f"TypeError: wrong type for reference, got: {self._get_type(ref_type)}")
        else:
            if node.assign_op == "=":
                self.table.put(node.assign_id.value, var_type)
            elif node.assign_op in ops:
                try:
                    var_id = self.table.get(node.assign_id.value)
                except:
                    var_id = None
                    self._wrap_with_lineno(node, f"NameError: {node.assign_id.value} is not defined in given scope")

                if var_type not in {int, float, Matrix}:
                    self._wrap_with_lineno(node,
                                           f"TypeError: Unsupported operand type for {node.assign_op}: {self._get_type(var_type)}")
                if var_id != var_id and var_id == Matrix or var_type == Matrix:
                    self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.assign_op}:"
                                                 f" {self._get_type(var_id)} and {self._get_type(var_type)}")
            else:  # this code should be unreachable
                self._wrap_with_lineno(node, f"SyntaxError: Unsupported operator {node.assign_op}")

    def visit_Break(self, node: Break):
        if self.table.current_scope_name != SCOPE.LOOP:
            self._wrap_with_lineno(node, "SyntaxError: 'break' outside loop")

    def visit_Continue(self, node: Continue):
        if self.table.current_scope_name != SCOPE.LOOP:
            self._wrap_with_lineno(node, "SyntaxError: 'continue' outside loop")

    def visit_BinOp(self, node: BinOp):
        number_ops = {'+', '-', '/', '*'}
        matrix_ops = {'.+', '.-', './', '.*'}
        boolean_ops = {'<', '>', '<=', '>=', '==', '!='}
        left_var_type = self.visit(node.left_expr)
        right_var_type = self.visit(node.right_expr)

        if node.bin_op in number_ops:
            if left_var_type not in {int, float} or right_var_type not in {int, float}:
                self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.bin_op}, got: "
                                             f"{self._get_type(left_var_type)} and {self._get_type(right_var_type)}")
                return None
            var_type = left_var_type and right_var_type  # int and float = float
        elif node.bin_op in boolean_ops:
            if (left_var_type not in {int, float} and right_var_type not in {int, float}) \
                    or left_var_type != right_var_type:
                self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.bin_op}, got: "
                                             f"{self._get_type(left_var_type)} and {self._get_type(right_var_type)}")
                return None
            var_type = bool
        elif node.bin_op in matrix_ops:
            if left_var_type != Matrix or right_var_type != Matrix:
                self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.bin_op}, got: "
                                             f"{self._get_type(left_var_type)} and {self._get_type(right_var_type)}")
                return None
            var_type = Matrix
        else:
            var_type = None

        return var_type
