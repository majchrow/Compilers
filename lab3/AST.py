from typing import Union, Type, Tuple, List


class AstNode(object):
    pass


class Statement(AstNode):
    pass


class Statements(AstNode):
    def __init__(self, statements: List[Statement] = None):
        self.statements = statements if statements else []

    def __str__(self):
        return "\n".join([statement.__str__() for statement in self.statements])


class Expr(AstNode):
    pass


class Matrix(AstNode):
    pass


class Id:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class Variable(Expr):
    def __init__(self, value: Union[str, int, float, Matrix, Id],
                 var_type: Type[Union[str, int, float, Matrix, Id]],
                 minus: bool = False, trans: bool = False):
        self.value = value
        self.var_type = var_type
        self.minus = minus
        self.trans = trans

    def __str__(self):
        return f"Variable((value, {self.value}), " \
               f"(type, {self.var_type}), " \
               f"(minus, {self.minus}), " \
               f"(transposition, {self.trans}))"


class SpecialMatrix(Matrix):
    def __init__(self, special: str, variable: Variable):
        self.special = special
        self.variable = variable

    def __str__(self):
        return f"SpecialMatrix((special, {self.special}), " \
               f"(variable, {self.variable}))"


class SimpleMatrix(Matrix):
    def __init__(self, vector: List[any]):
        self.vector = vector

class Block(AstNode):
    def __init__(self, statements: Statements):
        self.statements = statements

    def __str__(self):
        return self.statements.__str__()


class If(Statement):
    def __init__(self, cond_expr: Expr, if_block: Block, else_block: Block = None):
        self.cond_expr = cond_expr
        self.if_block = if_block
        self.else_block = else_block

    def __str__(self):
        else_body = f", (else_block, ({self.else_block})" if self.else_block else ""
        return f"If((cond_expr, {self.cond_expr}), " \
               f"(if_block, {self.if_block}){else_body})"


class While(Statement):
    def __init__(self, cond_expr: Expr, while_block: Block):
        self.cond_expr = cond_expr
        self.while_block = while_block

    def __str__(self):
        return f"While((cond_expr, {self.cond_expr}), " \
               f"(while_block, {self.while_block})) "


class ForExpr(AstNode):
    def __init__(self, for_id: str, start_var: Variable, end_var: Variable):
        self.for_id = for_id
        self.start_var = start_var
        self.end_var = end_var

    def __str__(self):
        return f"ForExpr((for_id, {self.for_id}), " \
               f"(start_var, {self.start_var}), " \
               f"(end_var, {self.end_var}))"


class PrintExpr(AstNode):
    def __init__(self, variable: Variable):
        self.variables = [variable]

    def __str__(self):
        variables = "\n".join([var.__str__() for var in self.variables])
        return f"PrintExpr((variables, {variables}))"


class For(Statement):
    def __init__(self, iteration: ForExpr, for_block: Block):
        self.iteration = iteration
        self.for_block = for_block

    def __str__(self):
        return f"For((ForExpr, {self.iteration}), " \
               f"(for_block, {self.for_block}))"


class Print(Statement):
    def __init__(self, print_expr: PrintExpr):
        self.print_expr = print_expr

    def __str__(self):
        return f"Print((print_expr, {self.print_expr}))"


class Assignment(Statement):
    def __init__(self, assign_id: str, assign_op: str, variable: Variable, with_ref: Tuple[Variable, Variable] = None):
        self.assign_id = assign_id
        self.assign_op = assign_op
        self.variable = variable
        self.with_ref = with_ref

    def __str__(self):
        ref = f", (with_ref, ({self.with_ref[0]}, {self.with_ref[1]}))" if self.with_ref else ""
        return f"Assignment((assign_id, {self.assign_id}), " \
               f"(assign_op, {self.assign_op}), " \
               f"(variable, {self.variable})" \
               f"{ref})"


class ControlExpr(Statement):
    pass


class Break(ControlExpr):

    def __str__(self):
        return "Break()"


class Continue(ControlExpr):

    def __str__(self):
        return "Continue()"


class Return(ControlExpr):
    def __init__(self, variable: Variable):
        self.variable = variable

    def __str__(self):
        return f"Return((variable, {self.variable}))"


class BinOp(Expr):
    def __init__(self, left_expr: Expr, bin_op: str, right_expr: Expr):
        self.left_expr = left_expr
        self.bin_op = bin_op
        self.right_expr = right_expr

    def __str__(self):
        return f"BinOp((left_expr, {self.left_expr}), " \
               f"(bin_op, {self.bin_op}), " \
               f"(right_expr, {self.right_expr}))"
