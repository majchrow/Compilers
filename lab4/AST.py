from typing import Union, List


class AstNode(object):
    def __init__(self, *args, **kwargs):
        self.lineno = kwargs.get('lineno', -1)


class Statement(AstNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Statements(AstNode):
    def __init__(self, statements: List[any] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statements = statements


class Expr(AstNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Matrix(AstNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Id(AstNode):
    def __init__(self, value: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value


class Variable(Expr):
    def __init__(self, value: Union[str, int, float, Matrix, Id],
                 minus: int = 0, trans: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.minus = minus
        self.trans = trans


class SpecialMatrix(Matrix):
    def __init__(self, special: str, expressions: List[Expr], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.special = special
        self.expressions = expressions


class SimpleMatrix(Matrix):
    def __init__(self, vector: List[any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vector = vector
        self.lineno = kwargs.get('lineno', 0)


class Block(AstNode):
    def __init__(self, statements: Union[Statements, Statement], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statements = statements

    def __str__(self):
        return self.statements.__str__()


class If(Statement):
    def __init__(self, cond_expr: Expr, if_block: Block, else_block: Block = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cond_expr = cond_expr
        self.if_block = if_block
        self.else_block = else_block


class While(Statement):
    def __init__(self, cond_expr: Expr, while_block: Block, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cond_expr = cond_expr
        self.while_block = while_block


class ForExpr(Expr):
    def __init__(self, for_id: Id, start_expr: Expr, end_expr: Expr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.for_id = for_id
        self.start_expr = start_expr
        self.end_expr = end_expr


class For(Statement):
    def __init__(self, iteration: ForExpr, for_block: Block, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iteration = iteration
        self.for_block = for_block


class Print(Statement):
    def __init__(self, expressions: List[Expr], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expressions = expressions


class Assignment(AstNode):
    def __init__(self, assign_id: Id, assign_op: str, expression: Expr,
                 with_ref: List[Expr] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assign_id = assign_id
        self.assign_op = assign_op
        self.expression = expression
        self.with_ref = with_ref


class Assignments(Statement):
    def __init__(self, assignments: List[Assignment], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignments = assignments


class ControlExpr(Expr):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Break(ControlExpr):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Continue(ControlExpr):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Return(ControlExpr):
    def __init__(self, expressions: List[Expr], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expressions = expressions


class BinOp(Expr):
    def __init__(self, left_expr: Expr, bin_op: str, right_expr: Expr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_expr = left_expr
        self.bin_op = bin_op
        self.right_expr = right_expr
