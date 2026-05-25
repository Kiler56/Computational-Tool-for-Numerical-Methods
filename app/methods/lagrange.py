"""
Lagrange polynomial interpolation
================================================
Constructs the interpolation polynomial P(x)
through distinct interpolation nodes (x_i, y_i).

The polynomial has the form:

    P(x) = Σ y_j L_j(x)

where:

    L_j(x) = Π ((x - x_m)/(x_j - x_m)),  m ≠ j

Additionally, the explicit expanded polynomial
is generated algebraically.

Implementado originalmente por: Julian (MetodosJul)
Integrado a la arquitectura web por: Andrés Yue
"""

from sympy import symbols, expand

from app.core.base_method import NumericalMethod


class LagrangeInterpolation(NumericalMethod):

    @property
    def name(self) -> str:
        return "lagrange"

    @property
    def description(self) -> str:
        return "Lagrange interpolation"

    @property
    def method_type(self) -> str:
        return "interpolation"

    @property
    def plot_type(self) -> str:
        return "interpolation"

    @property
    def instructions(self) -> dict:

        html = (
            "<ul>"
            "<li>Enter at least two distinct nodes <code>x_i</code> with values <code>y_i</code>.</li>"
            "<li>The interpolating polynomial has degree at most <code>n − 1</code> for <code>n</code> nodes.</li>"
            "<li>Basis polynomials: "
            "<code>L_j(x) = Π_{m≠j} (x − x_m) / (x_j − x_m)</code>; "
            "<code>P(x) = Σ_j y_j L_j(x)</code>.</li>"
            "<li>The explicit expanded polynomial is also generated.</li>"
            "<li>Set <code>x</code> to evaluate <code>P(x)</code> at that point.</li>"
            "</ul>"
        )

        return {"es": html, "en": html}

    # ── Build Explicit Polynomial ────────────────────────────────────────────

    @staticmethod
    def _build_lagrange_polynomial(
        xs: list,
        ys: list
    ) -> str:
        """
        Construct explicit expanded polynomial.
        """

        x = symbols('x')

        n = len(xs)

        poly = 0

        for j in range(n):

            Lj = 1

            for m in range(n):

                if m != j:

                    Lj *= (
                        (x - xs[m])
                        /
                        (xs[j] - xs[m])
                    )

            poly += ys[j] * Lj

        expanded_poly = expand(poly)

        return f"P(x) = {expanded_poly.evalf(6)}"

    # ── Public Solve Method ──────────────────────────────────────────────────

    def solve(self, points: list, x_eval: float | None = None, **_kwargs) -> dict:

        # Validate points
        if not points or len(points) < 2:
            raise ValueError(
                "At least two interpolation nodes are required."
            )

        xs: list[float] = []
        ys: list[float] = []

        # Extract points
        for i, pair in enumerate(points):

            if (
                not isinstance(pair, (list, tuple))
                or len(pair) != 2
            ):
                raise ValueError(
                    f"Each node must be [x, y]; invalid entry at index {i}."
                )

            xs.append(float(pair[0]))
            ys.append(float(pair[1]))

        n = len(xs)

        # Validate distinct nodes
        for i in range(n):

            for j in range(i + 1, n):

                if abs(xs[i] - xs[j]) < 1e-14:
                    raise ValueError(
                        "Abscissas x_i must be pairwise distinct."
                    )

        # Validate evaluation point
        if x_eval is None:
            raise ValueError(
                "Evaluation point 'x_eval' is required."
            )

        x_eval = float(x_eval)

        # ── Build Explicit Polynomial ───────────────────────────────────────

        polynomial_str = self._build_lagrange_polynomial(
            xs,
            ys
        )

        steps = []

        # ── Step 1: Setup ───────────────────────────────────────────────────

        steps.append({

            "step": 1,

            "phase": "lagrange_setup",

            "description": (
                f"Nodes: n = {n}. Distinct abscissas verified. "
                f"Evaluate P(x) at x = {x_eval:g} "
                f"using Lagrange bases L_j(x)."
            ),

        })

        products_detail = []

        # ── Step 2: Build Basis Polynomials ────────────────────────────────

        for j in range(n):

            lj = 1.0

            factors = []

            for m in range(n):

                if m == j:
                    continue

                xm = xs[m]
                xj = xs[j]

                factor_num = x_eval - xm

                factor_den = xj - xm

                term = factor_num / factor_den

                lj *= term

                factors.append(
                    f"({x_eval:g}-{xm:g})/({xj:g}-{xm:g})={term:.10g}"
                )

            contrib = ys[j] * lj

            products_detail.append(contrib)

            steps.append({

                "step": len(steps) + 1,

                "phase": "lagrange_basis",

                "description": (
                    f"j = {j}: "
                    f"L_j(x) = {lj:.16g}; "
                    f"y_j * L_j(x) = "
                    f"{ys[j]:g} * {lj:.16g} = {contrib:.16g}. "
                    f"Factors: {' × '.join(factors)}"
                ),

            })

        # ── Step 3: Explicit Polynomial ────────────────────────────────────

        steps.append({

            "step": len(steps) + 1,

            "phase": "polynomial",

            "description": (
                "Explicit expanded interpolation polynomial generated."
            ),

            "polynomial": polynomial_str,

        })

        # ── Step 4: Final Polynomial Evaluation ────────────────────────────

        p_x = sum(products_detail)

        steps.append({

            "step": len(steps) + 1,

            "phase": "lagrange_sum",

            "description": (
                f"P({x_eval:g}) = Σ_j y_j L_j(x) = {p_x:.16g}"
            ),

        })

        # ── Properties ──────────────────────────────────────────────────────

        props = {

            "Número de nodos": str(n),

            "Grado del polinomio": str(n - 1),

            "Punto evaluado": str(x_eval),

            "P(x_eval)": f"{p_x:.10g}",

            "Polinomio": polynomial_str,

        }

        # ── Final Response ──────────────────────────────────────────────────

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