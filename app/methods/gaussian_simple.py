"""
Gaussian elimination without pivoting.

Solves Ax = b by forward elimination and back substitution.
Snapshots the augmented matrix each step.
"""
import math
from app.core.base_method import NumericalMethod


class GaussianSimple(NumericalMethod):

    @property
    def name(self) -> str:
        return "gaussian_simple"

    @property
    def description(self) -> dict:
        return {"es": "Eliminación gaussiana (simple)", "en": "Gaussian elimination (simple)"}

    @property
    def plot_type(self) -> str:
        return "gaussian_elim"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul><li>Ingrese una matriz de coeficientes cuadrados <code>A</code> y un vector RHS <code>b</code>.</li><li>Esta variante no intercambia filas.</li><li>⚠️ <strong>Restricción:</strong> Un pivote diagonal cero o pequeño hace que el método falle; use una variante pivotante en su lugar.</li></ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter a square coefficient matrix <code>A</code> and an independent terms vector <code>b</code>.</li>"
                "<li>This method does not perform row swapping.</li>"
                "<li>⚠️ <strong>Restriction:</strong> If any pivot (diagonal element) is zero or near zero, the method will fail. In that case, use a method with pivoting.</li>"
                "</ul>"
            ),
        }

    def solve(self, A: list, b: list) -> dict:
        # ── Input validation ──────────────────────────────────────────────
        try:
            n = len(b)
            if n == 0:
                raise ValueError("Vector b cannot be empty.")
            if len(A) != n:
                raise ValueError(
                    f"Matrix A has {len(A)} rows but b has {n} elements. "
                    "The system must be square (n×n matrix with n-element vector b)."
                )
            for i, row in enumerate(A):
                if len(row) != n:
                    raise ValueError(
                        f"Row {i} of A has {len(row)} elements but expected {n}. "
                        "Matrix A must be square."
                    )
            # Convert to float and check for non-numeric values
            A = [[float(v) for v in row] for row in A]
            b = [float(v) for v in b]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid input: {e}") from e

        for i, row in enumerate(A):
            for j, v in enumerate(row):
                if not math.isfinite(v):
                    raise ValueError(f"A[{i}][{j}] = {v} is not a finite number.")
        for i, v in enumerate(b):
            if not math.isfinite(v):
                raise ValueError(f"b[{i}] = {v} is not a finite number.")

        # Augmented matrix [A|b]
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        steps = []

        # --- Forward elimination ---
        for k in range(n - 1):
            pivot = M[k][k]
            if abs(pivot) < 1e-12:
                raise ValueError(
                    f"Zero (or near-zero) pivot at row {k+1} (diagonal element = {pivot:.2e}). "
                    "The system may be singular or nearly singular. "
                    "Use Gaussian Elimination with Partial or Total Pivoting instead."
                )

            steps.append({
                "step": len(steps) + 1,
                "phase": "elimination",
                "description": {"es": f"Pivote en ({k},{k}) = {pivot:.6g}", "en": f"Pivot at ({k},{k}) ={pivot:.6g}"},
                "pivot": pivot,
                "matrix_state": self._snapshot(M),
            })

            for i in range(k + 1, n):
                factor = M[i][k] / pivot
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]

                steps.append({
                    "step": len(steps) + 1,
                    "phase": "elimination",
                    "description": {"es": (
                        f"R{i+1} ← R{i+1} - ({factor:.6g})·R{k+1}  →  "
                        f"entrada cero M[{i}][{k}]"
                    ), "en": (
                        f"R{i+1} ← R{i+1} - ({factor:.6g})·R{k+1}  →  "
                        f"zero entry M[{i}][{k}]"
                    )},
                    "factor": factor,
                    "matrix_state": self._snapshot(M),
                })

        # --- Back substitution ---
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            if abs(M[i][i]) < 1e-12:
                raise ValueError(
                    f"Singular system detected during back substitution at row {i+1} "
                    f"(diagonal element ≈ {M[i][i]:.2e}). "
                    "The system has no unique solution — it may be inconsistent or underdetermined."
                )
            s = sum(M[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (M[i][n] - s) / M[i][i]

            if not math.isfinite(x[i]):
                raise ValueError(
                    f"x[{i}] = {x[i]} is not finite during back substitution. "
                    "Numerical instability detected — consider using a pivoting method."
                )

            steps.append({
                "step": len(steps) + 1,
                "phase": "back_substitution",
                "description": {"es": f"x[{i}] = ({M[i][n]:.6g} - {s:.6g}) / {M[i][i]:.6g} = {x[i]:.6g}", "en": f"x[{i}] = ({M[i][n]:.6g}-{s:.6g}) /{M[i][i]:.6g}={x[i]:.6g}"},
                "matrix_state": self._snapshot(M),
            })

        return {
            "solution": x,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
            "plot_type": self.plot_type,
        }


if __name__ == "__main__":
    # Caso 1: sistema 3×3 sencillo
    A1 = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b1 = [8, -11, -3]
    result = GaussianSimple().solve(A1, b1)
    print("Caso 1 — solución:", result["solution"])  # Esperado: [2, 3, -1]

    # Caso 2: sistema 2×2
    A2 = [[1, 2], [3, 5]]
    b2 = [5, 13]
    result = GaussianSimple().solve(A2, b2)
    print("Caso 2 — solución:", result["solution"])  # Esperado: [1, 2]
