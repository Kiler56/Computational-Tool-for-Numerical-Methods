"""
Método de Steffensen — Búsqueda de raíces.
Similar a Newton pero usa una aproximación de la derivada basada en la propia función.
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Steffensen(NumericalMethod):

    @property
    def name(self) -> str:
        return "steffensen"

    @property
    def description(self) -> str:
        return "Steffensen"

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "Valor inicial (x₀)", "label_en": "Initial value (x₀)", "type": "float", "default": 1.5},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y un valor inicial <code>x₀</code>.</li>"
                "<li>Usa <code>x_{n+1} = x_n - f(x_n)² / (f(x_n + f(x_n)) - f(x_n))</code>.</li>"
                "<li>💡 Alternativa a Newton sin necesidad de calcular la derivada explícitamente.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and an initial value <code>x₀</code>.</li>"
                "<li>Uses <code>x_{n+1} = x_n - f(x_n)² / (f(x_n + f(x_n)) - f(x_n))</code>.</li>"
                "<li>💡 Newton-like alternative without explicit derivative calculations.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        x = float(params.get("x0", 1.5))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))
        steps = []

        for i in range(1, N + 1):
            fx = f(x)
            f_x_fx = f(x + fx)
            
            denom = f_x_fx - fx
            if abs(denom) < 1e-15:
                raise ValueError("División por cero en el denominador de Steffensen.")

            x_new = x - (fx ** 2) / denom
            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "steffensen",
                "x": x, "f_x": fx, "f_x_fx": f_x_fx, "x_new": x_new, "error": E,
                "description": f"Iter {i}: x={x:.6f}, f(x)={fx:.6e}, x_new={x_new:.6f}, E={E:.6e}"
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
