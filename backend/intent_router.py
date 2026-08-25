from ai_engine import AIEngine
from graph_engine import GraphEngine
from math_engine import MathEngine
from intent_classifier import IntentClassifier


class IntentRouter:

    def __init__(self):
        self.math = MathEngine()
        self.ai = AIEngine()
        self.graph = GraphEngine()
        self.classifier = IntentClassifier()

    def process(self, message: str) -> str:

        intent = self.classifier.detect(message)

        print(f"INTENT: {intent}")

        # =====================================================
        # MATH
        # =====================================================

        if intent == "MATH":

            text = message.lower().strip()

            if text.startswith("simplify"):
                expression = message[len("simplify"):].strip()
                return self.math.simplify_expression(expression)

            if text.startswith("factor"):
                expression = message[len("factor"):].strip()
                return self.math.factor_expression(expression)

            if text.startswith("expand"):
                expression = message[len("expand"):].strip()
                return self.math.expand_expression(expression)

            if text.startswith("solve"):
                expression = message[len("solve"):].strip()

                try:
                    result = self.math.calculate(expression)

                    if result["success"]:
                        return f"**Result:** {result['result']}"

                except Exception:
                    pass

            # If it wasn't a specialized operation,
            # send it to the normal AI.
            return self.ai.generate_response(message)

        # =====================================================
        # GRAPH
        # =====================================================

        if intent == "GRAPH":

            expression = message.lower().strip()

            if expression.startswith("graph"):
                expression = expression[len("graph"):].strip()

            expression = (
                expression
                .replace("y=", "")
                .replace("y =", "")
                .strip()
            )

            try:
                self.graph.plot(expression)

                return "📈 Graph generated successfully."

            except Exception as e:
                return f"Graph Error: {e}"

        # =====================================================
        # WEB
        # =====================================================

        if intent == "WEB":

            return self.ai.generate_response(message)

        # =====================================================
        # GENERAL AI
        # =====================================================

        return self.ai.generate_response(message)

    def reset_history(self):

        if hasattr(self.ai, "reset_history"):
            self.ai.reset_history()