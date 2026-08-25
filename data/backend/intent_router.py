from ai_engine import AIEngine
from graph_engine import GraphEngine
from math_engine import MathEngine


class IntentRouter:

    def __init__(self):
        self.math = MathEngine()
        self.ai = AIEngine()
        self.graph = GraphEngine()

    def process(self, message: str) -> str:
        text = message.lower().strip()

        if text.startswith("simplify"):
            expression = message[len("simplify") :].strip()
            return self.math.simplify_expression(expression)

        elif text.startswith("factor"):
            expression = message[len("factor") :].strip()
            return self.math.factor_expression(expression)

        elif text.startswith("expand"):
            expression = message[len("expand") :].strip()
            return self.math.expand_expression(expression)

        elif text.startswith("graph"):
            expression = message[len("graph") :].strip()

            # Clean out common y = prefixes
            expression = expression.replace("y=", "").replace("y =", "").strip()

            self.graph.plot(expression)
            return "📈 Graph generated successfully."

        else:
            return self.ai.generate_response(message)

    def reset_history(self):
        """Helper to clear AI chat memory when starting a new session."""
        if hasattr(self.ai, "reset_history"):
            self.ai.reset_history()