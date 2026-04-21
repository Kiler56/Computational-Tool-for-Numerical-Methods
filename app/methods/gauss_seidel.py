"""
Método Iterativo de Gauss-Seidel para Sistemas Lineales
"""
from app.core.base_method import NumericalMethod

class GaussSeidel(NumericalMethod):
    @property
    def name(self) -> str:
        return "gauss_seidel"

    @property
    def description(self) -> str:
        return "Método Iterativo de Gauss-Seidel"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese la matriz <code>A</code> y el vector <code>b</code>.</li>"
                "<li>Configure la tolerancia, el vector inicial y el máximo de iteraciones.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter matrix <code>A</code> and vector <code>b</code>.</li>"
                "<li>Set the tolerance, initial vector, and maximum iterations.</li>"
                "</ul>"
            ),
        }
        
    @property
    def params_schema(self) -> list:
        return [
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "number", "default": 0.0001},
            {"key": "max_iter", "label_es": "Iteraciones Max", "label_en": "Max Iterations", "type": "number", "default": 100},
            {"key": "x0", "label_es": "Vector Inicial (x0)", "label_en": "Initial Vector (x0)", "type": "text", "default": "0,0,0"}
        ]

    def solve(self, A: list, b: list, params: dict = None) -> dict:
        params = params or {}
        tol = float(params.get("tol", 1e-4))
        max_iter = int(params.get("max_iter", 100))
        x0_str = params.get("x0", "0")
        
        n = len(A)
        try:
            x0 = [float(x.strip()) for x in x0_str.split(',')]
            if len(x0) == 1 and n > 1:
                x0 = [x0[0]] * n
            elif len(x0) != n:
                raise ValueError
        except:
            raise ValueError(f"El vector inicial debe ser una lista de {n} números separados por coma.")
            
        x = x0[:]
        steps = []
        
        for i in range(n):
            if abs(A[i][i]) < 1e-12:
                raise ValueError(f"Fallo en Gauss-Seidel: el elemento diagonal A[{i}][{i}] es cero.")

        steps.append({
            "step": 0,
            "phase": "analysis",
            "description": f"Valores iniciales: x = {self._snapshot(x)}"
        })

        for k in range(max_iter):
            x_old = x[:]
            error = 0.0
            
            for i in range(n):
                s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x[i] = (b[i] - s) / A[i][i]
                
            error = max(abs(x[i] - x_old[i]) for i in range(n))
            
            desc = f"Iteración {k+1}: x = [" + ", ".join(f"{v:.6g}" for v in x) + f"], Error = {error:.6g}"
            steps.append({
                "step": k + 1,
                "phase": "elimination",
                "description": desc
            })
            
            if error < tol:
                break
                
        if error >= tol:
            steps.append({
                "step": max_iter + 1,
                "phase": "analysis",
                "description": "ADVERTENCIA: El método no convergió."
            })

        return {
            "solution": x,
            "steps": steps,
            "iterations": len(steps) - 1,
            "method": self.name,
        }
