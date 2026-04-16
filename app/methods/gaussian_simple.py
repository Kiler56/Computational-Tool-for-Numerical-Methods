"""
Eliminación Gaussiana Simple — sin pivoteo.

Resuelve Ax=b mediante eliminación hacia adelante y sustitución regresiva.
Guarda un snapshot de la matriz aumentada en cada paso.
"""
from app.core.base_method import NumericalMethod


class GaussianSimple(NumericalMethod):

    @property
    def name(self) -> str:
        return "gaussian_simple"

    @property
    def description(self) -> str:
        return "Eliminación Gaussiana Simple"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese una matriz cuadrada <code>A</code> de coeficientes y un vector <code>b</code> de términos independientes.</li>"
                "<li>Este método no realiza intercambio de filas.</li>"
                "<li>⚠️ <strong>Restricción:</strong> Si algún pivote (elemento de la diagonal) es cero o cercano a cero, el método fallará. En ese caso, utilice un método con pivoteo.</li>"
                "</ul>"
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
        n = len(b)
        # Construir matriz aumentada [A|b]
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        steps = []

        # --- Eliminación hacia adelante ---
        for k in range(n - 1):
            pivot = M[k][k]
            if abs(pivot) < 1e-12:
                raise ValueError(
                    f"Pivote cero (o casi cero) en la fila {k}. "
                    "Use un método con pivoteo."
                )

            steps.append({
                "step": len(steps) + 1,
                "phase": "elimination",
                "description": f"Pivote en posición ({k},{k}) = {pivot:.6g}",
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
                    "description": (
                        f"F{i+1} ← F{i+1} - ({factor:.6g})·F{k+1}  →  "
                        f"Se elimina M[{i}][{k}]"
                    ),
                    "factor": factor,
                    "matrix_state": self._snapshot(M),
                })

        # --- Sustitución regresiva ---
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            if abs(M[i][i]) < 1e-12:
                raise ValueError(f"Sistema singular: pivote cero en fila {i} durante sustitución regresiva.")
            s = sum(M[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (M[i][n] - s) / M[i][i]

            steps.append({
                "step": len(steps) + 1,
                "phase": "back_substitution",
                "description": f"x[{i}] = ({M[i][n]:.6g} - {s:.6g}) / {M[i][i]:.6g} = {x[i]:.6g}",
                "matrix_state": self._snapshot(M),
            })

        return {
            "solution": x,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
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
