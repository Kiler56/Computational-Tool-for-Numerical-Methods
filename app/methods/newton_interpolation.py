"""
Interpolación de Newton (Diferencias Divididas)
================================================
Construye el polinomio interpolante de Newton usando la tabla de diferencias
divididas. El polinomio tiene la forma:

    P(x) = c₀ + c₁(x−x₀) + c₂(x−x₀)(x−x₁) + … + cₙ₋₁∏(x−xᵢ)

donde c₀, c₁, …, cₙ₋₁ son los coeficientes de diferencias divididas.

Además, el método construye y muestra la
ecuación explícita expandida del polinomio.

Implementado originalmente por: Julian (MetodosJul)
Integrado a la arquitectura web por: Andrés Yue
"""

from sympy import symbols, expand

from app.core.base_method import NumericalMethod


class NewtonInterpolation(NumericalMethod):

    # ── Metadatos ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "newton_interpolation"

    @property
    def description(self) -> dict:
        return {"es": "Interpolación de Newton (Diferencias Divididas)", "en": "Newton Interpolation (Divided Differences)"}

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
            "<li>También se genera la ecuación explícita expandida del polinomio interpolante.</li>"
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
            "<li>The explicit expanded polynomial equation is also generated.</li>"
            "<li>💡 <strong>Advantage over Lagrange:</strong> Adding a new node requires only one extra "
            "column in the table, no full recomputation needed.</li>"
            "</ul>"
        )

        return {"es": html_es, "en": html_en}

    # ── Kernel numérico ───────────────────────────────────────────────────────

    @staticmethod
    def _build_divided_differences(xs: list, ys: list) -> list:
        """
        Construye la tabla completa de diferencias divididas.
        """

        n = len(xs)

        D = [[0.0] * n for _ in range(n)]

        # Primera columna = valores Y
        for i in range(n):
            D[i][0] = ys[i]

        # Construcción de diferencias divididas
        for j in range(1, n):

            for i in range(j, n):

                denom = xs[i] - xs[i - j]

                if abs(denom) < 1e-14:
                    raise ValueError(
                        f"Nodos repetidos detectados entre x[{i}] y x[{i - j}]."
                    )

                D[i][j] = (
                    D[i][j - 1] - D[i - 1][j - 1]
                ) / denom

        return D

    @staticmethod
    def _eval_newton(xs: list, coeffs: list, x_eval: float) -> float:
        """
        Evalúa el polinomio usando
        la forma anidada de Newton.
        """

        n = len(coeffs)

        result = coeffs[n - 1]

        for k in range(n - 2, -1, -1):

            result = (
                result * (x_eval - xs[k])
                + coeffs[k]
            )

        return result

    # ── Construcción explícita del polinomio ────────────────────────────────

    @staticmethod
    def _build_expanded_polynomial(
        xs: list,
        coeffs: list
    ) -> str:
        """
        Construye el polinomio expandido explícito.
        """

        x = symbols('x')

        n = len(coeffs)

        poly = coeffs[0]

        term = 1

        for i in range(1, n):

            term *= (x - xs[i - 1])

            poly += coeffs[i] * term

        expanded_poly = expand(poly)

        return f"P(x) = {expanded_poly.evalf(6)}"

    # ── Punto de entrada público ─────────────────────────────────────────────

    def solve(self, points: list, x_eval: float | None = None, **_kwargs) -> dict:

        # Validar mínimo de puntos
        if not points or len(points) < 2:
            raise ValueError(
                "Se necesitan al menos 2 nodos para interpolar."
            )

        xs: list[float] = []
        ys: list[float] = []

        # Extraer valores X e Y
        for idx, pair in enumerate(points):

            if (
                not isinstance(pair, (list, tuple))
                or len(pair) != 2
            ):
                raise ValueError(
                    f"Cada nodo debe ser [x, y]; entrada inválida en índice {idx}."
                )

            xs.append(float(pair[0]))
            ys.append(float(pair[1]))

        n = len(xs)

        # Validar nodos distintos
        for i in range(n):

            for j in range(i + 1, n):

                if abs(xs[i] - xs[j]) < 1e-14:
                    raise ValueError(
                        "Las abscisas x_i deben ser distintas entre sí."
                    )

        # Validar punto de evaluación
        if x_eval is None:
            raise ValueError(
                "Se requiere el punto de evaluación 'x_eval'."
            )

        x_eval = float(x_eval)

        steps = []

        # ── Step 1: Setup ───────────────────────────────────────────────────

        steps.append({

            "step": 1,

            "phase": "setup",

            "description": {"es": (
                f"Nodos: n = {n}. "
                f"X = {xs}, Y = {ys}. "
                f"Evaluar P({x_eval:g}) usando diferencias divididas de Newton."
            ), "en": (
                f"Nodes: n = {n}. "
                f"X = {xs}, Y = {ys}. "
                f"Evaluate P({x_eval:g}) using Newton's divided differences."
            )},

        })

        # ── Step 2: Tabla de diferencias divididas ─────────────────────────

        D = self._build_divided_differences(xs, ys)

        for j in range(n):

            col_vals = []

            for i in range(j, n):

                col_vals.append(
                    f"D[{i}][{j}] = {D[i][j]:.10g}"
                )

            steps.append({

                "step": len(steps) + 1,

                "phase": "divided_differences",

                "description": {"es": (
                    f"Columna j={j}: "
                    + " | ".join(col_vals)
                ), "en": (
                    f"Column j={j}: "
                    + " | ".join(col_vals)
                )},

                "matrix_state": [
                    [D[r + c][c] if r + c < n and c <= j else "" for c in range(n)]
                    for r in range(n)
                ],

            })

        # Coeficientes = diagonal principal
        coeffs = [D[i][i] for i in range(n)]

        # ── Step 3: Construcción del polinomio explícito ───────────────────

        polynomial_str = self._build_expanded_polynomial(
            xs,
            coeffs
        )

        steps.append({

            "step": len(steps) + 1,

            "phase": "polynomial",

            "description": {"es": (
                "Polinomio interpolante explícito generado."
            ), "en": (
                "Generated explicit interpolating polynomial."
            )},

            "polynomial": polynomial_str

        })

        # ── Step 4: Coeficientes ───────────────────────────────────────────

        steps.append({

            "step": len(steps) + 1,

            "phase": "result",

            "description": {"es": (
                f"Coeficientes del polinomio de Newton (diagonal): "
                f"{[f'c{i}={c:.8g}' for i, c in enumerate(coeffs)]}"
            ), "en": (
                f"Newton polynomial coefficients (diagonal): "
                f"{[f'c{i}={c:.8g}' for i, c in enumerate(coeffs)]}"
            )},

            "coefficients": coeffs[:],

        })

        # ── Step 5: Evaluación del polinomio ───────────────────────────────

        p_x = self._eval_newton(xs, coeffs, x_eval)

        steps.append({

            "step": len(steps) + 1,

            "phase": "evaluation",

            "description": {"es": (
                f"Evaluación P({x_eval:g}) = {p_x:.16g} "
                f"usando la forma anidada de Newton."
            ), "en": (
                f"Evaluation P({x_eval:g}) = {p_x:.16g} "
                f"using nested Newton form."
            )},

            "eval_x": x_eval,

            "eval_y": p_x,

        })

        # ── Step 6: Verificación en nodos originales ───────────────────────

        for xi, yi in zip(xs, ys):

            pi = self._eval_newton(xs, coeffs, xi)

            err = abs(pi - yi)

            steps.append({

                "step": len(steps) + 1,

                "phase": "verification",

                "description": {"es": (
                    f"P({xi}) = {pi:.8g} "
                    f"(esperado {yi}, error = {err:.2e})"
                ), "en": (
                    f"P({xi}) = {pi:.8g} "
                    f"(expected {yi}, error = {err:.2e})"
                )},

                "x": xi,

                "p_x": pi,

                "expected": yi,

                "error": err,

            })

        # ── Properties para UI ─────────────────────────────────────────────

        props = {

            "P(x_eval)": f"{p_x:.10g}",

            "Punto evaluado": str(x_eval),

            "Número de nodos": str(n),

            "Grado del polinomio": str(n - 1),

            "Coeficientes c_i": (
                ", ".join(f"{c:.6g}" for c in coeffs)
            ),

            "Polinomio": polynomial_str,

        }

        # ── Respuesta final ────────────────────────────────────────────────

        return {

            "solution": {

                "x_eval": x_eval,

                "P_x": p_x,

                "nodes_x": xs,

                "nodes_y": ys,

                "polynomial": polynomial_str,

            },

            "properties": props,

            "steps": steps,

            "iterations": len(steps),

            "method": self.name,

            "plot_type": self.plot_type,

        }