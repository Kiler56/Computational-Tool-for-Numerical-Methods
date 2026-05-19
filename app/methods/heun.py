"""
Heun's method (improved Euler / explicit trapezoidal rule) for ODEs.

Problem:  y' = f(t, y),   y(t0) = y0,   t in [t0, tf]

Per step:
    k1 = f(t_n, y_n)
    k2 = f(t_n + h, y_n + h*k1)
    y_{n+1} = y_n + (h/2)*(k1 + k2)

Local truncation error: O(h^3). Global error: O(h^2).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_ode_function


class HeunMethod(NumericalMethod):

    @property
    def name(self) -> str:
        return "heun"

    @property
    def description(self) -> str:
        return "Heun's Method (ODEs)"

    @property
    def method_type(self) -> str:
        return "ode"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "t0", "label_es": "Tiempo inicial (t0)", "label_en": "Initial time (t0)", "type": "float", "default": 0.0},
            {"key": "y0", "label_es": "Valor inicial (y0)", "label_en": "Initial value (y0)", "type": "float", "default": 0.5},
            {"key": "tf", "label_es": "Tiempo final (tf)", "label_en": "Final time (tf)", "type": "float", "default": 1.0},
            {"key": "h", "label_es": "Tamaño de paso (h)", "label_en": "Step size (h)", "type": "float", "default": 0.25},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(t, y)</code> para <code>y' = f(t, y)</code>.</li>"
                "<li>Heun usa un predictor-corrector: promedio de pendientes en <code>(t_n, y_n)</code> "
                "y <code>(t_n+h, y_n+h·f(t_n,y_n))</code>.</li>"
                "<li>Orden global O(h²), más preciso que Euler con el mismo <code>h</code>.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(t, y)</code> for <code>y' = f(t, y)</code>.</li>"
                "<li>Heun is a predictor-corrector: average slopes at <code>(t_n, y_n)</code> "
                "and <code>(t_n+h, y_n+h·f(t_n,y_n))</code>.</li>"
                "<li>Global order O(h²), more accurate than Euler for the same <code>h</code>.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        f = make_ode_function(expr)
        t0 = float(params.get("t0", 0.0))
        y0 = float(params.get("y0", 0.5))
        tf = float(params.get("tf", 1.0))
        h = float(params.get("h", 0.25))

        if h <= 0:
            raise ValueError("Step size h must be positive.")
        if tf < t0:
            raise ValueError("Final time tf must be >= initial time t0.")

        steps = []
        t_vals = [t0]
        y_vals = [y0]
        t, y = t0, y0
        n = 0

        while t < tf - 1e-15:
            h_eff = min(h, tf - t)
            k1 = f(t, y)
            k2 = f(t + h_eff, y + h_eff * k1)
            y_new = y + (h_eff / 2.0) * (k1 + k2)
            t_new = t + h_eff

            steps.append({
                "step": n + 1,
                "phase": "heun",
                "t": t,
                "y": y,
                "k1": k1,
                "k2": k2,
                "h": h_eff,
                "y_new": y_new,
                "t_new": t_new,
                "description": (
                    f"Step {n + 1}: t = {t:.8g}, y = {y:.8g}, "
                    f"k1 = {k1:.6e}, k2 = {k2:.6e}, y_new = {y_new:.8g}"
                ),
            })

            t, y = t_new, y_new
            n += 1
            t_vals.append(t)
            y_vals.append(y)

        return {
            "solution": [[ti, yi] for ti, yi in zip(t_vals, y_vals)],
            "t_values": t_vals,
            "y_values": y_vals,
            "final_t": t,
            "final_y": y,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
