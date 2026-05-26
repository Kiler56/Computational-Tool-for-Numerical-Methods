"""
Bisection — bracketing root finder.
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Bisection(NumericalMethod):

    @property
    def name(self) -> str:
        return "bisection"

    @property
    def description(self) -> dict:
        return {"es": "Bisección", "en": "Bisection"}

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def plot_type(self) -> str:
        return "root_finding"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "a", "label_es": "Punto final izquierdo (a)", "label_en": "Left endpoint (a)", "type": "float", "default": 0},
            {"key": "b", "label_es": "Extremo derecho (b)", "label_en": "Right endpoint (b)", "type": "float", "default": 2},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "iteraciones máximas", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul><li>Ingrese una función <code>f(x)</code> y un intervalo <code>[a, b]</code>.</li><li>⚠️ <strong>Requisito:</strong> <code>f(a)</code> y <code>f(b)</code> deben tener signos opuestos (Bolzano).</li><li>El intervalo se reduce a la mitad en cada iteración hasta que el error esté por debajo de la tolerancia.</li></ul>"
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
        # ── Parse function ────────────────────────────────────────────────
        try:
            f = make_function(expr)
        except Exception as e:
            raise ValueError(f"Invalid expression '{expr}': {e}") from e

        # ── Parse parameters ──────────────────────────────────────────────
        try:
            a = float(params.get("a", 0))
            b = float(params.get("b", 2))
            tol = float(params.get("tol", 1e-7))
            N = int(params.get("max_iter", 100))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid parameter: {e}") from e

        if tol <= 0:
            raise ValueError("Tolerance must be positive.")
        if N <= 0:
            raise ValueError("max_iter must be a positive integer.")
        if a >= b:
            raise ValueError(f"Interval error: a ({a}) must be strictly less than b ({b}).")

        # ── Evaluate endpoints ────────────────────────────────────────────
        try:
            fa = f(a)
            fb = f(b)
        except ZeroDivisionError:
            raise ValueError("f(x) produces a división por cero at one of the endpoints.")
        except OverflowError:
            raise ValueError("f(x) desbordamientos at one of the endpoints — try a smaller interval.")
        except Exception as e:
            raise ValueError(f"Error evaluating f at endpoints: {e}") from e

        if not math.isfinite(fa) or not math.isfinite(fb):
            raise ValueError(
                f"f(a) = {fa} or f(b) = {fb} is not finite (NaN/Inf). "
                "Check your function and interval."
            )
        if fa * fb > 0:
            raise ValueError(
                f"Bolzano condition not met: f({a}) = {fa:.6g} and f({b}) = {fb:.6g} "
                "have the same sign. No sign change in [a, b] — the interval may not contain a root."
            )

        # ── Bisection iterations ──────────────────────────────────────────
        steps = []
        xm = (a + b) / 2
        E = None

        for i in range(1, N + 1):
            try:
                fxm = f(xm)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero evaluating f({xm:.10g}) at iteration {i}.")
            except OverflowError:
                raise ValueError(f"Overflow evaluating f({xm:.10g}) at iteration {i}. The function grows too fast.")
            except Exception as e:
                raise ValueError(f"Error evaluating f({xm:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(fxm):
                raise ValueError(
                    f"f({xm:.10g}) = {fxm} is not finite at iteration {i}. "
                    "The function may have a singularity in this interval."
                )

            step = {
                "step": i,
                "phase": "bisection",
                "a": a, "b": b, "xm": xm,
                "f_xm": fxm,
                "error": E,
                "description": {"es": f"Iteración {i}: xm = {xm:.10g}, f(xm) = {fxm:.6e}" + (f", E = {E:.6e}" if E is not None else ""), "en": f"Iter{i}: xm ={xm:.10g}, f(xm) ={fxm:.6e}" + (f", E = {E:.6e}" if E is not None else "")},
            }
            steps.append(step)

            if fa * fxm < 0:
                b = xm
            else:
                a = xm
                try:
                    fa = f(a)
                except Exception as e:
                    raise ValueError(f"Error re-evaluating f(a) at iteration {i}: {e}") from e

            x_old = xm
            xm = (a + b) / 2
            E = abs(xm - x_old)

            if E < tol:
                try:
                    fxm_final = f(xm)
                except Exception:
                    fxm_final = None
                steps.append({
                    "step": i + 1, "phase": "converged",
                    "description": {"es": f"Convergió: xm = {xm:.10g}, E = {E:.6e}", "en": f"Converged: xm ={xm:.10g}, E ={E:.6e}"},
                    "a": a, "b": b, "xm": xm, "f_xm": fxm_final, "error": E,
                })
                break
        else:
            steps.append({
                "step": N + 1, "phase": "max_iter_reached",
                "description": {"es": (
                    f"Maximum iterations ({N}) reached without convergence. "
                    f"Last approximation: xm = {xm:.10g}, E = {E:.6e}. "
                    "Try increasing max_iter or adjusting the interval."
                ), "en": (
                    f"Maximum iterations ({N}) reached without convergence. "
                    f"Last approximation: xm = {xm:.10g}, E = {E:.6e}. "
                    "Try increasing max_iter or adjusting the interval."
                )},
                "xm": xm, "error": E,
            })

        return {
            "solution": [xm],
            "root": xm,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }
