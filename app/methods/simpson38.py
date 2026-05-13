"""
Método de Simpson 3/8 — Integración Numérica
=============================================
Aproxima la integral definida ∫_a^b f(x) dx usando la regla de Simpson 3/8,
que requiere que el número de subintervalos n sea múltiplo de 3.

Fórmula compuesta:
    h = (b - a) / n
    I ≈ (3h/8) · [f(x_0) + 3f(x_1) + 3f(x_2) + 2f(x_3) + 3f(x_4) + … + f(x_n)]

donde los coeficientes son: 1, 3, 3, 2, 3, 3, 2, …, 3, 3, 1

Error de truncamiento: O(h^4) por subintervalo, O(h^4) globalmente.

Implementado por: Andrés Yue — rama feature/vandermonde-simpson38
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Simpson38(NumericalMethod):

    # ── Metadatos ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "simpson38"

    @property
    def description(self) -> str:
        return "Simpson 3/8 (Integración Numérica)"

    @property
    def method_type(self) -> str:
        return "root"           # Reutiliza el flujo "root" (expr + params)

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
                "label_es": "Número de subintervalos n (múltiplo de 3)",
                "label_en": "Number of subintervals n (multiple of 3)",
                "type": "int",
                "default": 3,
            },
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese la función <code>f(x)</code> a integrar.</li>"
                "<li>Defina el intervalo <code>[a, b]</code> y el número de subintervalos <code>n</code>.</li>"
                "<li>⚠️ <strong>n debe ser múltiplo de 3</strong>. Si no lo es, el método lo ajusta automáticamente al siguiente múltiplo de 3.</li>"
                "<li>La regla compuesta aplica la fórmula de Simpson 3/8 en cada grupo de 3 subintervalos consecutivos.</li>"
                "<li>Fórmula: I ≈ (3h/8)·[f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + … + f(xₙ)]</li>"
                "<li>💡 Error de truncamiento global: O(h⁴). Más preciso que Simpson 1/3 cuando n es divisible por 3 pero no por 2.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter the function <code>f(x)</code> to integrate.</li>"
                "<li>Set the interval <code>[a, b]</code> and the number of subintervals <code>n</code>.</li>"
                "<li>⚠️ <strong>n must be a multiple of 3</strong>. If not, the method automatically rounds up to the next multiple of 3.</li>"
                "<li>The composite rule applies the Simpson 3/8 formula over each group of 3 consecutive subintervals.</li>"
                "<li>Formula: I ≈ (3h/8)·[f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + … + f(xₙ)]</li>"
                "<li>💡 Global truncation error: O(h⁴). More accurate than Simpson 1/3 when n is divisible by 3 but not 2.</li>"
                "</ul>"
            ),
        }

    # ── Kernel numérico ───────────────────────────────────────────────────────

    @staticmethod
    def _coefficient(i: int, n: int) -> int:
        """Coeficiente de cada nodo en la suma de Simpson 3/8.
        Patrón: 1, [3, 3, 2]·(n/3 - 1 veces), 3, 3, 1
        Equivale a: extremos → 1; múltiplos de 3 (internos) → 2; resto → 3.
        """
        if i == 0 or i == n:
            return 1
        if i % 3 == 0:
            return 2
        return 3

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        a = float(params.get("a", 0))
        b = float(params.get("b", 1))
        n = int(params.get("n", 3))

        # ── Validaciones ──────────────────────────────────────────────────────
        if a >= b:
            raise ValueError("El límite inferior a debe ser menor que el límite superior b.")
        if n < 3:
            n = 3

        # Ajustar n al múltiplo de 3 más cercano por arriba
        n_original = n
        if n % 3 != 0:
            n = n + (3 - n % 3)

        steps = []
        h = (b - a) / n

        # ── Paso 1: Configuración ─────────────────────────────────────────────
        adjusted_msg = (
            f" (ajustado de n={n_original} al siguiente múltiplo de 3)"
            if n != n_original else ""
        )
        steps.append({
            "step": 1,
            "phase": "setup",
            "description": (
                f"Configuración: a={a}, b={b}, n={n}{adjusted_msg}, "
                f"h=(b-a)/n=({b}-{a})/{n}={h:.8g}"
            ),
            "a": a, "b": b, "n": n, "h": h,
        })

        # ── Paso 2: Evaluación de los nodos ──────────────────────────────────
        nodes = [a + i * h for i in range(n + 1)]
        f_vals = []
        coefs = []

        for i, xi in enumerate(nodes):
            fxi = f(xi)
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

        # ── Paso 3: Suma ponderada ────────────────────────────────────────────
        weighted_sum = sum(ci * fxi for ci, fxi in zip(coefs, f_vals))
        steps.append({
            "step": len(steps) + 1,
            "phase": "weighted_sum",
            "description": (
                f"Suma ponderada Σ(c_i · f(x_i)) = {weighted_sum:.10g}  "
                f"con patrón de coeficientes [1, 3, 3, 2, 3, 3, 2, …, 3, 3, 1]"
            ),
            "weighted_sum": weighted_sum,
            "coefficients_pattern": coefs,
        })

        # ── Paso 4: Integral ──────────────────────────────────────────────────
        integral = (3 * h / 8) * weighted_sum
        steps.append({
            "step": len(steps) + 1,
            "phase": "result",
            "description": (
                f"Integral ≈ (3h/8) · suma = (3·{h:.8g}/8) · {weighted_sum:.10g} "
                f"= {integral:.10g}"
            ),
            "factor": 3 * h / 8,
            "integral": integral,
        })

        # ── Paso 5: Estimación del error (por refinamiento h→h/3) ─────────────
        # Usamos la extrapolación de Richardson (comparar con n*3 subintervalos)
        n_ref = n * 3
        h_ref = (b - a) / n_ref
        nodes_ref = [a + i * h_ref for i in range(n_ref + 1)]
        f_ref = [f(xi) for xi in nodes_ref]
        coefs_ref = [self._coefficient(i, n_ref) for i in range(n_ref + 1)]
        integral_ref = (3 * h_ref / 8) * sum(c * fv for c, fv in zip(coefs_ref, f_ref))
        error_est = abs(integral_ref - integral) / 15.0   # extrapolación Richardson O(h^4)

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
            "Error estimado (Richardson)": f"{error_est:.2e}",
            "Fórmula": "I ≈ (3h/8)·[f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + … + f(xₙ)]",
        }
        if n != n_original:
            props["Nota"] = f"n ajustado de {n_original} a {n} (múltiplo de 3)"

        return {
            "solution": [integral],
            "root": integral,          # alias para compatibilidad con flujo "root"
            "properties": props,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
