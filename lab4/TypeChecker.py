from AST import *
from SymbolTable import *


class NodeVisitor(object):

    @staticmethod
    def _get_type(var: any):
        if isinstance(var, Matrix):
            return Matrix.__name__
        try:
            return type(var).__name__
        except:
            return None

    @staticmethod
    def _get_shape(var: Matrix):
        try:
            return var.shape
        except:
            return (-1, -1)

    @staticmethod
    def _wrap_with_lineno(node: AstNode, msg: str):
        print(f"Line {node.lineno}, {msg}")

    def visit(self, node: AstNode):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: AstNode):  # Called if no explicit visitor function exists for a node.
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
            var = self.visit(node.value)
        elif isinstance(node.value, Id):
            try:
                var = self.table.get(node.value.value)
            except KeyError:
                var = None
                self._wrap_with_lineno(node, f"NameError: {node.value.value} is not defined in given scope")
        else:
            var = node.value

        if node.trans > 0 and not isinstance(var, Matrix):
            self._wrap_with_lineno(node, f"TypeError: bad operand for unary ': {self._get_type(var)}")

        if node.minus > 0 and type(var) not in {float, int}:
            self._wrap_with_lineno(node, f"TypeError: bad operand for unary -: {self._get_type(var)}")

        return var

    def visit_SpecialMatrix(self, node: SpecialMatrix):
        if len(node.expressions) != 1:
            self._wrap_with_lineno(node, f"TypeError: expected 1 argument got {len(node.expressions)}")
            return None
        var = self.visit(node.expressions[0])
        if type(var) != int:
            self._wrap_with_lineno(node, f"TypeError: bad operand for {node.special}: {self._get_type(var)}")
            return None

        if var <= 0:
            self._wrap_with_lineno(node, f"ValueError: expected non-negative argument for {node.special} "
                                         f"got: {var}")
            return None

        node.shape = (var, var)
        return node

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
            shape = len(row_sizes), row_sizes[0]
            return all(el == row_sizes[0] for el in row_sizes), shape

        vector = flatten(node.vector) if ';' not in node.vector else node.vector
        if len(vector) == len(get_indexes_of_semicolons(vector)):
            self._wrap_with_lineno(node, "TypeError: matrix rows cannot be empty")
            return None
        same_size, shape = rows_have_same_size(vector)
        if same_size:
            el_types = []
            for el in vector:
                if el == ';':
                    continue
                if isinstance(el, Id):
                    try:
                        var = self.table.get(el.value)
                        if type(var) not in {int, float}:
                            self._wrap_with_lineno(node, f"TypeError: bad operand for matrix element: "
                                                         f"{self._get_type(var)}")
                            return None
                        else:
                            el_types.append(type(var))
                    except KeyError:
                        self._wrap_with_lineno(node, f"NameError: {el.value} is not defined in given scope")
                        return None
                elif isinstance(el, list):
                    self._wrap_with_lineno(node, "TypeError: matrix element cannot be a list")
                    return None
                else:
                    if type(el) is int:
                        el_types.append(float)
                    else:
                        el_types.append(type(el))
            if not all([el_types[0] == el_type for el_type in el_types]):
                self._wrap_with_lineno(node, "TypeError: matrix elements should have the same type")
                return None
        else:
            self._wrap_with_lineno(node, "TypeError: matrix rows are not in the same size")
            return None
        node.shape = shape
        return node

    def visit_Block(self, node: Block):
        self.visit(node.statements)

    def visit_If(self, node: If):
        var = self.visit(node.cond_expr)
        if type(var) != bool:
            self._wrap_with_lineno(node, f"TypeError: boolean condition expected, got: {self._get_type(var)}")
        self.visit(node.if_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_While(self, node: While):
        scope = self.table.set_scope_name(SCOPE.LOOP)
        var = self.visit(node.cond_expr)
        if type(var) != bool:
            self._wrap_with_lineno(node, f"TypeError: boolean condition expected, got: {self._get_type(var)}")
        self.visit(node.while_block)
        self.table.set_scope_name(scope)

    def visit_ForExpr(self, node: ForExpr):
        var_start = self.visit(node.start_expr)
        var_end = self.visit(node.end_expr)
        if type(var_start) != int or type(var_end) != int:
            self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for iteration expression, got: "
                                         f"{self._get_type(var_start)} and {self._get_type(var_end)}")
            var_type = None
        else:
            var_type = int

        self.table.put(node.for_id.value, var_type)

    def visit_Return(self, node: Return):
        if len(node.expressions) != 1:
            self._wrap_with_lineno(node, f"TypeError: expected 1 argument got {len(node.expressions)}")
            return
        var = self.visit(node.expressions[0])
        if type(var) != int:
            self._wrap_with_lineno(node, f"TypeError: bad operand for return: {self._get_type(var)}")

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
        var = self.visit(node.expression)
        if node.with_ref:
            try:
                var_id = self.table.get(node.assign_id.value)
            except:
                var_id = None
                self._wrap_with_lineno(node, f"NameError: {node.assign_id.value} is not defined in given scope")
            if node.assign_op != "=":
                self._wrap_with_lineno(node, f"TypeError: unsupported operator reference assignment: {node.assign_op}")
            elif type(var) not in {int, float}:
                self._wrap_with_lineno(node, f"TypeError: cannot assign variable with type {self._get_type(var)}")
            if len(node.with_ref) != 2:
                self._wrap_with_lineno(node, f"TypeError: expected 2 arguments for reference assignment,"
                                             f" got: {len(node.with_ref)}")
            else:
                ref1 = self.visit(node.with_ref[0])
                ref2 = self.visit(node.with_ref[1])
                if type(ref1) != int:
                    self._wrap_with_lineno(node, f"TypeError: wrong type for reference, got: {self._get_type(ref1)}")

                if type(ref2) != int:
                    self._wrap_with_lineno(node, f"TypeError: wrong type for reference, got: {self._get_type(ref2)}")

                if type(ref1) == int and type(ref2) == int and isinstance(var_id, Matrix):
                    if var_id.shape[0] <= ref1 or var_id.shape[1] <= ref2:
                        self._wrap_with_lineno(node, f"IndexError: matrix indexes out of range "
                                                     f"{self._get_type(ref1)}, {self._get_type(ref2)}")

            if not isinstance(var_id, Matrix):
                self._wrap_with_lineno(node,
                                       f"TypeError: reference only possible for Matrix, got: {self._get_type(var_id)}")

        else:
            if node.assign_op == "=":
                self.table.put(node.assign_id.value, var)
            elif node.assign_op in ops:
                try:
                    var_id = self.table.get(node.assign_id.value)
                except:
                    var_id = None
                    self._wrap_with_lineno(node, f"NameError: {node.assign_id.value} is not defined in given scope")

                if type(var) not in {int, float} and not isinstance(var, Matrix):
                    self._wrap_with_lineno(node,
                                           f"TypeError: Unsupported operand type for "
                                           f"{node.assign_op}: {self._get_type(var)}")
                if type(var_id) != type(var_id) and isinstance(var_id, Matrix) or isinstance(var, Matrix):
                    self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.assign_op}:"
                                                 f" {self._get_type(var_id)} and {self._get_type(var)}")
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
        left_var = self.visit(node.left_expr)
        right_var = self.visit(node.right_expr)

        if node.bin_op in number_ops:
            if type(left_var) not in {int, float} or type(right_var) not in {int, float}:
                self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.bin_op}, got: "
                                             f"{self._get_type(left_var)} and {self._get_type(right_var)}")
                return None
            if node.bin_op == '+':  # Evaluating needed for shape checking in case of 'eye(2+2) .+ eye(3-1)' etc.
                var_type = left_var + right_var
            elif node.bin_op == '-':
                var_type = left_var - right_var
            elif node.bin_op == '*':
                var_type = left_var * right_var
            else:
                if right_var == 0:
                    self._wrap_with_lineno(node, f"ZeroDivisionError: division by zero : "
                                                 f"{self._get_type(left_var)} / {self._get_type(right_var)}")
                    return None
                var_type = left_var / right_var
        elif node.bin_op in boolean_ops:
            if (type(left_var) not in {int, float} and type(right_var) not in {int, float}) \
                    or type(left_var) != type(right_var):
                self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.bin_op}, got: "
                                             f"{self._get_type(left_var)} and {self._get_type(right_var)}")
                return None
            return True  # Evaluation not needed for type_checking

        elif node.bin_op in matrix_ops:
            if not isinstance(left_var, Matrix) or not isinstance(right_var, Matrix):
                self._wrap_with_lineno(node, f"TypeError: Unsupported operand types for {node.bin_op}, got: "
                                             f"{self._get_type(left_var)} and {self._get_type(right_var)}")
                return None
            if left_var.shape != right_var.shape:
                self._wrap_with_lineno(node, f"TypeError: Unsupported operand matrix shapes for {node.bin_op}, got: "
                                             f"{self._get_shape(left_var)} and {self._get_shape(right_var)}")
            var_type = left_var  # Evaluation not needed for type_checking
        else:
            var_type = None

        return var_type
