"""
Trisección — búsqueda de raíces dividiendo el intervalo en 3.
Basado en la implementación de Jul (MetodosJul).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Trisection(NumericalMethod):

    @property
    def name(self) -> str:
        return "trisection"

    @property
    def description(self) -> str:
        return "Trisección"

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "a", "label_es": "Extremo izquierdo (a)", "label_en": "Left endpoint (a)", "type": "float", "default": 0},
            {"key": "b", "label_es": "Extremo derecho (b)", "label_en": "Right endpoint (b)", "type": "float", "default": 2},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y un intervalo <code>[a, b]</code>.</li>"
                "<li>Divide el intervalo en tres partes iguales en cada iteración y selecciona el subintervalo que contiene la raíz.</li>"
                "<li>⚠️ <strong>Requisito:</strong> Debe existir un cambio de signo en <code>[a, b]</code>.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and an interval <code>[a, b]</code>.</li>"
                "<li>Divides the interval into three equal parts each iteration and selects the sub-interval containing the root.</li>"
                "<li>⚠️ <strong>Requirement:</strong> A sign change must exist in <code>[a, b]</code>.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        a = float(params.get("a", 0))
        b = float(params.get("b", 2))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))

        steps = []
        E = None

        for i in range(1, N + 1):
            x1 = a + (b - a) / 3
            x2 = b - (b - a) / 3

            steps.append({
                "step": i, "phase": "trisection",
                "a": a, "b": b, "x1": x1, "x2": x2,
                "f_x1": f(x1), "f_x2": f(x2), "error": E,
                "description": f"Iter {i}: a={a:.8g}, x1={x1:.8g}, x2={x2:.8g}, b={b:.8g}" + (f", E={E:.6e}" if E else ""),
            })

            fa = f(a)
            if fa * f(x1) < 0:
                b = x1
            elif f(x1) * f(x2) < 0:
                a = x1
                b = x2
            else:
                a = x2

            E = abs(b - a)
            if E < tol:
                break

        xm = (a + b) / 2
        steps.append({
            "step": len(steps) + 1, "phase": "converged",
            "description": f"Convergió: raíz ≈ {xm:.10g}, E = {E:.6e}",
            "a": a, "b": b, "xm": xm, "f_xm": f(xm), "error": E,
        })

        return {
            "solution": [xm],
            "root": xm,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
