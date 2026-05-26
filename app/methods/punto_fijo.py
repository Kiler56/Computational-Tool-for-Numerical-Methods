"""
Método de Punto Fijo — iteración funcional.
Basado en la implementación de Camilo (metodosCamilo).
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class PuntoFijo(NumericalMethod):

    @property
    def name(self) -> str:
        return "punto_fijo"

    @property
    def description(self) -> dict:
        return {"es": "Punto Fijo", "en": "Fixed Point"}

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
                "<li>Ingrese la función de iteración <code>g(x)</code> (no <code>f(x)</code>).</li>"
                "<li>Se busca un punto fijo donde <code>x = g(x)</code>, lo cual equivale a una raíz de <code>f(x) = x - g(x) = 0</code>.</li>"
                "<li>💡 <strong>Ejemplo:</strong> Para resolver <code>x² - 2 = 0</code>, puede usar <code>g(x) = (x + 2/x)/2</code>.</li>"
                "<li>⚠️ <strong>Requisito:</strong> <code>|g'(x)| &lt; 1</code> en la vecindad de la raíz para garantizar convergencia.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter the iteration function <code>g(x)</code> (not <code>f(x)</code>).</li>"
                "<li>Searches for a fixed point where <code>x = g(x)</code>, equivalent to a root of <code>f(x) = x - g(x) = 0</code>.</li>"
                "<li>💡 <strong>Example:</strong> To solve <code>x² - 2 = 0</code>, use <code>g(x) = (x + 2/x)/2</code>.</li>"
                "<li>⚠️ <strong>Requirement:</strong> <code>|g'(x)| &lt; 1</code> near the root to guarantee convergence.</li>"
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

        # ── Evaluate at x0 to validate ────────────────────────────────────
        try:
            _ = g(x)
        except ZeroDivisionError:
            raise ValueError(
                f"Division by zero in g({x}). "
                "The iteration function is undefined at x₀ — try a different starting value."
            )
        except OverflowError:
            raise ValueError(f"g({x}) desbordamientos. Try a different starting value.")
        except Exception as e:
            raise ValueError(f"Error evaluating g({x}): {e}") from e

        steps = []
        x_new = x

        for i in range(1, N + 1):
            try:
                x_new = g(x)
            except ZeroDivisionError:
                raise ValueError(
                    f"Division by zero in g({x:.10g}) at iteration {i}. "
                    "The iteration function has a singularity at this point."
                )
            except OverflowError:
                raise ValueError(
                    f"Overflow in g({x:.10g}) at iteration {i}. "
                    "The method is diverging — |g'(x)| may be ≥ 1 near the root."
                )
            except Exception as e:
                raise ValueError(f"Error evaluating g({x:.10g}) at iteration {i}: {e}") from e

            if not math.isfinite(x_new):
                raise ValueError(
                    f"g({x:.10g}) = {x_new} is not finite at iteration {i}. "
                    "The method is diverging. Ensure |g'(x)| < 1 near the root, "
                    "or reformulate g(x)."
                )

            E = abs(x_new - x)

            steps.append({
                "step": i, "phase": "fixed_point",
                "x": x, "g_x": x_new, "error": E,
                "description": {"es": f"Iteración {i}: x = {x:.10g}, g(x) = {x_new:.10g}, E = {E:.6e}", "en": f"Iter{i}: x ={x:.10g}, g(x) ={x_new:.10g}, E ={E:.6e}"},
            })

            if E < tol:
                steps[-1]["phase"] = "converged"
                break

            x = x_new
        else:
            steps.append({
                "step": N + 1, "phase": "max_iter_reached",
                "description": {"es": (
                    f"Maximum iterations ({N}) reached without convergence. "
                    f"Last approximation: x = {x_new:.10g}. "
                    "Verify that |g'(x)| < 1 near the root, or choose a better g(x)."
                ), "en": (
                    f"Maximum iterations ({N}) reached without convergence. "
                    f"Last approximation: x = {x_new:.10g}. "
                    "Verify that |g'(x)| < 1 near the root, or choose a better g(x)."
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
