"""
Posición Falsa (Regula Falsi) — búsqueda de raíces.
Basado en la implementación de Jul (MetodosJul).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class FalsePosition(NumericalMethod):

    @property
    def name(self) -> str:
        return "false_position"

    @property
    def description(self) -> str:
        return "Posición Falsa (Regula Falsi)"

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
                "<li>Ingrese <code>f(x)</code> y un intervalo <code>[a, b]</code> con cambio de signo.</li>"
                "<li>A diferencia de Bisección, usa interpolación lineal para elegir el punto intermedio, convergiendo más rápido en muchos casos.</li>"
                "<li>⚠️ <strong>Requisito:</strong> <code>f(a) · f(b) &lt; 0</code>.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and an interval <code>[a, b]</code> with a sign change.</li>"
                "<li>Unlike Bisection, it uses linear interpolation to choose the midpoint, converging faster in many cases.</li>"
                "<li>⚠️ <strong>Requirement:</strong> <code>f(a) · f(b) &lt; 0</code>.</li>"
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

        xm = (fb * a - fa * b) / (fb - fa)
        steps = []
        E = None

        for i in range(1, N + 1):
            fxm = f(xm)
            steps.append({
                "step": i, "phase": "false_position",
                "a": a, "b": b, "xm": xm, "f_xm": fxm, "error": E,
                "description": f"Iter {i}: xm = {xm:.10g}, f(xm) = {fxm:.6e}" + (f", E = {E:.6e}" if E is not None else ""),
            })

            if fa * fxm < 0:
                b = xm
                fb = f(b)
            else:
                a = xm
                fa = f(a)

            x_old = xm
            xm = (fb * a - fa * b) / (fb - fa)
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
