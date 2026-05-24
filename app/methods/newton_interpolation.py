"""
Interpolación de Newton (Diferencias Divididas)
================================================
Construye el polinomio interpolante de Newton usando la tabla de diferencias
divididas. El polinomio tiene la forma:

    P(x) = c₀ + c₁(x−x₀) + c₂(x−x₀)(x−x₁) + … + cₙ₋₁∏(x−xᵢ)

donde c₀, c₁, …, cₙ₋₁ son los coeficientes de diferencias divididas.

Implementado originalmente por: Julio (MetodosJul)
Integrado a la arquitectura web por: Andrés Yue
"""
from app.core.base_method import NumericalMethod


class NewtonInterpolation(NumericalMethod):

    # ── Metadatos ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "newton_interpolation"

    @property
    def description(self) -> str:
        return "Interpolación de Newton (Diferencias Divididas)"

    @property
    def method_type(self) -> str:
        return "interpolation"

    @property
    def plot_type(self) -> str:
        return "interpolation"

    @property
    def instructions(self) -> dict:
        html_es = (
            "<ul>"
            "<li>Ingrese los nodos de interpolación <code>x</code> con sus valores <code>y = f(x)</code>.</li>"
            "<li>El método construye la <strong>tabla de diferencias divididas</strong> D[i][j].</li>"
            "<li>Los coeficientes del polinomio son la diagonal: c<sub>i</sub> = D[i][i].</li>"
            "<li>El polinomio evalúa P(x) usando la forma anidada de Newton (similar a Horner).</li>"
            "<li>💡 <strong>Ventaja sobre Lagrange:</strong> Agregar un nodo nuevo requiere solo una columna "
            "adicional en la tabla, sin recalcular todo.</li>"
            "</ul>"
        )
        html_en = (
            "<ul>"
            "<li>Enter interpolation nodes <code>x</code> with their function values <code>y = f(x)</code>.</li>"
            "<li>The method builds the <strong>divided differences table</strong> D[i][j].</li>"
            "<li>Polynomial coefficients are the main diagonal: c<sub>i</sub> = D[i][i].</li>"
            "<li>P(x) is evaluated using Newton's nested form (similar to Horner's scheme).</li>"
            "<li>💡 <strong>Advantage over Lagrange:</strong> Adding a new node requires only one extra "
            "column in the table, no full recomputation needed.</li>"
            "</ul>"
        )
        return {"es": html_es, "en": html_en}

    # ── Kernel numérico (código original de Julio, adaptado) ──────────────────

    @staticmethod
    def _build_divided_differences(xs: list, ys: list) -> list:
        """Construye la tabla completa de diferencias divididas n×n."""
        n = len(xs)
        D = [[0.0] * n for _ in range(n)]

        # Primera columna = valores Y
        for i in range(n):
            D[i][0] = ys[i]

        # Rellenar columnas j = 1..n-1
        for j in range(1, n):
            for i in range(j, n):
                denom = xs[i] - xs[i - j]
                if abs(denom) < 1e-14:
                    raise ValueError(
                        f"Nodos repetidos detectados entre x[{i}] y x[{i - j}]."
                    )
                D[i][j] = (D[i][j - 1] - D[i - 1][j - 1]) / denom

        return D

    @staticmethod
    def _eval_newton(xs: list, coeffs: list, x_eval: float) -> float:
        """Evalúa P(x) usando la forma anidada de Newton."""
        n = len(coeffs)
        result = coeffs[n - 1]
        for k in range(n - 2, -1, -1):
            result = result * (x_eval - xs[k]) + coeffs[k]
        return result

    # ── Punto de entrada público ───────────────────────────────────────────────

    def solve(self, points: list, x_eval: float | None = None, **_kwargs) -> dict:
        if not points or len(points) < 2:
            raise ValueError("Se necesitan al menos 2 nodos para interpolar.")

        xs: list[float] = []
        ys: list[float] = []
        for idx, pair in enumerate(points):
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                raise ValueError(f"Cada nodo debe ser [x, y]; entrada inválida en índice {idx}.")
            xs.append(float(pair[0]))
            ys.append(float(pair[1]))

        n = len(xs)

        # Verificar nodos distintos
        for i in range(n):
            for j in range(i + 1, n):
                if abs(xs[i] - xs[j]) < 1e-14:
                    raise ValueError("Las abscisas x_i deben ser distintas entre sí.")

        if x_eval is None:
            raise ValueError("Se requiere el punto de evaluación 'x_eval'.")

        x_eval = float(x_eval)
        steps = []

        # ── Paso 1: Inicialización ─────────────────────────────────────────────
        steps.append({
            "step": 1,
            "phase": "setup",
            "description": (
                f"Nodos: n = {n}. "
                f"X = {xs}, Y = {ys}. "
                f"Evaluar P({x_eval:g}) usando diferencias divididas de Newton."
            ),
        })

        # ── Paso 2: Tabla de diferencias divididas ────────────────────────────
        D = self._build_divided_differences(xs, ys)

        for j in range(n):
            col_vals = []
            for i in range(j, n):
                col_vals.append(f"D[{i}][{j}] = {D[i][j]:.10g}")
            steps.append({
                "step": len(steps) + 1,
                "phase": "divided_differences",
                "description": (
                    f"Columna j={j}: " + " | ".join(col_vals)
                ),
                "matrix_state": [row[:j + 1] for row in D],
            })

        # Coeficientes = diagonal principal
        coeffs = [D[i][i] for i in range(n)]
        steps.append({
            "step": len(steps) + 1,
            "phase": "result",
            "description": (
                f"Coeficientes del polinomio de Newton (diagonal): "
                f"{[f'c{i}={c:.8g}' for i, c in enumerate(coeffs)]}"
            ),
            "coefficients": coeffs[:],
        })

        # ── Paso 3: Evaluación P(x_eval) ──────────────────────────────────────
        p_x = self._eval_newton(xs, coeffs, x_eval)
        steps.append({
            "step": len(steps) + 1,
            "phase": "evaluation",
            "description": (
                f"Evaluación P({x_eval:g}) = {p_x:.16g} "
                f"usando la forma anidada de Newton."
            ),
            "eval_x": x_eval,
            "eval_y": p_x,
        })

        # ── Paso 4: Verificación en los nodos originales ──────────────────────
        for xi, yi in zip(xs, ys):
            pi = self._eval_newton(xs, coeffs, xi)
            err = abs(pi - yi)
            steps.append({
                "step": len(steps) + 1,
                "phase": "verification",
                "description": (
                    f"P({xi}) = {pi:.8g}  (esperado {yi}, error = {err:.2e})"
                ),
                "x": xi, "p_x": pi, "expected": yi, "error": err,
            })

        # ── Propiedades para la UI ─────────────────────────────────────────────
        props = {
            "P(x_eval)": f"{p_x:.10g}",
            "Punto evaluado": str(x_eval),
            "Número de nodos": str(n),
            "Grado del polinomio": str(n - 1),
            "Coeficientes c_i": ", ".join(f"{c:.6g}" for c in coeffs),
        }

        return {
            "solution": {
                "x_eval": x_eval,
                "P_x": p_x,
                "nodes_x": xs,
                "nodes_y": ys,
            },
            "properties": props,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }
