import math
import re

def safe_factorial(n):
    n = int(n)
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return math.factorial(n)

safe_dict = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
    "factorial": safe_factorial,
    "exp": math.exp,
    "round": round,
}

def prepare_expression(expr):
    expr = expr.replace("×", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace("^", "**")
    expr = re.sub(r'(\d+)!', r'factorial(\1)', expr)
    expr = expr.replace("pi", str(math.pi))
    expr = expr.replace("e", str(math.e))
    return expr