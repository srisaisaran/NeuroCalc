import sympy as sp


class MathEngine:

    def calculate(self, expression: str):

        try:
            result = sp.sympify(expression)

            return {
                "success": True,
                "result": str(result)
            }

        except Exception as e:

            print(f"Math Error: {e}")

            return {
                "success": False,
                "result": None
            }