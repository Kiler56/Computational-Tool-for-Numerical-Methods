"""
Método de Bisección — búsqueda de raíces por intervalos.
Basado en la implementación de Jul (MetodosJul).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Bisection(NumericalMethod):

    @property
    def name(self) -> str:
        return "bisection"

    @property
    def description(self) -> str:
        return "Bisección"

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
                "<li>Ingrese una función <code>f(x)</code> y un intervalo <code>[a, b]</code>.</li>"
                "<li>⚠️ <strong>Requisito:</strong> <code>f(a)</code> y <code>f(b)</code> deben tener signos opuestos (Teorema de Bolzano).</li>"
                "<li>El método divide el intervalo por la mitad sucesivamente hasta encontrar la raíz con la tolerancia indicada.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter a function <code>f(x)</code> and an interval <code>[a, b]</code>.</li>"
                "<li>⚠️ <strong>Requirement:</strong> <code>f(a)</code> and <code>f(b)</code> must have opposite signs (Bolzano's Theorem).</li>"
                "<li>The method repeatedly halves the interval until the root is found within the given tolerance.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        a = float(params.get("a", 0))
        b = float(params.get("b", 2))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))

        fa = f(a)
        fb = f(b)
        if fa * fb > 0:
            raise ValueError("f(a) y f(b) deben tener signos opuestos.")

        steps = []
        xm = (a + b) / 2
        E = None

        for i in range(1, N + 1):
            fxm = f(xm)
            step = {
                "step": i,
                "phase": "bisection",
                "a": a, "b": b, "xm": xm,
                "f_xm": fxm,
                "error": E,
                "description": f"Iter {i}: xm = {xm:.10g}, f(xm) = {fxm:.6e}" + (f", E = {E:.6e}" if E is not None else ""),
            }
            steps.append(step)

            if fa * fxm < 0:
                b = xm
            else:
                a = xm
                fa = f(a)

            x_old = xm
            xm = (a + b) / 2
            E = abs(xm - x_old)

            if E < tol:
                steps.append({
                    "step": i + 1, "phase": "converged",
                    "description": f"Convergió: xm = {xm:.10g}, E = {E:.6e}",
                    "a": a, "b": b, "xm": xm, "f_xm": f(xm), "error": E,
                })
                break

        return {
            "solution": [xm],
            "root": xm,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
