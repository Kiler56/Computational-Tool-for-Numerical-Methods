"""
Factorización LU mediante el Método de Cholesky.
A = L * U (donde U = L^T).
Requiere que la matriz sea Simétrica y Definida Positiva.
"""
from app.core.base_method import NumericalMethod
import math

class Cholesky(NumericalMethod):

    @property
    def name(self) -> str:
        return "cholesky"

    @property
    def description(self) -> str:
        return "Factorización LU (Cholesky)"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese una matriz cuadrada <code>A</code> y el vector <code>b</code>.</li>"
                "<li>La matriz debe ser <strong>Simétrica y Definida Positiva</strong>.</li>"
                "<li>Calcula L y U (donde U = L^T) y luego resuelve Lz = b y Ux = z.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter a square matrix <code>A</code> and vector <code>b</code>.</li>"
                "<li>The matrix must be <strong>Symmetric and Positive Definite</strong>.</li>"
                "<li>Calculates L and U (where U = L^T) and then solves Lz = b and Ux = z.</li>"
                "</ul>"
            ),
        }

    def solve(self, A: list, b: list) -> dict:
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        steps = []
        
        # Propiedades de la matriz (para el quiz)
        from app.methods.matrix_analysis import MatrixAnalysis
        analyzer = MatrixAnalysis()
        det = analyzer._determinant(A)
        is_edd = analyzer._is_strictly_diagonally_dominant(A)
        is_pd = analyzer._is_positive_definite(A)
        
        props = {
            "Determinante": f"{det:.6g}",
            "Estrictamente Diagonal Dominante": "Sí" if is_edd else "No",
            "Definida Positiva": "Sí" if is_pd else "No"
        }

        # Verificación de simetría
        for i in range(n):
            for j in range(i+1, n):
                if abs(A[i][j] - A[j][i]) > 1e-10:
                    raise ValueError("El método de Cholesky requiere una matriz simétrica.")

        if not is_pd:
            steps.append({
                "step": len(steps) + 1,
                "phase": "analysis",
                "description": "ADVERTENCIA: La matriz no es definida positiva según el criterio de Sylvester. Cholesky puede fallar.",
            })

        # Construcción de L y U
        for i in range(n):
            for j in range(i + 1):
                sum_k = sum(L[i][k] * L[j][k] for k in range(j))
                
                if i == j: # Diagonal de L
                    val = A[i][i] - sum_k
                    if val <= 0:
                        raise ValueError(f"Fallo en Cholesky: elemento (A[{i}][{i}] - sum) = {val:.6g} <= 0. La matriz no es definida positiva.")
                    L[i][i] = math.sqrt(val)
                    U[i][i] = L[i][i]
                else:
                    L[i][j] = (A[i][j] - sum_k) / L[j][j]
                    U[j][i] = L[i][j]
            
            steps.append({
                "step": len(steps) + 1,
                "phase": "elimination",
                "description": f"Cálculo de fila {i+1} de L y columna {i+1} de U",
                "matrix_state": self._snapshot(L)
            })
            
        steps.append({
            "step": len(steps) + 1,
            "phase": "extract",
            "description": "Factorización L y U completada.",
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
            "properties": props,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
