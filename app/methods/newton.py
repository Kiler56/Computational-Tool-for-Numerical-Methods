"""
Método de Newton-Raphson — búsqueda de raíces con derivada numérica.
Basado en la implementación de Camilo (metodosCamilo).
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
            {"key": "x0", "label_es": "Valor inicial (x₀)", "label_en": "Initial value (x₀)", "type": "float", "default": 1.5},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y un valor inicial <code>x₀</code> cercano a la raíz.</li>"
                "<li>Usa la fórmula <code>x_{n+1} = x_n - f(x_n)/f'(x_n)</code> con derivada numérica aproximada.</li>"
                "<li>💡 <strong>Ventaja:</strong> Convergencia cuadrática cuando el valor inicial es cercano a la raíz.</li>"
                "<li>⚠️ Puede fallar si la derivada es cero o si el valor inicial está lejos de la raíz.</li>"
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
                raise ValueError(f"Derivada cero en x = {x:.10g}. No se puede continuar.")

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
