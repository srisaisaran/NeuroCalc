MATH_SYMBOLS = "+-*/^=()"


def is_math_question(message: str) -> bool:

    return any(symbol in message for symbol in MATH_SYMBOLS)