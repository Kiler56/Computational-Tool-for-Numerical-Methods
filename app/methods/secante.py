"""
Método de la Secante — búsqueda de raíces sin derivada.
Implementado desde el pseudocódigo de Camilo (metodosCamilo).
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Secante(NumericalMethod):

    @property
    def name(self) -> str:
        return "secante"

    @property
    def description(self) -> dict:
        return {"es": "Secante", "en": "Secant Method"}

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def plot_type(self) -> str:
        return "root_convergence"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "x₀ (primer punto)", "label_en": "x₀ (first point)", "type": "float", "default": 0},
            {"key": "x1", "label_es": "x₁ (segundo punto)", "label_en": "x₁ (second point)", "type": "float", "default": 2},
            {"key": "tol", "label_es": "tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y dos puntos iniciales <code>x₀</code> y <code>x₁</code>.</li>"
                "<li>Usa la recta secante entre los dos últimos puntos para estimar la raíz, sin necesitar la derivada.</li>"
                "<li>💡 <strong>Ventaja:</strong> No requiere calcular derivadas (más rápido por iteración que Newton).</li>"
                "<li>⚠️ Puede no converger si los puntos iniciales están mal elegidos.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and two initial points <code>x₀</code> and <code>x₁</code>.</li>"
                "<li>Uses the secant line between the last two points to estimate the root, without computing derivatives.</li>"
                "<li>💡 <strong>Advantage:</strong> No derivative computation needed (faster per iteration than Newton).</li>"
                "<li>⚠️ May not converge if the initial points are poorly chosen.</li>"
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
            x0 = float(params.get("x0", 0))
            x1 = float(params.get("x1", 2))
            tol = float(params.get("tol", 1e-7))
            N = int(params.get("max_iter", 100))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid parameter: {e}") from e

        if tol <= 0:
            raise ValueError("Tolerance must be positive.")
        if N <= 0:
            raise ValueError("max_iter must be a positive integer.")
        if abs(x1 - x0) < 1e-15:
            raise ValueError(
                f"x₀ ({x0}) and x₁ ({x1}) are identical or too close. "
                "The Secant method requires two distinct initial points."
            )

        # ── Evaluate initial points ────────────────────────────────────────
        try:
            f0 = f(x0)
            f1 = f(x1)
        except ZeroDivisionError:
            raise ValueError("Division by zero evaluating f at the initial points.")
        except OverflowError:
            raise ValueError("f overflows at the initial points — try different starting values.")
        except Exception as e:
            raise ValueError(f"Error evaluating f at initial points: {e}") from e

        if not math.isfinite(f0) or not math.isfinite(f1):
            raise ValueError(
                f"f(x₀) = {f0} or f(x₁) = {f1} is not finite. "
                "Choose initial points where f is well-defined."
            )

        steps = []
        x2 = x1  # Initialize

        for i in range(1, N + 1):
            denom = f1 - f0
            if abs(denom) < 1e-15:
                raise ValueError(
                    f"Division by zero at iteration {i}: f(x₁) - f(x₀) ≈ {denom:.2e}. "
                    "The secant line is nearly horizontal — the method has stagnated. "
                    "Try different initial points."
                )

            x2 = x1 - f1 * (x1 - x0) / denom

            if not math.isfinite(x2):
                raise ValueError(
                    f"x₂ = {x2} is not finite at iteration {i}. "
                    "The method is diverging — choose initial points closer to the root."
                )

            E = abs(x2 - x1)

            steps.append({
                "step": i, "phase": "secante",
                "x0": x0, "x1": x1, "x2": x2,
                "f_x0": f0, "f_x1": f1, "error": E,
                "description": {"es": f"Iter {i}: x0={x0:.8g}, x1={x1:.8g}, x2={x2:.10g}, E = {E:.6e}", "en": f"Iter{i}: x0={x0:.8g}, x1={x1:.8g}, x2={x2:.10g}, E ={E:.6e}"},
            })

            if E < tol:
                steps[-1]["phase"] = "converged"
                break

            x0, f0 = x1, f1
            x1 = x2
            try:
                f1 = f(x1)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero evaluating f({x1:.10g}) at iteration {i+1}.")
            except OverflowError:
                raise ValueError(
                    f"Overflow evaluating f({x1:.10g}) at iteration {i+1}. "
                    "The method may be diverging."
                )
            except Exception as e:
                raise ValueError(f"Error evaluating f({x1:.10g}) at iteration {i+1}: {e}") from e

            if not math.isfinite(f1):
                raise ValueError(
                    f"f({x1:.10g}) = {f1} is not finite at iteration {i+1}. "
                    "The function has a singularity near this point."
                )
        else:
            steps.append({
                "step": N + 1, "phase": "max_iter_reached",
                "description": {"es": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x₂ = {x2:.10g}. "
                    "Try different initial points or increase max_iter."
                ), "en": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x₂ = {x2:.10g}. "
                    "Try different initial points or increase max_iter."
                )},
                "x2": x2,
            })

        return {
            "solution": [x2],
            "root": x2,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }
