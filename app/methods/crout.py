"""
Factorización LU mediante el Método de Crout.
U tiene unos en la diagonal principal.
"""
from app.core.base_method import NumericalMethod

class Crout(NumericalMethod):
    @property
    def name(self) -> str:
        return "crout"

    @property
    def description(self) -> str:
        return "Factorización LU (Crout)"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese una matriz cuadrada <code>A</code> y el vector <code>b</code>.</li>"
                "<li>Calcula L y U (donde U tiene unos en su diagonal principal).</li>"
                "<li>Resuelve Lz = b y Ux = z.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter a square matrix <code>A</code> and vector <code>b</code>.</li>"
                "<li>Calculates L and U (where U has ones on its main diagonal).</li>"
                "<li>Solves Lz = b and Ux = z.</li>"
                "</ul>"
            ),
        }

    def solve(self, A: list, b: list) -> dict:
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        for i in range(n):
            U[i][i] = 1.0
            
        steps = []
        
        for k in range(n):
            # Calcular columna k de L
            for i in range(k, n):
                sum_k = sum(L[i][j] * U[j][k] for j in range(k))
                L[i][k] = A[i][k] - sum_k
                
            if abs(L[k][k]) < 1e-12:
                raise ValueError(f"Fallo en Crout: L[{k}][{k}] es cercano a cero.")

            # Calcular fila k de U
            for j in range(k + 1, n):
                sum_k = sum(L[k][i] * U[i][j] for i in range(k))
                U[k][j] = (A[k][j] - sum_k) / L[k][k]
                
            steps.append({
                "step": len(steps) + 1,
                "phase": "elimination",
                "description": f"Paso {k+1}: Construcción de columna {k+1} de L y fila {k+1} de U",
                "matrix_state": self._snapshot(L)
            })

        steps.append({
            "step": len(steps) + 1,
            "phase": "extract",
            "description": "Factorización L y U (Crout) completada.",
            "matrix_state": self._snapshot(L)
        })

        # Forward substitution: Lz = b
        z = [0.0] * n
        for i in range(n):
            s = sum(L[i][j] * z[j] for j in range(i))
            z[i] = (b[i] - s) / L[i][i]
            steps.append({
                "step": len(steps) + 1,
                "phase": "forward_sweep",
                "description": f"z[{i+1}] = {z[i]:.6g}"
            })

        # Backward substitution: Ux = z
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            s = sum(U[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (z[i] - s) / U[i][i]
            steps.append({
                "step": len(steps) + 1,
                "phase": "back_substitution",
                "description": f"x[{i+1}] = {x[i]:.6g}"
            })

        return {
            "solution": x,
            "L": L,
            "U": U,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
