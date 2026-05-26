"""
Método de Steffensen — Búsqueda de raíces.
Similar a Newton pero usa una aproximación de la derivada basada en la propia función.
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Steffensen(NumericalMethod):

    @property
    def name(self) -> str:
        return "steffensen"

    @property
    def description(self) -> dict:
        return {"es": "Steffensen", "en": "Steffensen"}

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

        steps = []
        x_new = x

        for i in range(1, N + 1):
            # ── f(x) ──────────────────────────────────────────────────────
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

            # ── f(x + f(x)) ───────────────────────────────────────────────
            x_shifted = x + fx
            if not math.isfinite(x_shifted):
                raise ValueError(
                    f"x + f(x) = {x_shifted} at iteration {i}. "
                    "f(x) is too large — the method cannot evaluate f(x + f(x))."
                )
            try:
                f_x_fx = f(x_shifted)
            except ZeroDivisionError:
                raise ValueError(
                    f"Division by zero in f(x + f(x)) = f({x_shifted:.10g}) at iteration {i}."
                )
            except OverflowError:
                raise ValueError(
                    f"Overflow in f(x + f(x)) at iteration {i}. "
                    "f(x) is too large, making x + f(x) far from the root."
                )
            except Exception as e:
                raise ValueError(
                    f"Error evaluating f(x + f(x)) at iteration {i}: {e}"
                ) from e

            if not math.isfinite(f_x_fx):
                raise ValueError(f"f(x + f(x)) = {f_x_fx} is not finite at iteration {i}.")

            denom = f_x_fx - fx
            if abs(denom) < 1e-15:
                raise ValueError(
                    f"Division by zero at iteration {i}: f(x + f(x)) - f(x) ≈ {denom:.2e}. "
                    "The denominator in Steffensen's formula is zero. "
                    "This happens when f(x + f(x)) ≈ f(x), i.e., f is nearly constant near x. "
                    "Try a different initial value."
                )

            x_new = x - (fx ** 2) / denom

            if not math.isfinite(x_new):
                raise ValueError(
                    f"x_new = {x_new} is not finite at iteration {i}. "
                    "The method is diverging."
                )

            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "steffensen",
                "x": x, "f_x": fx, "f_x_fx": f_x_fx, "x_new": x_new, "error": E,
                "description": {"es": f"Iter {i}: x={x:.6f}, f(x)={fx:.6e}, x_new={x_new:.6f}, E={E:.6e}", "en": f"Iter{i}:x={x:.6f}, f(x)={fx:.6e}, x_new={x_new:.6f}, E={E:.6e}"}
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
                    "Try a closer initial guess or increase max_iter."
                ), "en": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x = {x_new:.10g}. "
                    "Try a closer initial guess or increase max_iter."
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
