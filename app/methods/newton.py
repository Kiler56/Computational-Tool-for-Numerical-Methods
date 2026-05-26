"""
Newton–Raphson root finding with a numerical derivative.
"""
import math
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
    def plot_type(self) -> str:
        return "root_convergence"

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
        x_new = x  # Initialize so it's defined if N=0

        for i in range(1, N + 1):
            # ── Evaluate f(x) ─────────────────────────────────────────────
            try:
                fx = f(x)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero in f({x:.10g}) at iteration {i}.")
            except OverflowError:
                raise ValueError(
                    f"Overflow in f({x:.10g}) at iteration {i}. "
                    "The function grows too large — try a closer initial guess."
                )
            except Exception as e:
                raise ValueError(f"Error evaluating f({x:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(fx):
                raise ValueError(
                    f"f({x:.10g}) = {fx} is not finite at iteration {i}. "
                    "The function may have a singularity near x₀."
                )

            # Check if already at root
            if abs(fx) < 1e-15:
                steps.append({
                    "step": i, "phase": "converged",
                    "x": x, "f_x": fx, "df_x": 0.0, "x_new": x, "error": 0.0,
                    "description": {"es": f"Iter {i}: f({x:.10g}) ≈ 0 — exact root found.", "en": f"Iter{i}: f({x:.10g}) ≈ 0 — exact root found."},
                })
                x_new = x
                break

            # ── Evaluate f'(x) numerically ────────────────────────────────
            try:
                dfx = self._numerical_derivative(f, x)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero computing f'({x:.10g}) at iteration {i}.")
            except OverflowError:
                raise ValueError(f"Overflow computing f'({x:.10g}) at iteration {i}.")
            except Exception as e:
                raise ValueError(f"Error computing f'({x:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(dfx):
                raise ValueError(
                    f"f'({x:.10g}) = {dfx} is not finite at iteration {i}. "
                    "The derivative cannot be computed reliably at this point."
                )
            if abs(dfx) < 1e-15:
                raise ValueError(
                    f"Zero derivative at x = {x:.10g} (iteration {i}): f'(x) ≈ {dfx:.2e}. "
                    "Newton-Raphson cannot continue — try a different starting point."
                )

            x_new = x - fx / dfx

            if not math.isfinite(x_new):
                raise ValueError(
                    f"x_new = {x_new} is not finite at iteration {i} "
                    f"(x={x:.10g}, f(x)={fx:.6e}, f'(x)={dfx:.6e}). "
                    "The method is diverging."
                )

            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "newton",
                "x": x, "f_x": fx, "df_x": dfx, "x_new": x_new, "error": E,
                "description": {"es": f"Iter {i}: x = {x:.10g}, f(x) = {fx:.6e}, f'(x) = {dfx:.6e}, x_new = {x_new:.10g}, E = {E:.6e}", "en": f"Iter{i}: x ={x:.10g}, f(x) ={fx:.6e}, f'(x) ={dfx:.6e}, x_new ={x_new:.10g}, E ={E:.6e}"},
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
                "x": x_new,
            })

        return {
            "solution": [x_new],
            "root": x_new,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }
