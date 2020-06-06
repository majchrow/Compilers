import operator
import sys

import numpy as np

from AST import *
from Exceptions import *
from Memory import MemoryStack
from visit import *

sys.setrecursionlimit(10000)


class Interpreter(object):
    _ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">+": operator.ge,
        "==": operator.eq,
        "!=": operator.ne,
        ".+": operator.add,
        ".-": operator.sub,
        ".*": operator.mul,
        "./": operator.truediv,
        "+=": operator.add,
        "-=": operator.sub,
        "*=": operator.mul,
        "/=": operator.truediv
    }

    def __init__(self):
        self.memory = MemoryStack()

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
        for statement in node.statements:
            if isinstance(statement, Statements):
                print("Pushing")
                self.memory.push()
                statement.accept(self)
                self.memory.pop()
            else:
                statement.accept(self)

    @when(Expr)
    def visit(self, node: Expr):
        return node.accept(self)

    @when(Id)
    def visit(self, node: Id):
        return self.memory.get(node.value)

    @when(Variable)
    def visit(self, node: Variable):
        if isinstance(node.value, Id):
            value = node.value.accept(self)
        elif isinstance(node.value, Matrix):
            matrix = node.value.accept(self)
            return matrix if node.trans % 2 == 0 else np.transpose(matrix)
        else:
            value = node.value
        return value if node.minus % 2 == 0 else -value

    @when(Matrix)
    def visit(self, node: Matrix):
        return node.accept(self)

    @when(SpecialMatrix)
    def visit(self, node: SpecialMatrix):
        value = node.expressions[0].accept(self)
        if node.special == "eye":
            return np.eye(value)
        elif node.special == "zeros":
            return np.zeros((value, value))
        else:  # ones
            return np.ones((value, value))

    @when(SimpleMatrix)
    def visit(self, node: SimpleMatrix):
        def _create_matrix(vector: List[any]):
            outer = []
            inner = []
            for el in vector:
                if el == ";":
                    outer.append(inner)
                    inner = []
                else:
                    inner.append(el)
            outer.append(inner)
            return outer

        matrix = _create_matrix(node.vector) if ';' in node.vector else node.vector
        return np.array(matrix)

    @when(Block)
    def visit(self, node: Block):
        node.statements.accept(self)

    @when(If)
    def visit(self, node: If):
        cond = node.cond_expr.accept(self)
        if cond:
            node.if_block.accept(self)
        elif node.else_block:
            node.else_block.accept(self)

    @when(While)
    def visit(self, node: While):
        while node.cond_expr.accept(self):
            try:
                node.while_block.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue

    @when(ForExpr)
    def visit(self, node: ForExpr):
        return node.for_id.value, node.start_expr.accept(self), node.end_expr.accept(self)

    @when(For)
    def visit(self, node: For):
        self.memory.push()
        var_id, start, end = node.iteration.accept(self)
        self.memory.put(var_id, start)
        while self.memory.get(var_id) < end:
            try:
                node.for_block.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
            finally:
                self.memory.put(var_id, self.memory.get(var_id) + 1)  # doesn't matter for break anyway
        self.memory.pop()

    @when(Print)
    def visit(self, node: Print):
        values = [expr.accept(self) for expr in node.expressions]
        print(*values, sep=" ")

    @when(Assignment)
    def visit(self, node: Assignment):
        value = node.expression.accept(self)
        name = node.assign_id.value
        if node.with_ref:
            matrix = self.memory.get(name)
            first_slice = node.with_ref[0].accept(self)
            second_slice = node.with_ref[1].accept(self)
            matrix[first_slice][second_slice] = value
        else:
            if node.assign_op == "=":
                self.memory.put(name, value)
            else:
                var_value = node.assign_id.accept(self)
                evaluated_value = self._ops[node.assign_op](var_value, value)
                self.memory.put(name, evaluated_value)

    @when(Assignments)
    def visit(self, node: Assignments):
        for assignment in node.assignments:
            assignment.accept(self)

    @when(ControlExpr)
    def visit(self, node: ControlExpr):
        return node.accept(self)

    @when(Break)
    def visit(self, node: Break):
        raise BreakException

    @when(Continue)
    def visit(self, node: Continue):
        raise ContinueException

    @when(Return)
    def visit(self, node: Return):
        value = node.expressions[0].accept(self)
        raise ReturnValueException(value)

    @when(BinOp)
    def visit(self, node: BinOp):
        left = node.left_expr.accept(self)
        right = node.right_expr.accept(self)
        return self._ops[node.bin_op](left, right)
