"""
Búsqueda Incremental — localización de intervalos con raíz.
Basado en la implementación de Jul (MetodosJul).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class IncrementalSearch(NumericalMethod):

    @property
    def name(self) -> str:
        return "incremental_search"

    @property
    def description(self) -> str:
        return "Búsqueda Incremental"

    @property
    def method_type(self) -> str:
        return "root"

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
        f = make_function(expr)
        x0 = float(params.get("x0", -3))
        h = float(params.get("h", 0.5))
        N = int(params.get("max_iter", 100))

        x_prev = x0
        f_prev = f(x_prev)
        steps = []
        found_intervals = []

        for i in range(1, N + 1):
            x_curr = x_prev + h
            f_curr = f(x_curr)

            step = {
                "step": i, "phase": "search",
                "x_prev": x_prev, "x_curr": x_curr,
                "f_prev": f_prev, "f_curr": f_curr,
                "description": f"Iter {i}: [{x_prev:.6g}, {x_curr:.6g}], f = [{f_prev:.6e}, {f_curr:.6e}]",
            }

            if f_prev * f_curr < 0:
                step["phase"] = "root_found"
                step["description"] += f" ← Raíz en [{x_prev:.6g}, {x_curr:.6g}]"
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
            }
        else:
            raise ValueError("No se encontró ningún intervalo con cambio de signo en el rango explorado.")
