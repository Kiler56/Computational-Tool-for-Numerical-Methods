"""
Método del Trapecio Compuesto — Integración Numérica
=====================================================
Aproxima la integral definida ∫_a^b f(x) dx usando n subintervalos
con la regla compuesta del trapecio.

Fórmula compuesta:
    h = (b - a) / n
    I ≈ (h/2) · [f(x_0) + 2·f(x_1) + 2·f(x_2) + … + 2·f(x_{n-1}) + f(x_n)]

El patrón de coeficientes es: 1, 2, 2, …, 2, 1
Error de truncamiento global: O(h²).

Implementado por: Jul (MetodosJul) — adaptado e integrado a la arquitectura
                  modular por el equipo de despliegue (rama main).
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function
import math


class CompositeTrapezoidal(NumericalMethod):

    # ── Metadatos ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "composite_trapezoidal"

    @property
    def description(self) -> dict:
        return {
            "es": "Trapecio Compuesto (Integración Numérica)",
            "en": "Composite Trapezoidal (Numerical Integration)",
        }

    @property
    def plot_type(self) -> str:
        return "integration"

    @property
    def method_type(self) -> str:
        return "root"   # Reutiliza el flujo "root" (expr + params)

    @property
    def params_schema(self) -> list:
        return [
            {
                "key": "a",
                "label_es": "Límite inferior a",
                "label_en": "Lower limit a",
                "type": "float",
                "default": 0,
            },
            {
                "key": "b",
                "label_es": "Límite superior b",
                "label_en": "Upper limit b",
                "type": "float",
                "default": 1,
            },
            {
                "key": "n",
                "label_es": "Número de subintervalos n",
                "label_en": "Number of subintervals n",
                "type": "int",
                "default": 4,
            },
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese la función <code>f(x)</code> a integrar.</li>"
                "<li>Defina el intervalo <code>[a, b]</code> y el número de subintervalos <code>n</code>.</li>"
                "<li>⚠️ <strong>n debe ser ≥ 1</strong>. Cualquier valor menor se ajusta automáticamente a 1.</li>"
                "<li>La regla compuesta aplica la fórmula del trapecio en cada subintervalo consecutivo.</li>"
                "<li>Fórmula: I ≈ (h/2)·[f(x₀) + 2f(x₁) + 2f(x₂) + … + 2f(xₙ₋₁) + f(xₙ)]</li>"
                "<li>💡 Error de truncamiento global: O(h²). A mayor <em>n</em>, mayor precisión.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter the function <code>f(x)</code> to integrate.</li>"
                "<li>Set the interval <code>[a, b]</code> and the number of subintervals <code>n</code>.</li>"
                "<li>⚠️ <strong>n must be ≥ 1</strong>. Values smaller than 1 are automatically set to 1.</li>"
                "<li>The composite rule applies the trapezoidal formula over each consecutive subinterval.</li>"
                "<li>Formula: I ≈ (h/2)·[f(x₀) + 2f(x₁) + 2f(x₂) + … + 2f(xₙ₋₁) + f(xₙ)]</li>"
                "<li>💡 Global truncation error: O(h²). A larger <em>n</em> gives higher accuracy.</li>"
                "</ul>"
            ),
        }

    # ── Kernel numérico ───────────────────────────────────────────────────────

    @staticmethod
    def _coefficient(i: int, n: int) -> int:
        """Coeficiente de cada nodo en la suma del trapecio compuesto.
        Patrón: 1 en los extremos, 2 en los nodos interiores.
        """
        if i == 0 or i == n:
            return 1
        return 2

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        a = float(params.get("a", 0))
        b = float(params.get("b", 1))
        n = int(params.get("n", 4))

        # ── Validaciones ──────────────────────────────────────────────────────
        if a >= b:
            raise ValueError(
                "El límite inferior a debe ser estrictamente menor que el límite superior b."
            )
        if n < 1:
            n = 1

        steps = []
        h = (b - a) / n

        # ── Paso 1: Configuración ─────────────────────────────────────────────
        steps.append({
            "step": 1,
            "phase": "setup",
            "description": (
                f"Configuración: a={a}, b={b}, n={n}, "
                f"h=(b-a)/n=({b}-{a})/{n}={h:.8g}"
            ),
            "a": a, "b": b, "n": n, "h": h,
        })

        # ── Paso 2: Evaluación de los nodos ───────────────────────────────────
        nodes = [a + i * h for i in range(n + 1)]
        f_vals = []
        coefs = []
        panels = []  # Para la graficadora universal

        for i, xi in enumerate(nodes):
            try:
                fxi = f(xi)
            except ZeroDivisionError:
                raise ValueError(
                    f"División por cero evaluando f({xi:.10g}) en el nodo x_{i}."
                )
            except OverflowError:
                raise ValueError(
                    f"Desbordamiento evaluando f({xi:.10g}) en el nodo x_{i}."
                )
            except Exception as e:
                raise ValueError(
                    f"Error evaluando f({xi:.10g}) en el nodo x_{i}: {e}"
                ) from e

            if not math.isfinite(fxi):
                raise ValueError(
                    f"f({xi:.10g}) no es un valor finito (NaN/Inf). "
                    "Puede haber una asíntota vertical en el intervalo."
                )

            ci = self._coefficient(i, n)
            f_vals.append(fxi)
            coefs.append(ci)
            steps.append({
                "step": len(steps) + 1,
                "phase": "evaluation",
                "description": (
                    f"x_{i} = {xi:.8g}, f(x_{i}) = {fxi:.10g}, "
                    f"coeficiente = {ci}"
                ),
                "index": i,
                "x": xi,
                "f_x": fxi,
                "coefficient": ci,
            })

        # Armar paneles individuales para la graficadora (shaded trapezoids)
        for i in range(n):
            xa, xb = nodes[i], nodes[i + 1]
            ya, yb = f_vals[i], f_vals[i + 1]
            panel_area = h * (ya + yb) / 2.0
            panels.append({"a": xa, "b": xb, "area": panel_area})

        # ── Paso 3: Suma ponderada ────────────────────────────────────────────
        weighted_sum = sum(ci * fxi for ci, fxi in zip(coefs, f_vals))
        steps.append({
            "step": len(steps) + 1,
            "phase": "weighted_sum",
            "description": (
                f"Suma ponderada Σ(c_i · f(x_i)) = {weighted_sum:.10g}  "
                f"con patrón de coeficientes [1, 2, 2, …, 2, 1]"
            ),
            "weighted_sum": weighted_sum,
            "coefficients_pattern": coefs,
        })

        # ── Paso 4: Integral ──────────────────────────────────────────────────
        integral = (h / 2) * weighted_sum
        steps.append({
            "step": len(steps) + 1,
            "phase": "result",
            "description": (
                f"Integral ≈ (h/2) · suma = ({h:.8g}/2) · {weighted_sum:.10g} "
                f"= {integral:.10g}"
            ),
            "factor": h / 2,
            "integral": integral,
        })

        # ── Paso 5: Estimación del error (extrapolación de Richardson) ────────
        # Refinamos con 2n subintervalos y aplicamos Richardson O(h²):
        # E ≈ |I_{2n} - I_n| / 3
        n_ref = n * 2
        h_ref = (b - a) / n_ref
        nodes_ref = [a + i * h_ref for i in range(n_ref + 1)]
        try:
            f_ref = [f(xi) for xi in nodes_ref]
            coefs_ref = [self._coefficient(i, n_ref) for i in range(n_ref + 1)]
            integral_ref = (h_ref / 2) * sum(
                c * fv for c, fv in zip(coefs_ref, f_ref)
            )
            error_est = abs(integral_ref - integral) / 3.0
        except Exception:
            integral_ref = None
            error_est = None

        if error_est is not None:
            steps.append({
                "step": len(steps) + 1,
                "phase": "error_estimation",
                "description": (
                    f"Estimación de error (extrapolación de Richardson con n_ref={n_ref}): "
                    f"I_ref = {integral_ref:.10g}, error estimado ≈ {error_est:.2e}"
                ),
                "n_ref": n_ref,
                "integral_ref": integral_ref,
                "error_estimate": error_est,
            })

        # ── Propiedades para la UI ────────────────────────────────────────────
        props = {
            "Integral aproximada": f"{integral:.10g}",
            "Subintervalos usados (n)": str(n),
            "Paso h": f"{h:.8g}",
            "Fórmula": "I ≈ (h/2)·[f(x₀) + 2f(x₁) + 2f(x₂) + … + 2f(xₙ₋₁) + f(xₙ)]",
        }
        if error_est is not None:
            props["Error estimado (Richardson)"] = f"{error_est:.2e}"

        return {
            "solution": [integral],
            "root": integral,       # alias para compatibilidad con flujo "root"
            "properties": props,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
            # Claves que necesita _render_integration en universal_plotter:
            "a": a,
            "b": b,
            "integral": integral,
            "panels": panels,
        }
