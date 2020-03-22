class Node(object):
    pass

# statements
class Statements(Node):
    pass

# block
# statement
class Statement(Node):
    pass

class If(Statement):
    def __init__(self, cond, body, else_body=None):
        self.cond = cond
        self.body = body
        self.else_body = else_body

class While(Statement):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class For(Statement):
    def __init__(self, iteration, body):
        self.iteration = iteration
        self.body = body

class Print(Statement):
    def __init__(self, content):
        self.content = content

#TODO: Assign, Control
# expression
class Expr:
    pass

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class ParenExpression(Expr):
    def __init__(self, expression):
        self.expression = expression

class VariableExpression(Expr):
    def __init__(self, variable):
        self.variable = variable

#variable
#const
# for_expression
# print_expression
# control_expression
class ControlExpr(Node):
    pass

class Break(ControlExpr):
    pass

class Continue(ControlExpr):
    pass

class Return(ControlExpr):
    def __init__(self, value):
        self.value = value
#assignment
#matrix_ref
#matrix
#matrix_rows
#matrix_row