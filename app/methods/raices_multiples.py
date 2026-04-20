"""
Raíces Múltiples — método modificado de Newton para raíces con multiplicidad > 1.
Basado en el pseudocódigo de Camilo (metodosCamilo).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class RaicesMultiples(NumericalMethod):

    @property
    def name(self) -> str:
        return "raices_multiples"

    @property
    def description(self) -> str:
        return "Raíces Múltiples"

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
                "<li>Usa la fórmula modificada: <code>x_{n+1} = x_n - f·f' / (f'² - f·f'')</code> para manejar raíces con multiplicidad.</li>"
                "<li>💡 <strong>Ventaja:</strong> Mantiene convergencia cuadrática incluso con raíces de multiplicidad > 1, donde Newton estándar se vuelve lento.</li>"
                "<li>⚠️ Requiere evaluar f, f' y f'' numéricamente en cada paso.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and an initial value <code>x₀</code>.</li>"
                "<li>Uses the modified formula: <code>x_{n+1} = x_n - f·f' / (f'² - f·f'')</code> to handle roots with multiplicity.</li>"
                "<li>💡 <strong>Advantage:</strong> Maintains quadratic convergence even for roots with multiplicity > 1, where standard Newton slows down.</li>"
                "<li>⚠️ Requires evaluating f, f' and f'' numerically at each step.</li>"
                "</ul>"
            ),
        }

    @staticmethod
    def _deriv(f, x, h=1e-5):
        return (f(x + h) - f(x - h)) / (2 * h)

    @staticmethod
    def _deriv2(f, x, h=1e-5):
        return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        x = float(params.get("x0", 1.5))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))
        steps = []

        for i in range(1, N + 1):
            fx = f(x)
            dfx = self._deriv(f, x)
            d2fx = self._deriv2(f, x)

            denom = dfx ** 2 - fx * d2fx
            if abs(denom) < 1e-15:
                raise ValueError(f"División por cero en iteración {i}: f'² - f·f'' ≈ 0.")

            x_new = x - (fx * dfx) / denom
            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "multiple_roots",
                "x": x, "f_x": fx, "df_x": dfx, "d2f_x": d2fx,
                "x_new": x_new, "error": E,
                "description": f"Iter {i}: x={x:.10g}, f={fx:.6e}, f'={dfx:.6e}, f''={d2fx:.6e}, x_new={x_new:.10g}, E={E:.6e}",
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
