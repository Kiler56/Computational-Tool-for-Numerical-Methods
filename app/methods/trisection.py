"""
Trisección — búsqueda de raíces dividiendo el intervalo en 3.
Basado en la implementación de Jul (MetodosJul).
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Trisection(NumericalMethod):

    @property
    def name(self) -> str:
        return "trisection"

    @property
    def description(self) -> dict:
        return {"es": "Trisección", "en": "Trisection"}

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
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y un intervalo <code>[a, b]</code>.</li>"
                "<li>Divide el intervalo en tres partes iguales en cada iteración y selecciona el subintervalo que contiene la raíz.</li>"
                "<li>⚠️ <strong>Requisito:</strong> Debe existir un cambio de signo en <code>[a, b]</code>.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and an interval <code>[a, b]</code>.</li>"
                "<li>Divides the interval into three equal parts each iteration and selects the sub-interval containing the root.</li>"
                "<li>⚠️ <strong>Requirement:</strong> A sign change must exist in <code>[a, b]</code>.</li>"
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

        # ── Validate sign change ──────────────────────────────────────────
        try:
            fa = f(a)
            fb = f(b)
        except ZeroDivisionError:
            raise ValueError("Division by zero evaluating f at an endpoint.")
        except OverflowError:
            raise ValueError("f overflows at an endpoint — try a smaller interval.")
        except Exception as e:
            raise ValueError(f"Error evaluating f at endpoints: {e}") from e

        if not math.isfinite(fa) or not math.isfinite(fb):
            raise ValueError(
                f"f(a) = {fa} or f(b) = {fb} is not finite. "
                "Choose an interval where f is well-defined."
            )
        if fa * fb > 0:
            raise ValueError(
                f"No sign change: f({a}) = {fa:.6g} and f({b}) = {fb:.6g} have the same sign. "
                "Trisection requires f(a) · f(b) < 0."
            )

        steps = []
        E = None

        for i in range(1, N + 1):
            x1 = a + (b - a) / 3
            x2 = b - (b - a) / 3

            try:
                fx1 = f(x1)
                fx2 = f(x2)
                fa_cur = f(a)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero evaluating f at the trisection points at iteration {i}.")
            except OverflowError:
                raise ValueError(f"Overflow evaluating f at iteration {i}. The interval may need to be smaller.")
            except Exception as e:
                raise ValueError(f"Error evaluating f at iteration {i}: {e}") from e

            for val, label in [(fx1, f"f(x₁={x1:.6g})"), (fx2, f"f(x₂={x2:.6g})")]:
                if not math.isfinite(val):
                    raise ValueError(
                        f"{label} = {val} is not finite at iteration {i}. "
                        "The function has a singularity in this interval."
                    )

            steps.append({
                "step": i, "phase": "trisection",
                "a": a, "b": b, "x1": x1, "x2": x2,
                "f_x1": fx1, "f_x2": fx2, "error": E,
                "description": f"Iter {i}: a={a:.8g}, x1={x1:.8g}, x2={x2:.8g}, b={b:.8g}" + (f", E={E:.6e}" if E else ""),
            })

            if fa_cur * fx1 < 0:
                b = x1
            elif fx1 * fx2 < 0:
                a = x1
                b = x2
            else:
                a = x2

            E = abs(b - a)
            if E < tol:
                break

        xm = (a + b) / 2
        try:
            fxm = f(xm)
        except Exception:
            fxm = None

        steps.append({
            "step": len(steps) + 1, "phase": "converged",
            "description": f"Converged: root ≈ {xm:.10g}, E = {E:.6e}",
            "a": a, "b": b, "xm": xm, "f_xm": fxm, "error": E,
        })

        return {
            "solution": [xm],
            "root": xm,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }
