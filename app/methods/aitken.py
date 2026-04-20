"""
Método de la Secante Modificado por Aitken (o proceso delta-cuadrado de Aitken).
Acelera la convergencia de una sucesión. Lo aplicaremos sobre una secuencia generada
por punto fijo o Newton-like approach. Para ser un método base de búsqueda de raíces,
lo enfocaremos como un punto fijo acelerado.
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Aitken(NumericalMethod):

    @property
    def name(self) -> str:
        return "aitken"

    @property
    def description(self) -> str:
        return "Aceleración de Aitken"

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "Valor inicial (x₀)", "label_en": "Initial value (x₀)", "type": "float", "default": 0.5},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese una función de iteración <code>g(x)</code> para buscar un punto fijo.</li>"
                "<li>El método de Aitken aplica un delta-cuadrado a tres puntos sucesivos para acelerar la convergencia.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter an iteration function <code>g(x)</code> to search for a fixed point.</li>"
                "<li>Aitken's method applies a delta-squared process to three successive points to accelerate convergence.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        g = make_function(expr)
        x0 = float(params.get("x0", 0.5))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))
        steps = []

        x = x0
        for i in range(1, N + 1):
            x1 = g(x)
            x2 = g(x1)
            
            denom = x2 - 2 * x1 + x
            if denom == 0:
                raise ValueError("División por cero en el denominador de Aitken.")

            x_new = x - ((x1 - x) ** 2) / denom
            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "aitken",
                "x": x, "x1": x1, "x2": x2, "x_new": x_new, "error": E,
                "description": f"Iter {i}: x={x:.6f}, x1={x1:.6f}, x2={x2:.6f}, x_new={x_new:.6f}, E={E:.6e}"
            })

            if E < tol:
                steps[-1]["phase"] = "converged"
                break
            
            x = x_new

        return {
            "solution": [x_new],
            "root": x_new,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
