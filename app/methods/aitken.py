"""
Método de la Secante Modificado por Aitken (proceso delta-cuadrado).
Acelera la convergencia de punto fijo.
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Aitken(NumericalMethod):

    @property
    def name(self) -> str:
        return "aitken"

    @property
    def description(self) -> dict:
        return {"es": "Aceleración de Aitken", "en": "Aitken's Acceleration"}

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def plot_type(self) -> str:
        return "root_convergence"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "Valor inicial (x₀)", "label_en": "Initial value (x₀)", "type": "float", "default": 0.5},
            {"key": "tol", "label_es": "tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese una función de iteración <code>g(x)</code> para buscar un punto fijo.</li>"
                "<li>El método de Aitken aplica un delta-cuadrado a tres puntos sucesivos para acelerar la convergencia.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter an iteration function <code>g(x)</code> to search for a fixed point.</li>"
                "<li>Aitken's method applies a delta-squared process to three successive points to accelerate convergence.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        # ── Parse function ────────────────────────────────────────────────
        try:
            g = make_function(expr)
        except Exception as e:
            raise ValueError(f"Invalid expression '{expr}': {e}") from e

        # ── Parse parameters ──────────────────────────────────────────────
        try:
            x0 = float(params.get("x0", 0.5))
            tol = float(params.get("tol", 1e-7))
            N = int(params.get("max_iter", 100))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid parameter: {e}") from e

        if tol <= 0:
            raise ValueError("Tolerance must be positive.")
        if N <= 0:
            raise ValueError("max_iter must be a positive integer.")

        steps = []
        x = x0
        x_new = x0

        for i in range(1, N + 1):
            # ── Compute x1 = g(x) ─────────────────────────────────────────
            try:
                x1 = g(x)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero in g({x:.10g}) at iteration {i}, computing x₁.")
            except OverflowError:
                raise ValueError(
                    f"Overflow in g({x:.10g}) at iteration {i}. "
                    "The sequence is diverging — |g'(x)| may be ≥ 1."
                )
            except Exception as e:
                raise ValueError(f"Error evaluating g({x:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(x1):
                raise ValueError(
                    f"g({x:.10g}) = {x1} is not finite at iteration {i}. "
                    "The sequence is diverging."
                )

            # ── Compute x2 = g(x1) ────────────────────────────────────────
            try:
                x2 = g(x1)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero in g({x1:.10g}) at iteration {i}, computing x₂.")
            except OverflowError:
                raise ValueError(
                    f"Overflow in g({x1:.10g}) at iteration {i}, computing x₂. "
                    "The sequence diverged after one step."
                )
            except Exception as e:
                raise ValueError(f"Error evaluating g({x1:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(x2):
                raise ValueError(
                    f"g(x₁) = g({x1:.10g}) = {x2} is not finite at iteration {i}. "
                    "The sequence is diverging."
                )

            # ── Aitken denominator ─────────────────────────────────────────
            denom = x2 - 2 * x1 + x
            if abs(denom) < 1e-15:
                raise ValueError(
                    f"Division by zero at iteration {i}: Δ²x = x₂ - 2x₁ + x = {denom:.2e}. "
                    "The three consecutive iterates are nearly collinear — "
                    "Aitken's acceleration cannot be applied. "
                    "Try a different initial value or use Fixed Point directly."
                )

            x_new = x - ((x1 - x) ** 2) / denom

            if not math.isfinite(x_new):
                raise ValueError(
                    f"x_new = {x_new} is not finite at iteration {i}. "
                    "The acceleration formula produced an undefined result."
                )

            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "aitken",
                "x": x, "x1": x1, "x2": x2, "x_new": x_new, "error": E,
                "description": {"es": f"Iter {i}: x={x:.6f}, x1={x1:.6f}, x2={x2:.6f}, x_new={x_new:.6f}, E={E:.6e}", "en": f"Iter{i}:x={x:.6f}, x1={x1:.6f}, x2={x2:.6f}, x_new={x_new:.6f}, E={E:.6e}"}
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
                    "Try a different initial value or increase max_iter."
                ), "en": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x = {x_new:.10g}. "
                    "Try a different initial value or increase max_iter."
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
