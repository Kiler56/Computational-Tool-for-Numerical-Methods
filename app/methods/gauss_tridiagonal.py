"""
Gauss Tridiagonal — Algoritmo de Thomas (TDMA).

Resuelve sistemas tridiagonales de forma eficiente O(n).
Valida que la matriz sea tridiagonal antes de proceder.
"""
from app.core.base_method import NumericalMethod


class GaussTridiagonal(NumericalMethod):

    @property
    def name(self) -> str:
        return "gauss_tridiagonal"

    @property
    def description(self) -> str:
        return "Gauss Tridiagonal — Algoritmo de Thomas"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>⚠️ <strong>Restricción Crítica:</strong> La matriz ingresada debe ser <strong>estrictamente tridiagonal</strong> (todos los elementos fuera de la diagonal principal, superdiagonal y subdiagonal deben ser 0).</li>"
                "<li>Si la matriz no cumple esta condición, el algoritmo arrojará un error de validación inicial.</li>"
                "<li>💡 <strong>Rendimiento:</strong> Este algoritmo (TDMA) procesa sistemas tridiagonales en tiempo lineal <code>O(n)</code>.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>⚠️ <strong>Critical Restriction:</strong> The input matrix must be <strong>strictly tridiagonal</strong> (all elements outside the main diagonal, superdiagonal and subdiagonal must be 0).</li>"
                "<li>If the matrix does not meet this condition, the algorithm will throw an initial validation error.</li>"
                "<li>💡 <strong>Performance:</strong> This algorithm (TDMA) processes tridiagonal systems in linear time <code>O(n)</code>.</li>"
                "</ul>"
            ),
        }

    def _validate_tridiagonal(self, A: list, n: int) -> None:
        """Verifica que la matriz sea estrictamente tridiagonal."""
        for i in range(n):
            for j in range(n):
                if abs(i - j) > 1 and abs(A[i][j]) > 1e-12:
                    raise ValueError(
                        f"La matriz NO es tridiagonal: A[{i}][{j}] = {A[i][j]} ≠ 0. "
                        "Use otro método de resolución."
                    )

    def solve(self, A: list, b: list) -> dict:
        n = len(b)
        self._validate_tridiagonal(A, n)

        # Extraer diagonales
        # a: subdiagonal (a[0] no se usa, a[1..n-1])
        # d: diagonal principal
        # c: superdiagonal (c[n-1] no se usa, c[0..n-2])
        a = [0.0] + [A[i][i - 1] for i in range(1, n)]
        d = [A[i][i] for i in range(n)]
        c = [A[i][i + 1] for i in range(n - 1)] + [0.0]
        r = [bi for bi in b]  # RHS (copia)

        steps = []

        steps.append({
            "step": 1,
            "phase": "extract",
            "description": "Vectores extraídos de la matriz tridiagonal",
            "sub_diagonal": self._snapshot(a),
            "main_diagonal": self._snapshot(d),
            "super_diagonal": self._snapshot(c),
            "rhs": self._snapshot(r),
        })

        # --- Forward sweep ---
        for i in range(1, n):
            if abs(d[i - 1]) < 1e-12:
                raise ValueError(f"División por cero en forward sweep (d[{i-1}] = {d[i-1]}).")
            w = a[i] / d[i - 1]
            d[i] = d[i] - w * c[i - 1]
            r[i] = r[i] - w * r[i - 1]

            steps.append({
                "step": len(steps) + 1,
                "phase": "forward_sweep",
                "description": (
                    f"i={i}: w = a[{i}]/d[{i-1}] = {w:.6g}, "
                    f"d[{i}] = {d[i]:.6g}, r[{i}] = {r[i]:.6g}"
                ),
                "w": w,
                "main_diagonal": self._snapshot(d),
                "rhs": self._snapshot(r),
            })

        # --- Back substitution ---
        x = [0.0] * n
        if abs(d[n - 1]) < 1e-12:
            raise ValueError(f"División por cero en back substitution (d[{n-1}] = {d[n-1]}).")
        x[n - 1] = r[n - 1] / d[n - 1]

        steps.append({
            "step": len(steps) + 1,
            "phase": "back_substitution",
            "description": f"x[{n-1}] = r[{n-1}] / d[{n-1}] = {x[n-1]:.6g}",
            "solution_partial": self._snapshot(x),
        })

        for i in range(n - 2, -1, -1):
            if abs(d[i]) < 1e-12:
                raise ValueError(f"División por cero en back substitution (d[{i}] = {d[i]}).")
            x[i] = (r[i] - c[i] * x[i + 1]) / d[i]

            steps.append({
                "step": len(steps) + 1,
                "phase": "back_substitution",
                "description": (
                    f"x[{i}] = (r[{i}] - c[{i}]·x[{i+1}]) / d[{i}] = {x[i]:.6g}"
                ),
                "solution_partial": self._snapshot(x),
            })

        return {
            "solution": x,
            "steps": steps,
            "iterations": len(steps),
            "lower": self._snapshot(a),
            "upper": self._snapshot(c),
            "method": self.name,
        }


if __name__ == "__main__":
    # Sistema tridiagonal 4×4
    A = [
        [2, -1, 0, 0],
        [-1, 2, -1, 0],
        [0, -1, 2, -1],
        [0, 0, -1, 2],
    ]
    b = [1, 0, 0, 1]
    result = GaussTridiagonal().solve(A, b)
    print("Solución:", result["solution"])  # Esperado: [1, 1, 1, 1]
    print("Pasos:", len(result["steps"]))
