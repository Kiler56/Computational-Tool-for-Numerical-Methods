"""
Newton–Raphson root finding with a numerical derivative.
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Newton(NumericalMethod):

    @property
    def name(self) -> str:
        return "newton"

    @property
    def description(self) -> str:
        return "Newton-Raphson"

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "Initial value (x₀)", "label_en": "Initial value (x₀)", "type": "float", "default": 1.5},
            {"key": "tol", "label_es": "Tolerance", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Max iterations", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and an initial <code>x₀</code> near the root.</li>"
                "<li>Uses <code>x_{n+1} = x_n - f(x_n)/f'(x_n)</code> with a numerical derivative.</li>"
                "<li>💡 Often quadratic convergence when <code>x₀</code> is good.</li>"
                "<li>⚠️ Can fail if the derivative vanishes or the guess is poor.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and an initial value <code>x₀</code> close to the root.</li>"
                "<li>Uses <code>x_{n+1} = x_n - f(x_n)/f'(x_n)</code> with a numerical derivative approximation.</li>"
                "<li>💡 <strong>Advantage:</strong> Quadratic convergence when the initial value is close to the root.</li>"
                "<li>⚠️ May fail if the derivative is zero or if the initial value is far from the root.</li>"
                "</ul>"
            ),
        }

    @staticmethod
    def _numerical_derivative(f, x, h=1e-8):
        return (f(x + h) - f(x - h)) / (2 * h)

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        x = float(params.get("x0", 1.5))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))
        steps = []

        for i in range(1, N + 1):
            fx = f(x)
            dfx = self._numerical_derivative(f, x)

            if abs(dfx) < 1e-15:
                raise ValueError(f"Zero derivative at x = {x:.10g}; cannot continue.")

            x_new = x - fx / dfx
            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "newton",
                "x": x, "f_x": fx, "df_x": dfx, "x_new": x_new, "error": E,
                "description": f"Iter {i}: x = {x:.10g}, f(x) = {fx:.6e}, f'(x) = {dfx:.6e}, x_new = {x_new:.10g}, E = {E:.6e}",
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
