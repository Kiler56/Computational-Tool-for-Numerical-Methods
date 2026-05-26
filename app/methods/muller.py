"""
Método de Müller — Encuentra raíces interpolando una parábola por 3 puntos.
Puede encontrar raíces complejas, aunque aquí limitaremos a reales por UI.
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Muller(NumericalMethod):

    @property
    def name(self) -> str:
        return "muller"

    @property
    def description(self) -> dict:
        return {"es": "Müller", "en": "Müller"}

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def plot_type(self) -> str:
        return "root_convergence"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "x₀", "label_en": "x₀", "type": "float", "default": 0.0},
            {"key": "x1", "label_es": "x₁", "label_en": "x₁", "type": "float", "default": 0.5},
            {"key": "x2", "label_es": "x₂", "label_en": "x₂", "type": "float", "default": 1.0},
            {"key": "tol", "label_es": "tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y tres aproximaciones iniciales <code>x₀, x₁, x₂</code>.</li>"
                "<li>Interpola un polinomio cuadrático y saca la raíz más cercana a x₂.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and three initial approximations <code>x₀, x₁, x₂</code>.</li>"
                "<li>Interpolates a quadratic polynomial and finds the root closest to x₂.</li>"
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
            x0 = float(params.get("x0", 0.0))
            x1 = float(params.get("x1", 0.5))
            x2 = float(params.get("x2", 1.0))
            tol = float(params.get("tol", 1e-7))
            N = int(params.get("max_iter", 100))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid parameter: {e}") from e

        if tol <= 0:
            raise ValueError("Tolerance must be positive.")
        if N <= 0:
            raise ValueError("max_iter must be a positive integer.")

        # Check that initial points are distinct
        if abs(x1 - x0) < 1e-14:
            raise ValueError(f"x₀ ({x0}) and x₁ ({x1}) are too close or identical. All three points must be distinct.")
        if abs(x2 - x1) < 1e-14:
            raise ValueError(f"x₁ ({x1}) and x₂ ({x2}) are too close or identical. All three points must be distinct.")
        if abs(x2 - x0) < 1e-14:
            raise ValueError(f"x₀ ({x0}) and x₂ ({x2}) are too close or identical. All three points must be distinct.")

        # ── Evaluate initial points ────────────────────────────────────────
        try:
            _ = f(x0), f(x1), f(x2)
        except ZeroDivisionError:
            raise ValueError("Division by zero evaluating f at the initial points.")
        except OverflowError:
            raise ValueError("f overflows at one of the initial points — try different starting values.")
        except Exception as e:
            raise ValueError(f"Error evaluating f at initial points: {e}") from e

        steps = []
        x3 = x2

        for i in range(1, N + 1):
            # ── Evaluate f at current triple ──────────────────────────────
            try:
                f0, f1, f2 = f(x0), f(x1), f(x2)
            except ZeroDivisionError:
                raise ValueError(f"Division by zero evaluating f at iteration {i}.")
            except OverflowError:
                raise ValueError(f"Overflow evaluating f at iteration {i}.")
            except Exception as e:
                raise ValueError(f"Error evaluating f at iteration {i}: {e}") from e

            for val, name in [(f0, "f(x₀)"), (f1, "f(x₁)"), (f2, "f(x₂)")]:
                if not math.isfinite(val):
                    raise ValueError(f"{name} = {val} is not finite at iteration {i}.")

            h1 = x1 - x0
            h2 = x2 - x1

            if abs(h1) < 1e-14 or abs(h2) < 1e-14:
                raise ValueError(
                    f"Points coincide at iteration {i}: h1={h1:.2e}, h2={h2:.2e}. "
                    "Cannot construct the parabola — points collapsed to the same value."
                )

            d1 = (f1 - f0) / h1
            d2 = (f2 - f1) / h2
            denom_d = h2 + h1
            if abs(denom_d) < 1e-14:
                raise ValueError(f"h₁ + h₂ ≈ 0 at iteration {i}. Cannot build divided difference.")

            d = (d2 - d1) / denom_d
            b = d2 + h2 * d

            # ── Discriminant ──────────────────────────────────────────────
            disc = b**2 - 4 * f2 * d

            if disc < 0:
                raise ValueError(
                    f"Negative discriminant at iteration {i}: disc = {disc:.6g}. "
                    "Müller's method would produce complex roots with the current triple. "
                    "This interface is limited to real roots — try different initial points "
                    "closer to a real root of f."
                )

            sqrt_disc = math.sqrt(disc)

            # ── Denominator: pick the larger magnitude ────────────────────
            E_plus = b + sqrt_disc
            E_minus = b - sqrt_disc
            denom_E = E_plus if abs(E_plus) > abs(E_minus) else E_minus

            if abs(denom_E) < 1e-15:
                raise ValueError(
                    f"Zero denominator at iteration {i}: both (b ± √disc) ≈ 0. "
                    "The quadratic term d ≈ 0 — the three points may be nearly collinear. "
                    "Try more spread-out initial points."
                )

            h = -2 * f2 / denom_E
            x3 = x2 + h
            err = abs(x3 - x2)

            if not math.isfinite(x3):
                raise ValueError(
                    f"x_new = {x3} is not finite at iteration {i}. "
                    "The method is diverging — choose initial points closer to the root."
                )

            steps.append({
                "step": i, "phase": "muller",
                "x_new": x3, "error": err,
                "description": {"es": f"Iter {i}: x_new={x3:.6f}, E={err:.6e}", "en": f"Iter{i}: x_new={x3:.6f}, E={err:.6e}"}
            })

            if err < tol:
                steps[-1]["phase"] = "converged"
                break

            x0, x1, x2 = x1, x2, x3
        else:
            steps.append({
                "step": N + 1, "phase": "max_iter_reached",
                "description": {"es": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x = {x3:.10g}. "
                    "Try different initial points or increase max_iter."
                ), "en": (
                    f"Maximum iterations ({N}) reached. "
                    f"Last approximation: x = {x3:.10g}. "
                    "Try different initial points or increase max_iter."
                )},
            })

        return {
            "solution": [x3],
            "root": x3,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }
