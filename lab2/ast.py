from typing import Union, Type, Tuple, List


class AstNode(object):
    pass


class Statement(AstNode):
    pass


class Statements(AstNode):
    def __init__(self, statements: List[Statement] = None):
        self.statements = statements if statements else []


class Expr(AstNode):
    pass


class Matrix(AstNode):
    pass


class Id:
    def __init__(self, value: str):
        self.value = value


class Variable(Expr):
    def __init__(self, value: Union[str, int, float, Matrix, Id],
                 var_type: Type[Union[str, int, float, Matrix, Id]],
                 minus: bool = False, trans: bool = False):
        self.value = value
        self.var_type = var_type
        self.minus = minus
        self.trans = trans


class SpecialMatrix(Matrix):
    def __init__(self, special: str, variable: Variable):
        self.special = special
        self.variable = variable


class SimpleMatrix(Matrix):
    def __init__(self, rows: List[List[Variable]]):
        self.rows = rows


class Block(AstNode):
    def __init__(self, statements: Statements):
        self.statements = statements


class If(Statement):
    def __init__(self, cond_expr: Expr, if_block: Block, else_block: Block = None):
        self.cond_expr = cond_expr
        self.if_block = if_block
        self.else_body = else_block


class While(Statement):
    def __init__(self, cond_expr: Expr, while_block: Block):
        self.cond_expr = cond_expr
        self.while_block = while_block


class ForExpr(AstNode):
    def __init__(self, for_id: str, start_var: Variable, end_var: Variable):
        self.for_id = for_id
        self.start_var = start_var
        self.end_var = end_var


class PrintExpr(AstNode):
    def __init__(self, variable: Variable):
        self.variables = [variable]


class For(Statement):
    def __init__(self, iteration: ForExpr, for_block: Block):
        self.iteration = iteration
        self.for_block = for_block


class Print(Statement):
    def __init__(self, print_expr: PrintExpr):
        self.print_expr = print_expr


class Assignment(Statement):
    def __init__(self, assign_id: str, assign_op: str, variable: Variable, with_ref: Tuple[Variable, Variable] = None):
        self.assign_id = assign_id
        self.assign_op = assign_op
        self.variable = variable
        self.with_ref = with_ref


class ControlExpr(Statement):
    pass


class Break(ControlExpr):
    pass


class Continue(ControlExpr):
    pass


class Return(ControlExpr):
    def __init__(self, variable: Variable):
        self.variables = variable


class BinOp(Expr):
    def __init__(self, left_expr: Expr, bin_op: str, right_expr: Expr):
        self.left_expr = left_expr
        self.bin_op = bin_op
        self.right_expr = right_expr
