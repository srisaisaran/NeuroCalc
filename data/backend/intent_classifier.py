class IntentClassifier:
    
    def detect(self, message):

        text = message.lower().strip()

        math_keywords = [
            "simplify",
            "factor",
            "expand",
            "solve",
            "integrate",
            "differentiate",
            "derivative",
            "limit"
        ]

        graph_keywords = [
            "graph",
            "plot"
        ]

        web_keywords = [
            "latest",
            "news",
            "today",
            "current",
            "search"
        ]

        if any(text.startswith(word) for word in graph_keywords):
            return "GRAPH"

        if any(text.startswith(word) for word in math_keywords):
            return "MATH"

        if any(word in text for word in web_keywords):
            return "WEB"

        return "AI"