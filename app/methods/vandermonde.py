"""
Método de Vandermonde
================================================
Construye el polinomio interpolante usando la
matriz de Vandermonde.

La matriz sigue la convención teórica clásica:

    V[i][j] = x_i^(n-1-j)

Es decir, las columnas se ordenan desde la
mayor potencia hasta la potencia cero.

Además, el método construye y muestra la
ecuación explícita del polinomio interpolante.

Implementado originalmente por: Julian (MetodosJul)
Integrado a la arquitectura web por: Andrés Yue
"""

import numpy as np

from sympy import symbols, expand

from app.core.base_method import NumericalMethod


class VandermondeMethod(NumericalMethod):

    # ── Metadata ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "vandermonde"

    @property
    def description(self) -> dict:
        return {"es": "Método de Vandermonde", "en": "Vandermonde Method"}

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
            "<li>Ingrese los nodos de interpolación <code>x</code> y sus valores <code>y</code>.</li>"
            "<li>El método construye la matriz de Vandermonde.</li>"
            "<li>Cada columna representa una potencia decreciente de x.</li>"
            "<li>Se resuelve el sistema lineal V·a = y.</li>"
            "<li>Los coeficientes obtenidos corresponden al polinomio interpolante.</li>"
            "<li>También se genera la ecuación explícita del polinomio P(x).</li>"
            "</ul>"
        )

        html_en = (
            "<ul>"
            "<li>Enter interpolation nodes <code>x</code> and function values <code>y</code>.</li>"
            "<li>The method builds the Vandermonde matrix.</li>"
            "<li>Each column represents descending powers of x.</li>"
            "<li>The linear system V·a = y is solved.</li>"
            "<li>The resulting coefficients define the interpolation polynomial.</li>"
            "<li>The explicit polynomial equation P(x) is also generated.</li>"
            "</ul>"
        )

        return {"es": html_es, "en": html_en}

    # ── Build Vandermonde Matrix ─────────────────────────────────────────────

    @staticmethod
    def _build_vandermonde(xs: list[float]) -> np.ndarray:
        """
        Build Vandermonde matrix using descending powers.

        Theoretical convention:

            [x^(n-1)  x^(n-2) ... x^1  x^0]
        """

        n = len(xs)

        V = np.zeros((n, n))

        for i in range(n):

            for j in range(n):

                power = n - 1 - j

                V[i][j] = xs[i] ** power

        return V

    # ── Polynomial Evaluation ────────────────────────────────────────────────

    @staticmethod
    def _evaluate_polynomial(coeffs: list[float], x: float) -> float:
        """
        Evaluate polynomial using descending powers.
        """

        n = len(coeffs)

        result = 0.0

        for i in range(n):

            power = n - 1 - i

            result += coeffs[i] * (x ** power)

        return result

    # ── Build Explicit Polynomial ────────────────────────────────────────────

    @staticmethod
    def _build_polynomial(coeffs: list[float]) -> tuple[str, str]:
        """
        Build explicit polynomial equation in:
        - expanded form
        - readable mathematical form
        """

        x = symbols('x')

        n = len(coeffs)

        poly = 0

        readable_terms = []

        for i in range(n):

            coeff = coeffs[i]

            power = n - 1 - i

            poly += coeff * (x ** power)

            coeff_str = f"{coeff:.10g}"

            if abs(coeff) < 1e-14:
                continue

            if power > 1:
                readable_terms.append(
                    f"({coeff_str})x^{power}"
                )

            elif power == 1:
                readable_terms.append(
                    f"({coeff_str})x"
                )

            else:
                readable_terms.append(
                    f"({coeff_str})"
                )

        expanded_poly = expand(poly)

        readable_poly = " + ".join(readable_terms)
        readable_poly = readable_poly.replace("+ (-", "- (")

        return (
            f"P(x) = {expanded_poly}",
            f"P(x) = {readable_poly}"
        )

    # ── Public Solve Method ──────────────────────────────────────────────────

    def solve(self, points: list, x_eval: float | None = None, **_kwargs) -> dict:

        if not points or len(points) < 2:
            raise ValueError(
                "Se necesitan al menos 2 nodos."
            )

        xs = []
        ys = []

        # Extract points
        for idx, pair in enumerate(points):

            if (
                not isinstance(pair, (list, tuple))
                or len(pair) != 2
            ):
                raise ValueError(
                    f"Nodo inválido en índice {idx}."
                )

            xs.append(float(pair[0]))
            ys.append(float(pair[1]))

        n = len(xs)

        # Validate distinct nodes
        for i in range(n):

            for j in range(i + 1, n):

                if abs(xs[i] - xs[j]) < 1e-14:
                    raise ValueError(
                        "Los valores x_i deben ser distintos."
                    )

        steps = []

        # ── Step 1: Setup ───────────────────────────────────────────────────

        steps.append({

            "step": 1,

            "phase": "setup",

            "description": {"es": (
                f"Construcción de la matriz de Vandermonde "
                f"para n = {n} nodos."
            ), "en": (
                f"Construcción de la matriz de Vandermonde "
                f"para n = {n} nodos."
            )}

        })

        # ── Step 2: Build Matrix ───────────────────────────────────────────

        V = self._build_vandermonde(xs)

        steps.append({

            "step": len(steps) + 1,

            "phase": "matrix",

            "description": {"es": (
                "Matriz de Vandermonde construida "
                "usando potencias descendentes."
            ), "en": (
                "Matriz de Vandermonde construida "
                "usando potencias descendentes."
            )},

            "matrix_state": V.tolist()

        })

        # ── Step 3: Solve Linear System ────────────────────────────────────

        coeffs = np.linalg.solve(V, np.array(ys))

        coeffs_list = coeffs.tolist()

        steps.append({

            "step": len(steps) + 1,

            "phase": "solution",

            "description": {"es": (
                "Coeficientes del polinomio interpolante "
                "obtenidos resolviendo V·a = y."
            ), "en": (
                "Coeficientes del polinomio interpolante "
                "obtenidos resolviendo V·a = y."
            )},

            "coefficients": coeffs_list

        })

        # ── Step 4: Explicit Polynomial ────────────────────────────────────

        polynomial_str, polynomial_readable = (
            self._build_polynomial(coeffs_list)
        )

        steps.append({

            "step": len(steps) + 1,

            "phase": "polynomial",

            "description": {"es": (
                "Polinomio interpolante explícito generado."
            ), "en": (
                "Generated explicit interpolating polynomial."
            )},

            "polynomial": polynomial_str,

            "polynomial_readable": polynomial_readable

        })

        # ── Step 5: Evaluate Polynomial ────────────────────────────────────

        p_x = None

        if x_eval is not None:

            x_eval = float(x_eval)

            p_x = self._evaluate_polynomial(
                coeffs_list,
                x_eval
            )

            steps.append({

                "step": len(steps) + 1,

                "phase": "evaluation",

                "description": {"es": (
                    f"P({x_eval:g}) = {p_x:.16g}"
                ), "en": (
                    f"P({x_eval:g}) ={p_x:.16g}"
                )},

                "eval_x": x_eval,

                "eval_y": p_x

            })

        # ── Step 6: Verification ───────────────────────────────────────────

        for xi, yi in zip(xs, ys):

            pi = self._evaluate_polynomial(
                coeffs_list,
                xi
            )

            err = abs(pi - yi)

            steps.append({

                "step": len(steps) + 1,

                "phase": "verification",

                "description": {"es": (
                    f"P({xi}) = {pi:.8g} "
                    f"(esperado {yi}, error = {err:.2e})"
                ), "en": (
                    f"P({xi}) = {pi:.8g} "
                    f"(esperado {yi}, error = {err:.2e})"
                )},

                "x": xi,

                "p_x": pi,

                "expected": yi,

                "error": err

            })

        # ── Properties ─────────────────────────────────────────────────────

        props = {

            "Número de nodos": str(n),

            "Grado del polinomio": str(n - 1),

            "Coeficientes": (
                ", ".join(f"{c:.6g}" for c in coeffs_list)
            ),

            "Polinomio expandido": polynomial_str,

            "Polinomio legible": polynomial_readable

        }

        if p_x is not None:

            props["P(x_eval)"] = f"{p_x:.10g}"

            props["Punto evaluado"] = str(x_eval)

        # ── Final Response ─────────────────────────────────────────────────

        return {

            "solution": {

                "nodes_x": xs,

                "nodes_y": ys,

                "coefficients": coeffs_list,

                "polynomial": polynomial_str,

                "polynomial_readable": polynomial_readable,

                "x_eval": x_eval,

                "P_x": p_x,

            },

            "properties": props,

            "steps": steps,

            "iterations": len(steps),

            "method": self.name,

            "plot_type": self.plot_type,

        }