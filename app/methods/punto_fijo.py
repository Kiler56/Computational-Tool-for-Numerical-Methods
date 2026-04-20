"""
Método de Punto Fijo — iteración funcional.
Basado en la implementación de Camilo (metodosCamilo).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class PuntoFijo(NumericalMethod):

    @property
    def name(self) -> str:
        return "punto_fijo"

    @property
    def description(self) -> str:
        return "Punto Fijo"

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
                "<li>Ingrese la función de iteración <code>g(x)</code> (no <code>f(x)</code>).</li>"
                "<li>Se busca un punto fijo donde <code>x = g(x)</code>, lo cual equivale a una raíz de <code>f(x) = x - g(x) = 0</code>.</li>"
                "<li>💡 <strong>Ejemplo:</strong> Para resolver <code>x² - 2 = 0</code>, puede usar <code>g(x) = (x + 2/x)/2</code>.</li>"
                "<li>⚠️ <strong>Requisito:</strong> <code>|g'(x)| &lt; 1</code> en la vecindad de la raíz para garantizar convergencia.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter the iteration function <code>g(x)</code> (not <code>f(x)</code>).</li>"
                "<li>Searches for a fixed point where <code>x = g(x)</code>, equivalent to a root of <code>f(x) = x - g(x) = 0</code>.</li>"
                "<li>💡 <strong>Example:</strong> To solve <code>x² - 2 = 0</code>, use <code>g(x) = (x + 2/x)/2</code>.</li>"
                "<li>⚠️ <strong>Requirement:</strong> <code>|g'(x)| &lt; 1</code> near the root to guarantee convergence.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        g = make_function(expr)
        x = float(params.get("x0", 1.5))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))
        steps = []

        for i in range(1, N + 1):
            x_new = g(x)
            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "fixed_point",
                "x": x, "g_x": x_new, "error": E,
                "description": f"Iter {i}: x = {x:.10g}, g(x) = {x_new:.10g}, E = {E:.6e}",
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
