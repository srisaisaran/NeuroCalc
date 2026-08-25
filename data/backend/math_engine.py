import sympy as sp


class MathEngine:

    def solve_expression(self, expression):
        try:
            result = sp.sympify(expression)
            return str(result)
        except Exception as e:
            return f"Math Error: {e}"

    def simplify_expression(self, expression):
        try:
            result = sp.simplify(expression)
            return str(result)
        except Exception as e:
            return f"Math Error: {e}"

    def expand_expression(self, expression):
        try:
            result = sp.expand(expression)
            return str(result)
        except Exception as e:
            return f"Math Error: {e}"

    def factor_expression(self, expression):
        try:
            result = sp.factor(expression)
            return str(result)
        except Exception as e:
            return f"Math Error: {e}"