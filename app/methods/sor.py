"""
Método Iterativo SOR (Successive Over-Relaxation)
"""
import math
from app.core.base_method import NumericalMethod


class SOR(NumericalMethod):
    @property
    def name(self) -> str:
        return "sor"

    @property
    def description(self) -> dict:
        return {"es": "Método Iterativo SOR (Relajación)", "en": "SOR Iterative Method (Relaxation)"}

    @property
    def plot_type(self) -> str:
        return "iterative_matrix"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese la matriz <code>A</code> y el vector <code>b</code>.</li>"
                "<li>Especifique omega (ω), tolerancia, vector inicial y límite de iteraciones.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter matrix <code>A</code> and vector <code>b</code>.</li>"
                "<li>Specify omega (ω), tolerance, initial vector and iteration limit.</li>"
                "</ul>"
            ),
        }
        
    @property
    def params_schema(self) -> list:
        return [
            {"key": "w", "label_es": "Omega (ω)", "label_en": "Omega (ω)", "type": "number", "default": 1.5},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "number", "default": 0.0001},
            {"key": "max_iter", "label_es": "Iteraciones Max", "label_en": "Max Iterations", "type": "number", "default": 100},
            {"key": "x0", "label_es": "Vector Inicial (x0)", "label_en": "Initial Vector (x0)", "type": "text", "default": "0,0,0"}
        ]

    def solve(self, A: list, b: list, params: dict = None) -> dict:
        params = params or {}

        # ── Parse parameters ──────────────────────────────────────────
        try:
            w = float(params.get("w", 1.5))
            tol = float(params.get("tol", 1e-4))
            max_iter = int(params.get("max_iter", 100))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid parameter: {e}") from e
        if tol <= 0:
            raise ValueError("Tolerance must be positive.")
        if max_iter <= 0:
            raise ValueError("max_iter must be a positive integer.")
        if not (0 < w < 2):
            raise ValueError(
                f"Relaxation parameter ω = {w} is out of range. "
                "SOR converges only when 0 < ω < 2. "
                "Typical values: ω = 1.0 (Gauss-Seidel), 1.0 < ω < 2.0 (over-relaxation)."
            )

        x0_str = params.get("x0", "0")
        n = len(A)

        # ── Validate matrix ──────────────────────────────────────────
        if n == 0:
            raise ValueError("Matrix A is empty.")
        if len(b) != n:
            raise ValueError(
                f"Matrix A has {n} rows but b has {len(b)} elements. "
                "The system must be square."
            )
        try:
            A = [[float(v) for v in row] for row in A]
            b = [float(v) for v in b]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Non-numeric value in A or b: {e}") from e
        for i, row in enumerate(A):
            if len(row) != n:
                raise ValueError(f"Row {i} of A has {len(row)} elements, expected {n}.")

        # ── Parse initial vector ─────────────────────────────────────
        try:
            x0 = [float(xi.strip()) for xi in str(x0_str).split(',')]
            if len(x0) == 1 and n > 1:
                x0 = [x0[0]] * n
            elif len(x0) != n:
                raise ValueError(f"Expected {n} values, got {len(x0)}.")
        except (ValueError, AttributeError) as e:
            raise ValueError(
                f"Invalid initial vector x0: '{x0_str}'. "
                f"Provide {n} comma-separated numbers (e.g., '0,0,0')."
            ) from e

        # ── Check diagonal ──────────────────────────────────────────
        for i in range(n):
            if abs(A[i][i]) < 1e-12:
                raise ValueError(
                    f"Zero diagonal element at A[{i}][{i}] = {A[i][i]:.2e}. "
                    "SOR requires all diagonal elements to be non-zero."
                )


        x = x0[:]
        steps = []

        steps.append({
            "step": 0,
            "phase": "analysis",
            "description": f"Valores iniciales: x = {self._snapshot(x)}, w = {w}"
        })

        try:
            for k in range(max_iter):
                x_old = x[:]
                error = 0.0
                
                for i in range(n):
                    s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                    x_new_i = (b[i] - s) / A[i][i]
                    x[i] = (1 - w) * x_old[i] + w * x_new_i
                    
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
        except OverflowError:
            raise ValueError(
                f"Desbordamiento numérico (Overflow) en la iteración {k+1}. "
                "El método divergió. Verifica que la matriz sea diagonalmente dominante y ω adecuado."
            )
        except ZeroDivisionError:
            raise ValueError(f"División por cero en la iteración {k+1}.")

        props = {}
        try:
            import numpy as np
            A_np = np.array(A)
            D = np.diag(np.diag(A_np))
            L = np.tril(A_np, -1)
            U = np.triu(A_np, 1)
            D_wL_inv = np.linalg.inv(D + w * L)
            Tw = np.dot(D_wL_inv, ((1 - w) * D - w * U))
            eigenvalues = np.linalg.eigvals(Tw)
            spectral_radius = np.max(np.abs(eigenvalues))
            
            props["Radio Espectral (ρ)"] = f"{spectral_radius:.6g}"
            props["Convergencia"] = "Garantizada (ρ < 1)" if spectral_radius < 1 else "No garantizada (ρ >= 1)"
            
            Tw_str = "[" + "]\n[".join([", ".join([f"{v:.4f}" for v in row]) for row in Tw]) + "]"
            props["Matriz de Transición Tw"] = Tw_str
        except Exception as e:
            pass

        return {
            "solution": x,
            "properties": props,
            "steps": steps,
            "iterations": len(steps) - 1,
            "method": self.name,
            "plot_type": self.plot_type,
        }
