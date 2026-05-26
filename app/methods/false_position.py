"""
Posición Falsa (Regula Falsi) — búsqueda de raíces.
Basado en la implementación de Jul (MetodosJul).
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class FalsePosition(NumericalMethod):

    @property
    def name(self) -> str:
        return "false_position"

    @property
    def description(self) -> dict:
        return {"es": "Posición Falsa (Regula Falsi)", "en": "False Position (Regula Falsi)"}

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def plot_type(self) -> str:
        return "root_finding"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "a", "label_es": "Extremo izquierdo (a)", "label_en": "Left endpoint (a)", "type": "float", "default": 0},
            {"key": "b", "label_es": "Extremo derecho (b)", "label_en": "Right endpoint (b)", "type": "float", "default": 2},
            {"key": "tol", "label_es": "tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
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
            raise ValueError("f(x) produces a division by zero at one of the endpoints.")
        except OverflowError:
            raise ValueError("f(x) overflows at one of the endpoints — try a smaller interval.")
        except Exception as e:
            raise ValueError(f"Error evaluating f at endpoints: {e}") from e

        if not math.isfinite(fa) or not math.isfinite(fb):
            raise ValueError(
                f"f(a) = {fa} or f(b) = {fb} is not finite. Check your function and interval."
            )
        if fa * fb > 0:
            raise ValueError(
                f"Bolzano condition not met: f({a}) = {fa:.6g} and f({b}) = {fb:.6g} "
                "have the same sign — no guaranteed root in [a, b]."
            )

        # ── Check denominator for first step ─────────────────────────────
        if abs(fb - fa) < 1e-15:
            raise ValueError(
                f"f(a) ≈ f(b) ≈ {fa:.6g}. The secant line is nearly horizontal — "
                "cannot compute the False Position point."
            )

        xm = (fb * a - fa * b) / (fb - fa)
        steps = []
        E = None

        for i in range(1, N + 1):
            try:
                fxm = f(xm)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero evaluating f({xm:.10g}) at iteration {i}.")
            except OverflowError:
                raise ValueError(f"Overflow evaluating f({xm:.10g}) at iteration {i}.")
            except Exception as e:
                raise ValueError(f"Error evaluating f({xm:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(fxm):
                raise ValueError(
                    f"f({xm:.10g}) = {fxm} is not finite at iteration {i}. "
                    "The function may have a singularity."
                )

            steps.append({
                "step": i, "phase": "false_position",
                "a": a, "b": b, "xm": xm, "f_xm": fxm, "error": E,
                "description": {"es": f"Iter {i}: xm = {xm:.10g}, f(xm) = {fxm:.6e}" + (f", E = {E:.6e}" if E is not None else ""), "en": f"Iter{i}: xm ={xm:.10g}, f(xm) ={fxm:.6e}" + (f", E = {E:.6e}" if E is not None else "")},
            })

            if fa * fxm < 0:
                b = xm
                try:
                    fb = f(b)
                except Exception as e:
                    raise ValueError(f"Error re-evaluating f(b) at iteration {i}: {e}") from e
            else:
                a = xm
                try:
                    fa = f(a)
                except Exception as e:
                    raise ValueError(f"Error re-evaluating f(a) at iteration {i}: {e}") from e

            x_old = xm
            denom = fb - fa
            if abs(denom) < 1e-15:
                raise ValueError(
                    f"Division by zero at iteration {i}: f(b) - f(a) ≈ 0. "
                    "The method has stagnated — the interval may be too small or f is nearly flat."
                )
            xm = (fb * a - fa * b) / denom
            E = abs(xm - x_old)

            if E < tol:
                steps.append({
                    "step": i + 1, "phase": "converged",
                    "description": {"es": f"Converged: xm = {xm:.10g}, E = {E:.6e}", "en": f"Converged: xm ={xm:.10g}, E ={E:.6e}"},
                    "a": a, "b": b, "xm": xm, "f_xm": f(xm), "error": E,
                })
                break
        else:
            steps.append({
                "step": N + 1, "phase": "max_iter_reached",
                "description": {"es": (
                    f"Maximum iterations ({N}) reached. Last xm = {xm:.10g}, E = {E:.6e}. "
                    "Try increasing max_iter or tightening the initial interval."
                ), "en": (
                    f"Maximum iterations ({N}) reached. Last xm = {xm:.10g}, E = {E:.6e}. "
                    "Try increasing max_iter or tightening the initial interval."
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
