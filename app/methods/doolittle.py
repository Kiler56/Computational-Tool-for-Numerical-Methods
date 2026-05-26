"""
Factorización LU mediante el Método de Doolittle.
=================================================

Descompone una matriz A en:

    A = L * U

donde:

- L es triangular inferior con unos en la diagonal.
- U es triangular superior.

Además:

1. Resuelve el sistema:
       Lz = b
2. Luego resuelve:
       Ux = z

Modificación aplicada:
✔ La salida ahora renderiza por separado:
    - Matriz L
    - Matriz U

✔ Se eliminó la visualización de la matriz combinada.
"""

from app.core.base_method import NumericalMethod


class Doolittle(NumericalMethod):

    # ── Metadata ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "doolittle"

    @property
    def description(self) -> dict:
        return {"es": "Factorización LU (Doolittle)", "en": "LU Factorization (Doolittle)"}

    @property
    def plot_type(self) -> str:
        return "lu_factorization"

    @property
    def instructions(self) -> dict:

        return {

            "es": (
                "<ul><li>Ingrese una matriz cuadrada <code>A</code> y el vector <code>b</code>.</li><li>El método calcula las matrices <code>L</code> y <code>U</code>.</li><li>La matriz <code>L</code> tiene unos en su diagonal principal.</li><li>Primero se resuelve <code>Lz = b</code>.</li><li>Luego se resuelve <code>Ux = z</code>.</li></ul>"
            ),

            "en": (
                "<ul>"
                "<li>Enter a square matrix <code>A</code> and vector <code>b</code>.</li>"
                "<li>The method computes matrices <code>L</code> and <code>U</code>.</li>"
                "<li>Matrix <code>L</code> has ones on its main diagonal.</li>"
                "<li>First solve <code>Lz = b</code>.</li>"
                "<li>Then solve <code>Ux = z</code>.</li>"
                "</ul>"
            ),

        }

    # ── Main Solve Method ────────────────────────────────────────────────────

    def solve(self, A: list, b: list) -> dict:

        n = len(A)

        # Initialize matrices
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]

        # L diagonal = 1
        for i in range(n):
            L[i][i] = 1.0

        steps = []

        # ── LU Factorization ────────────────────────────────────────────────

        for k in range(n):

            # Compute row k of U
            for j in range(k, n):

                sum_k = sum(
                    L[k][i] * U[i][j]
                    for i in range(k)
                )

                U[k][j] = A[k][j] - sum_k

            # Zero pivot validation
            if abs(U[k][k]) < 1e-12:

                raise ValueError(
                    f"Fallo en Doolittle: "
                    f"U[{k}][{k}] es cercano a cero."
                )

            # Compute column k of L
            for i in range(k + 1, n):

                sum_k = sum(
                    L[i][j] * U[j][k]
                    for j in range(k)
                )

                L[i][k] = (
                    A[i][k] - sum_k
                ) / U[k][k]

            # ── Separate rendering of L and U ──────────────────────────────

            steps.append({

                "step": len(steps) + 1,

                "phase": "factorization",

                "description": {"es": (
                    f"Paso {k + 1}: "
                    f"Construcción de fila {k + 1} de U "
                    f"y columna {k + 1} de L."
                ), "en": (
                    f"Paso {k + 1}: "
                    f"Construcción de fila {k + 1} de U "
                    f"y columna {k + 1} de L."
                )},

                # Separate matrices
                "L_matrix": [row[:] for row in L],

                "U_matrix": [row[:] for row in U],

            })

        # ── Final LU Result ────────────────────────────────────────────────

        steps.append({

            "step": len(steps) + 1,

            "phase": "result",

            "description": {"es": (
                "Factorización LU (Doolittle) completada."
            ), "en": (
                "LU (Doolittle) factorization completed."
            )},

            "L_matrix": [row[:] for row in L],

            "U_matrix": [row[:] for row in U],

        })

        # ── Forward Substitution: Lz = b ───────────────────────────────────

        z = [0.0] * n

        for i in range(n):

            s = sum(
                L[i][j] * z[j]
                for j in range(i)
            )

            z[i] = (
                b[i] - s
            ) / L[i][i]

            steps.append({

                "step": len(steps) + 1,

                "phase": "forward_substitution",

                "description": {"es": (
                    f"z[{i + 1}] = {z[i]:.10g}"
                ), "en": (
                    f"z[{i + 1}] ={z[i]:.10g}"
                )},

                "z_vector": z[:]

            })

        # ── Back Substitution: Ux = z ──────────────────────────────────────

        x = [0.0] * n

        for i in range(n - 1, -1, -1):

            s = sum(
                U[i][j] * x[j]
                for j in range(i + 1, n)
            )

            x[i] = (
                z[i] - s
            ) / U[i][i]

            steps.append({

                "step": len(steps) + 1,

                "phase": "back_substitution",

                "description": {"es": (
                    f"x[{i + 1}] = {x[i]:.10g}"
                ), "en": (
                    f"x[{i + 1}] ={x[i]:.10g}"
                )},

                "x_vector": x[:]

            })

        # ── Properties for UI ──────────────────────────────────────────────

        props = {

            "Matrix size": str(n),

            "Factorization": "A = L · U",

            "L diagonal": "1",

            "Solution vector": (
                ", ".join(f"{v:.6g}" for v in x)
            )

        }

        # ── Final Response ─────────────────────────────────────────────────

        return {

            "solution": x,

            # Final matrices separated
            "L": L,

            "U": U,

            "properties": props,

            "steps": steps,

            "iterations": len(steps),

            "method": self.name,

            "plot_type": self.plot_type,

        }