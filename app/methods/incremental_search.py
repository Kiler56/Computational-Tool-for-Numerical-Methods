"""
Búsqueda Incremental — localización de intervalos con cambio de signo.
"""
import math
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class IncrementalSearch(NumericalMethod):

    @property
    def name(self) -> str:
        return "incremental_search"

    @property
    def description(self) -> dict:
        return {"es": "Búsqueda Incremental", "en": "Incremental Search"}

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def plot_type(self) -> str:
        return "incremental"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "Valor inicial (x₀)", "label_en": "Initial value (x₀)", "type": "float", "default": -3},
            {"key": "h", "label_es": "Paso (h)", "label_en": "Step size (h)", "type": "float", "default": 0.5},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code>, un punto de inicio <code>x₀</code> y un paso <code>h</code>.</li>"
                "<li>El método avanza con paso fijo buscando intervalos donde <code>f</code> cambia de signo.</li>"
                "<li>💡 <strong>Nota:</strong> Este método no da la raíz exacta, sino el intervalo que la contiene. Úselo como paso previo a Bisección o Posición Falsa.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code>, a starting point <code>x₀</code> and a step size <code>h</code>.</li>"
                "<li>The method advances with a fixed step searching for intervals where <code>f</code> changes sign.</li>"
                "<li>💡 <strong>Note:</strong> This method does not return the exact root, but the interval containing it. Use it as a preliminary step before Bisection or False Position.</li>"
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
            x0 = float(params.get("x0", -3))
            h = float(params.get("h", 0.5))
            N = int(params.get("max_iter", 100))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid parameter: {e}") from e

        if h == 0:
            raise ValueError("Step size h cannot be zero.")
        if N <= 0:
            raise ValueError("max_iter must be a positive integer.")

        # ── Evaluate starting point ───────────────────────────────────────
        try:
            f_prev = f(x0)
        except ZeroDivisionError:
            raise ValueError(f"Division by zero evaluating f({x0}). Try a different starting point.")
        except OverflowError:
            raise ValueError(f"f({x0}) desbordamientos. Try a different starting point.")
        except Exception as e:
            raise ValueError(f"Error evaluating f({x0}): {e}") from e

        if not math.isfinite(f_prev):
            raise ValueError(
                f"f({x0}) = {f_prev} is not finite. The function may have a singularity at x₀."
            )

        x_prev = x0
        steps = []
        found_intervals = []

        for i in range(1, N + 1):
            x_curr = x_prev + h

            try:
                f_curr = f(x_curr)
            except ZeroDivisionError:
                steps.append({
                    "step": i, "phase": "singularity",
                    "x_prev": x_prev, "x_curr": x_curr,
                    "f_prev": f_prev, "f_curr": None,
                    "description": {"es": f"Iteración {i}: [{x_prev:.6g}, {x_curr:.6g}] — división por cero en x={x_curr:.6g}, saltando.", "en": f"Iter{i}:[{x_prev:.6g},{x_curr:.6g}] — división por cero at x={x_curr:.6g}, saltando."},
                })
                x_prev = x_curr
                f_prev = float("nan")
                continue
            except OverflowError:
                steps.append({
                    "step": i, "phase": "desbordamiento",
                    "x_prev": x_prev, "x_curr": x_curr,
                    "description": {"es": f"Iteración {i}: desbordamiento en x={x_curr:.6g}, saltando.", "en": f"Iter{i}: desbordamiento at x={x_curr:.6g}, saltando."},
                })
                x_prev = x_curr
                f_prev = float("nan")
                continue
            except Exception as e:
                raise ValueError(f"Error evaluating f({x_curr:.6g}) at iteration {i}: {e}") from e

            step = {
                "step": i, "phase": "search",
                "x_prev": x_prev, "x_curr": x_curr,
                "f_prev": f_prev, "f_curr": f_curr,
                "description": {"es": f"Iteración {i}: [{x_prev:.6g}, {x_curr:.6g}], f = [{f_prev:.6e}, {f_curr:.6e}]", "en": f"Iter{i}:[{x_prev:.6g},{x_curr:.6g}], f = [{f_prev:.6e},{f_curr:.6e}]"},
            }

            if math.isfinite(f_prev) and math.isfinite(f_curr) and f_prev * f_curr < 0:
                step["phase"] = "root_found"
                step["description"]["es"] += f" ← Intervalo raíz [{x_prev:.6g}, {x_curr:.6g}]"
                step["description"]["en"] += f" ← Root bracket [{x_prev:.6g}, {x_curr:.6g}]"
                found_intervals.append([x_prev, x_curr])

            steps.append(step)
            x_prev = x_curr
            f_prev = f_curr

        if found_intervals:
            midpoint = (found_intervals[0][0] + found_intervals[0][1]) / 2
            return {
                "solution": [midpoint],
                "root": midpoint,
                "intervals": found_intervals,
                "steps": steps,
                "iterations": len(steps),
                "method": self.name,
                "plot_type": self.plot_type,
            }
        else:
            raise ValueError(
                f"No sign-change bracket was found in [{x0}, {x0 + N * h:.6g}] "
                f"with step h = {h}. "
                "Try a wider range (larger N or smaller |h|), or a different starting point."
            )
