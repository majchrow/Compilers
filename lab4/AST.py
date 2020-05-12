from typing import Union, Tuple, List


class AstNode(object):
    pass


class Statement(AstNode):
    pass


class Statements(AstNode):
    def __init__(self, statements: List[any] = None):
        self.statements = statements


class Expr(AstNode):
    pass


class Matrix(AstNode):
    pass


class Id:
    def __init__(self, value: str):
        self.value = value


class Variable(Expr):
    def __init__(self, value: Union[str, int, float, Matrix, Id],
                 minus: bool = False, trans: bool = False):
        self.value = value
        self.minus = minus
        self.trans = trans


class SpecialMatrix(Matrix):
    def __init__(self, special: str, variable: Variable):
        super().__init__()
        self.special = special
        self.variable = variable


class SimpleMatrix(Matrix):
    def __init__(self, vector: List[any]):
        super().__init__()
        self.vector = vector


class Block(AstNode):
    def __init__(self, statements: Union[Statements, Statement]):
        self.statements = statements

    def __str__(self):
        return self.statements.__str__()


class If(Statement):
    def __init__(self, cond_expr: Expr, if_block: Block, else_block: Block = None):
        self.cond_expr = cond_expr
        self.if_block = if_block
        self.else_block = else_block


class While(Statement):
    def __init__(self, cond_expr: Expr, while_block: Block):
        self.cond_expr = cond_expr
        self.while_block = while_block


class ForExpr(Expr):
    def __init__(self, for_id: Id, start_var: Variable, end_var: Variable):
        self.for_id = for_id
        self.start_var = start_var
        self.end_var = end_var


class PrintExpr(Expr):
    def __init__(self, expressions: List[Expr]):
        self.expressions = expressions


# class ControlExpr(Expr):
#     def __init__(self, variable: List[Variable]):
#         self.variables = variable
#
#     def __str__(self):
#         variables = "\n".join([var.__str__() for var in self.variables])
#         return f"PrintExpr((variables, {variables}))"


class For(Statement):
    def __init__(self, iteration: ForExpr, for_block: Block):
        self.iteration = iteration
        self.for_block = for_block


class Print(Statement):
    def __init__(self, print_expr: PrintExpr):
        self.print_expr = print_expr


class Assignment(Statement):
    def __init__(self, assign_id: Id, assign_op: str, variable: Variable, with_ref: Tuple[Variable, Variable] = None):
        self.assign_id = assign_id
        self.assign_op = assign_op
        self.variable = variable
        self.with_ref = with_ref


class ControlExpr(Expr):
    pass


class Break(ControlExpr):
    pass


class Continue(ControlExpr):
    pass


class Return(ControlExpr):
    def __init__(self, expresion: Expr):
        self.expresion = expresion

    def __str__(self):
        return f"Return((variable, {self.expresion}))"


class BinOp(Expr):
    def __init__(self, left_expr: Expr, bin_op: str, right_expr: Expr):
        self.left_expr = left_expr
        self.bin_op = bin_op
        self.right_expr = right_expr

    def __str__(self):
        return f"BinOp((left_expr, {self.left_expr}), " \
               f"(bin_op, {self.bin_op}), " \
               f"(right_expr, {self.right_expr}))"
