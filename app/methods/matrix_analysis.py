"""
Análisis de Matrices: Determinante, Diagonalmente Dominante, Definida Positiva.
"""
from app.core.base_method import NumericalMethod
import copy

class MatrixAnalysis(NumericalMethod):

    @property
    def name(self) -> str:
        return "matrix_analysis"

    @property
    def description(self) -> str:
        return "Análisis de Propiedades de Matriz"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese una matriz cuadrada <code>A</code>. El vector <code>b</code> será ignorado pero debe llenarlo con cualquier valor.</li>"
                "<li>Calcula el determinante de la matriz.</li>"
                "<li>Verifica si es Estrictamente Diagonal Dominante.</li>"
                "<li>Verifica si es Definida Positiva.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter a square matrix <code>A</code>. Vector <code>b</code> will be ignored but you must fill it.</li>"
                "<li>Calculates the determinant of the matrix.</li>"
                "<li>Checks if it is Strictly Diagonally Dominant.</li>"
                "<li>Checks if it is Positive Definite.</li>"
                "</ul>"
            ),
        }

    def _determinant(self, A):
        n = len(A)
        M = copy.deepcopy(A)
        det = 1.0
        for k in range(n - 1):
            max_val = abs(M[k][k])
            max_row = k
            for i in range(k + 1, n):
                if abs(M[i][k]) > max_val:
                    max_val = abs(M[i][k])
                    max_row = i
            
            if max_row != k:
                M[k], M[max_row] = M[max_row], M[k]
                det *= -1.0
            
            pivot = M[k][k]
            if abs(pivot) < 1e-12:
                return 0.0
            det *= pivot
            
            for i in range(k + 1, n):
                factor = M[i][k] / pivot
                for j in range(k, n):
                    M[i][j] -= factor * M[k][j]
        det *= M[n-1][n-1]
        return det

    def _is_strictly_diagonally_dominant(self, A):
        n = len(A)
        for i in range(n):
            diagonal_val = abs(A[i][i])
            row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
            if diagonal_val <= row_sum:
                return False
        return True

    def _is_positive_definite(self, A):
        n = len(A)
        for i in range(n):
            for j in range(i+1, n):
                if abs(A[i][j] - A[j][i]) > 1e-10:
                    return False
                    
        for k in range(1, n + 1):
            submatrix = [row[:k] for row in A[:k]]
            det = self._determinant(submatrix)
            if det <= 0:
                return False
        return True

    def solve(self, A: list, b: list) -> dict:
        det = self._determinant(A)
        is_edd = self._is_strictly_diagonally_dominant(A)
        is_pd = self._is_positive_definite(A)
        
        props = {
            "Determinante": f"{det:.6g}",
            "Estrictamente Diagonal Dominante": "Sí" if is_edd else "No",
            "Definida Positiva": "Sí" if is_pd else "No"
        }
        
        steps = [{
            "step": 1,
            "phase": "analysis",
            "description": "Cálculo de propiedades de la matriz.",
            "matrix_state": self._snapshot(A)
        }]

        return {
            "solution": [],
            "properties": props,
            "steps": steps,
            "iterations": 1,
            "method": self.name,
        }
