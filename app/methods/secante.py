"""
Método de la Secante — búsqueda de raíces sin derivada.
Implementado desde el pseudocódigo de Camilo (metodosCamilo).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Secante(NumericalMethod):

    @property
    def name(self) -> str:
        return "secante"

    @property
    def description(self) -> str:
        return "Secante"

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "x₀ (primer punto)", "label_en": "x₀ (first point)", "type": "float", "default": 0},
            {"key": "x1", "label_es": "x₁ (segundo punto)", "label_en": "x₁ (second point)", "type": "float", "default": 2},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y dos puntos iniciales <code>x₀</code> y <code>x₁</code>.</li>"
                "<li>Usa la recta secante entre los dos últimos puntos para estimar la raíz, sin necesitar la derivada.</li>"
                "<li>💡 <strong>Ventaja:</strong> No requiere calcular derivadas (más rápido por iteración que Newton).</li>"
                "<li>⚠️ Puede no converger si los puntos iniciales están mal elegidos.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and two initial points <code>x₀</code> and <code>x₁</code>.</li>"
                "<li>Uses the secant line between the last two points to estimate the root, without computing derivatives.</li>"
                "<li>💡 <strong>Advantage:</strong> No derivative computation needed (faster per iteration than Newton).</li>"
                "<li>⚠️ May not converge if the initial points are poorly chosen.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        x0 = float(params.get("x0", 0))
        x1 = float(params.get("x1", 2))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))
        steps = []

        for i in range(1, N + 1):
            f0 = f(x0)
            f1 = f(x1)

            denom = f1 - f0
            if abs(denom) < 1e-15:
                raise ValueError(f"División por cero: f(x₁) - f(x₀) ≈ 0 en iteración {i}.")

            x2 = x1 - f1 * (x1 - x0) / denom
            E = abs(x2 - x1)

            steps.append({
                "step": i, "phase": "secante",
                "x0": x0, "x1": x1, "x2": x2,
                "f_x0": f0, "f_x1": f1, "error": E,
                "description": f"Iter {i}: x0={x0:.8g}, x1={x1:.8g}, x2={x2:.10g}, E = {E:.6e}",
            })

            if E < tol:
                steps[-1]["phase"] = "converged"
                break

            x0 = x1
            x1 = x2

        return {
            "solution": [x2],
            "root": x2,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
