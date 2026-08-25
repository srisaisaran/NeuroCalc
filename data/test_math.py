from math_engine import MathEngine

math = MathEngine()

print(math.solve_expression("2+2"))
print(math.simplify_expression("(x+x+x)"))
print(math.expand_expression("(x+2)*(x+3)"))
print(math.factor_expression("x**2+5*x+6"))