import re


class IntentClassifier:

    def detect(self, message: str) -> str:

        text = message.lower().strip()

        # =====================================================
        # EMPTY MESSAGE
        # =====================================================

        if not text:
            return "AI"

        # =====================================================
        # GRAPH
        # =====================================================

        graph_keywords = [
            "graph",
            "plot",
            "draw graph",
            "plot graph",
        ]

        if any(keyword in text for keyword in graph_keywords):
            return "GRAPH"

        # =====================================================
        # MATH COMMANDS
        # =====================================================

        math_keywords = [
            "simplify",
            "factor",
            "expand",
            "solve",
            "integrate",
            "differentiate",
            "derivative",
            "differentiate",
            "limit",
        ]

        if any(text.startswith(keyword) for keyword in math_keywords):
            return "MATH"

        # =====================================================
        # DIRECT MATHEMATICAL EXPRESSIONS
        # =====================================================

        math_pattern = r"^[\d\s\+\-\*\/\^\(\)\.\=xX]+$"

        if re.match(math_pattern, text):

            # Make sure it actually contains
            # a mathematical operator.

            operators = [
                "+",
                "-",
                "*",
                "/",
                "^",
                "=",
            ]

            if any(operator in text for operator in operators):
                return "MATH"

        # =====================================================
        # WEB / CURRENT INFORMATION
        # =====================================================

        web_keywords = [
            "latest",
            "news",
            "today",
            "current",
            "recent",
            "search",
            "right now",
        ]

        if any(keyword in text for keyword in web_keywords):
            return "WEB"

        # =====================================================
        # EVERYTHING ELSE
        # =====================================================

        return "AI"