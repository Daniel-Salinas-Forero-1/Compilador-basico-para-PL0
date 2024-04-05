from Visitor import Visitor


class Evaluator(Visitor):
    @classmethod
    def eval(cls, n: Node):
        vis = cls()
        return n.accept(vis)

    def visit(self, n: Number):
        return n.value

    def visit(self, n: Binary):
        left = n.left.accept(self)
        right = n.right.accept(self)

        if n.op == '^':
            return left ** right
        else:
            return eval(f'{left} {n.op} {right}')

    def visit(self, n: Factorial):
        expr_val = n.expr.accept(self)
        return math.factorial(expr_val)

    def visit(self, n: FunctionCall):
        if n.func_name == 'sin':
            return math.sin(n.expr.accept(self))
        elif n.func_name == 'cos':
            return math.cos(n.expr.accept(self))
        elif n.func_name == 'asin':
            return math.asin(n.expr.accept(self))
        elif n.func_name == 'acos':
            return math.acos(n.expr.accept(self))
        elif n.func_name == 'atan':
            return math.atan(n.expr.accept(self))
        elif n.func_name == 'log':
            return math.log(n.expr.accept(self))
        elif n.func_name == 'random':
            return random.random()

    def visit(self, n: Assignment):
        value = n.expr.accept(self)
        Variables.set(n.variable, value)
        return value
