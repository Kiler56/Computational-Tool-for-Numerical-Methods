"""
Raíces Múltiples — método modificado de Newton para raíces con multiplicidad > 1.
Basado en el pseudocódigo de Camilo (metodosCamilo).
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class RaicesMultiples(NumericalMethod):

    @property
    def name(self) -> str:
        return "raices_multiples"

    @property
    def description(self) -> dict:
        return {"es": "Raíces Múltiples", "en": "Multiple Roots"}

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def plot_type(self) -> str:
        return "root_convergence"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "Valor inicial (x₀)", "label_en": "Initial value (x₀)", "type": "float", "default": 1.5},
            {"key": "tol", "label_es": "tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
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
        # ── Parse function ────────────────────────────────────────────────
        try:
            f = make_function(expr)
        except Exception as e:
            raise ValueError(f"Invalid expression '{expr}': {e}") from e

        # ── Parse parameters ──────────────────────────────────────────────
        try:
            x = float(params.get("x0", 1.5))
            tol = float(params.get("tol", 1e-7))
            N = int(params.get("max_iter", 100))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid parameter: {e}") from e

        if tol <= 0:
            raise ValueError("Tolerance must be positive.")
        if N <= 0:
            raise ValueError("max_iter must be a positive integer.")
        if not math.isfinite(x):
            raise ValueError("Initial value x₀ must be a finite number.")

        steps = []
        x_new = x

        for i in range(1, N + 1):
            # ── Evaluate f, f', f'' ───────────────────────────────────────
            try:
                fx = f(x)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero in f({x:.10g}) at iteration {i}.")
            except OverflowError:
                raise ValueError(f"Overflow in f({x:.10g}) at iteration {i}.")
            except Exception as e:
                raise ValueError(f"Error evaluating f({x:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(fx):
                raise ValueError(f"f({x:.10g}) = {fx} is not finite at iteration {i}.")

            try:
                dfx = self._deriv(f, x)
                d2fx = self._deriv2(f, x)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero computing derivatives at x = {x:.10g} (iter {i}).")
            except OverflowError:
                raise ValueError(f"Overflow computing derivatives at x = {x:.10g} (iter {i}).")
            except Exception as e:
                raise ValueError(f"Error computing derivatives at x = {x:.10g} (iter {i}): {e}") from e

            if not math.isfinite(dfx) or not math.isfinite(d2fx):
                raise ValueError(
                    f"Derivative not finite at x = {x:.10g} (iter {i}): "
                    f"f' = {dfx}, f'' = {d2fx}."
                )

            denom = dfx ** 2 - fx * d2fx
            if abs(denom) < 1e-15:
                raise ValueError(
                    f"Division by zero at iteration {i}: f'² - f·f'' ≈ {denom:.2e} at x = {x:.10g}. "
                    "This can happen at inflection points or if f and f'' balance each other. "
                    "Try a different starting point."
                )

            x_new = x - (fx * dfx) / denom

            if not math.isfinite(x_new):
                raise ValueError(
                    f"x_new = {x_new} is not finite at iteration {i}. "
                    "The method is diverging — try a closer initial guess."
                )

            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "multiple_roots",
                "x": x, "f_x": fx, "df_x": dfx, "d2f_x": d2fx,
                "x_new": x_new, "error": E,
                "description": {"es": f"Iter {i}: x={x:.10g}, f={fx:.6e}, f'={dfx:.6e}, f''={d2fx:.6e}, x_new={x_new:.10g}, E={E:.6e}", "en": f"Iter{i}:x={x:.10g}, f={fx:.6e}, f'={dfx:.6e}, f''={d2fx:.6e}, x_new={x_new:.10g}, E={E:.6e}"},
            })

            if E < tol:
                steps[-1]["phase"] = "converged"
                break

            x = x_new
        else:
            steps.append({
                "step": N + 1, "phase": "max_iter_reached",
                "description": {"es": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x = {x_new:.10g}. "
                    "Try a different x₀ or increase max_iter."
                ), "en": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x = {x_new:.10g}. "
                    "Try a different x₀ or increase max_iter."
                )},
            })

        return {
            "solution": [x_new],
            "root": x_new,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }
