"""
Lagrange polynomial interpolation — constructs P(x) through distinct nodes (x_i, y_i).
"""
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
    def instructions(self) -> dict:
        html = (
            "<ul>"
            "<li>Enter at least two distinct nodes <code>x_i</code> with values <code>y_i</code>.</li>"
            "<li>The interpolating polynomial has degree at most <code>n − 1</code> for <code>n</code> nodes.</li>"
            "<li>Basis polynomials: "
            "<code>L_j(x) = Π_{m≠j} (x − x_m) / (x_j − x_m)</code>; "
            "<code>P(x) = Σ_j y_j L_j(x)</code>.</li>"
            "<li>Set <code>x</code> to evaluate <code>P(x)</code> at that point.</li>"
            "</ul>"
        )
        return {"es": html, "en": html}

    def solve(self, points: list, x_eval: float | None = None, **_kwargs) -> dict:
        if not points or len(points) < 2:
            raise ValueError("At least two interpolation nodes are required.")

        xs: list[float] = []
        ys: list[float] = []
        for i, pair in enumerate(points):
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                raise ValueError(f"Each node must be [x, y]; invalid entry at index {i}.")
            xs.append(float(pair[0]))
            ys.append(float(pair[1]))

        n = len(xs)
        for i in range(n):
            for j in range(i + 1, n):
                if abs(xs[i] - xs[j]) < 1e-14:
                    raise ValueError("Abscissas x_i must be pairwise distinct.")

        if x_eval is None:
            raise ValueError("Evaluation point 'x_eval' is required.")

        x_eval = float(x_eval)
        steps = []

        steps.append({
            "step": 1,
            "phase": "lagrange_setup",
            "description": (
                f"Nodes: n = {n}. Distinct abscissas verified. "
                f"Evaluate P(x) at x = {x_eval:g} using Lagrange bases L_j(x)."
            ),
        })

        products_detail = []

        for j in range(n):
            lj = 1.0
            factors = []
            for m in range(n):
                if m == j:
                    continue
                xm, xj = xs[m], xs[j]
                factor_num = x_eval - xm
                factor_den = xj - xm
                term = factor_num / factor_den
                lj *= term
                factors.append(f"({x_eval:g}-{xm:g})/({xj:g}-{xm:g})={term:.10g}")

            contrib = ys[j] * lj
            products_detail.append(contrib)

            steps.append({
                "step": len(steps) + 1,
                "phase": "lagrange_basis",
                "description": (
                    f"j = {j}: L_j(x) = {lj:.16g}; "
                    f"y_j * L_j(x) = {ys[j]:g} * {lj:.16g} = {contrib:.16g}. "
                    f"Factors: {' × '.join(factors)}"
                ),
            })

        p_x = sum(products_detail)

        steps.append({
            "step": len(steps) + 1,
            "phase": "lagrange_sum",
            "description": (
                f"P({x_eval:g}) = Σ_j y_j L_j(x) = {p_x:.16g}"
            ),
        })

        return {
            "solution": {
                "x_eval": x_eval,
                "P_x": p_x,
                "nodes_x": xs,
                "nodes_y": ys,
            },
            "steps": steps,
            "method": self.name,
        }
