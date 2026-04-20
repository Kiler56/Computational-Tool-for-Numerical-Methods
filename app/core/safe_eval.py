"""
Evaluación segura de expresiones matemáticas ingresadas por el usuario.
Solo permite funciones de math, sin acceso a builtins peligrosos.
"""
import math

# Funciones matemáticas permitidas en las expresiones del usuario
_SAFE_MATH = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "exp": math.exp,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "sqrt": math.sqrt,
    "abs": abs,
    "pi": math.pi,
    "e": math.e,
    "inf": math.inf,
}


def safe_eval_expr(expr: str, x: float) -> float:
    """Evalúa una expresión matemática de forma segura.

    Args:
        expr: Expresión como string, e.g. 'x**2 - 2'
        x: Valor de la variable x

    Returns:
        Resultado numérico de evaluar la expresión en x.
    """
    allowed = {"x": x, "__builtins__": {}}
    allowed.update(_SAFE_MATH)
    return float(eval(expr, allowed))


def make_function(expr: str):
    """Crea una función f(x) a partir de un string de expresión.

    Returns:
        callable: función que recibe un float y retorna un float
    """
    def f(x):
        return safe_eval_expr(expr, x)
    return f
