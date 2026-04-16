"""
Eliminación Gaussiana con Pivoteo Parcial y Pivoteo Total.

Dos clases que heredan de NumericalMethod:
- GaussianPartialPivoting: intercambia filas (máximo en columna).
- GaussianTotalPivoting: intercambia filas Y columnas (máximo en submatriz).
"""
from app.core.base_method import NumericalMethod


class GaussianPartialPivoting(NumericalMethod):

    @property
    def name(self) -> str:
        return "gaussian_partial_pivoting"

    @property
    def description(self) -> str:
        return "Eliminación Gaussiana con Pivoteo Parcial"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese el sistema de ecuaciones. Antes de cada paso de eliminación, el algoritmo buscará el valor absoluto mayor en la columna actual.</li>"
                "<li>Si ese valor no está en la fila pivote actual, intercambiará las filas pertinentes.</li>"
                "<li>💡 <strong>Ventaja:</strong> Evita la división por cero y reduce significativamente los errores de redondeo comparado con la Gaussiana Simple.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter the system of equations. Before each elimination step, the algorithm will search for the largest absolute value in the current column.</li>"
                "<li>If that value is not in the current pivot row, it will swap the relevant rows.</li>"
                "<li>💡 <strong>Advantage:</strong> Avoids division by zero and significantly reduces rounding errors compared to Simple Gaussian.</li>"
                "</ul>"
            ),
        }

    def solve(self, A: list, b: list) -> dict:
        n = len(b)
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        steps = []

        for k in range(n - 1):
            # Buscar pivote máximo en columna k (filas k..n-1)
            max_val = abs(M[k][k])
            max_row = k
            for i in range(k + 1, n):
                if abs(M[i][k]) > max_val:
                    max_val = abs(M[i][k])
                    max_row = i

            # Intercambiar filas si necesario
            swap_info = None
            if max_row != k:
                M[k], M[max_row] = M[max_row], M[k]
                swap_info = [k, max_row]

            pivot = M[k][k]
            if abs(pivot) < 1e-12:
                raise ValueError(
                    f"Sistema singular: pivote cero en columna {k} incluso después de pivoteo parcial."
                )

            step_data = {
                "step": len(steps) + 1,
                "phase": "elimination",
                "description": f"Pivote parcial en columna {k}: valor = {pivot:.6g}",
                "pivot": pivot,
                "swap_rows": swap_info,
                "matrix_state": self._snapshot(M),
            }
            steps.append(step_data)

            # Eliminación
            for i in range(k + 1, n):
                factor = M[i][k] / pivot
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]

                steps.append({
                    "step": len(steps) + 1,
                    "phase": "elimination",
                    "description": f"F{i+1} ← F{i+1} - ({factor:.6g})·F{k+1}",
                    "factor": factor,
                    "matrix_state": self._snapshot(M),
                })

        # Sustitución regresiva
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            if abs(M[i][i]) < 1e-12:
                raise ValueError(f"Sistema singular en sustitución regresiva (fila {i}).")
            s = sum(M[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (M[i][n] - s) / M[i][i]
            steps.append({
                "step": len(steps) + 1,
                "phase": "back_substitution",
                "description": f"x[{i}] = {x[i]:.6g}",
                "matrix_state": self._snapshot(M),
            })

        return {
            "solution": x,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }


class GaussianTotalPivoting(NumericalMethod):

    @property
    def name(self) -> str:
        return "gaussian_total_pivoting"

    @property
    def description(self) -> str:
        return "Eliminación Gaussiana con Pivoteo Total"

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Este método busca el valor absoluto máximo no solo en la columna actual, sino en toda la submatriz restante.</li>"
                "<li>Puede intercambiar tanto <strong>filas como columnas</strong> para posicionar el pivote.</li>"
                "<li>💡 <strong>Ventaja:</strong> Ofrece la mayor estabilidad numérica entre todos los métodos de eliminación directa.</li>"
                "<li>El orden de las incógnitas cambiará durante el proceso, pero el sistema reordena la solución final automáticamente.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>This method searches for the maximum absolute value not only in the current column, but in the entire remaining submatrix.</li>"
                "<li>It can swap both <strong>rows and columns</strong> to position the pivot.</li>"
                "<li>💡 <strong>Advantage:</strong> Offers the highest numerical stability among all direct elimination methods.</li>"
                "<li>The order of unknowns will change during the process, but the system automatically reorders the final solution.</li>"
                "</ul>"
            ),
        }

    def solve(self, A: list, b: list) -> dict:
        n = len(b)
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        # Vector de permutación de columnas para reordenar la solución
        col_order = list(range(n))
        steps = []

        for k in range(n - 1):
            # Buscar máximo absoluto en submatriz M[k:, k:n]
            max_val = abs(M[k][k])
            max_row, max_col = k, k
            for i in range(k, n):
                for j in range(k, n):
                    if abs(M[i][j]) > max_val:
                        max_val = abs(M[i][j])
                        max_row = i
                        max_col = j

            # Intercambiar filas
            row_swap = None
            if max_row != k:
                M[k], M[max_row] = M[max_row], M[k]
                row_swap = [k, max_row]

            # Intercambiar columnas (solo las primeras n columnas, no la aumentada)
            col_swap = None
            if max_col != k:
                for row in M:
                    row[k], row[max_col] = row[max_col], row[k]
                col_order[k], col_order[max_col] = col_order[max_col], col_order[k]
                col_swap = [k, max_col]

            pivot = M[k][k]
            if abs(pivot) < 1e-12:
                raise ValueError(
                    f"Sistema singular: pivote cero en paso {k} incluso después de pivoteo total."
                )

            steps.append({
                "step": len(steps) + 1,
                "phase": "elimination",
                "description": f"Pivote total en paso {k}: valor = {pivot:.6g}",
                "pivot": pivot,
                "max_val": max_val,
                "swap_rows": row_swap,
                "swap_cols": col_swap,
                "matrix_state": self._snapshot(M),
            })

            # Eliminación
            for i in range(k + 1, n):
                factor = M[i][k] / pivot
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]

                steps.append({
                    "step": len(steps) + 1,
                    "phase": "elimination",
                    "description": f"F{i+1} ← F{i+1} - ({factor:.6g})·F{k+1}",
                    "factor": factor,
                    "matrix_state": self._snapshot(M),
                })

        # Sustitución regresiva (resultado en orden permutado)
        x_perm = [0.0] * n
        for i in range(n - 1, -1, -1):
            if abs(M[i][i]) < 1e-12:
                raise ValueError(f"Sistema singular en sustitución regresiva (fila {i}).")
            s = sum(M[i][j] * x_perm[j] for j in range(i + 1, n))
            x_perm[i] = (M[i][n] - s) / M[i][i]
            steps.append({
                "step": len(steps) + 1,
                "phase": "back_substitution",
                "description": f"x_perm[{i}] = {x_perm[i]:.6g}",
                "matrix_state": self._snapshot(M),
            })

        # Reordenar la solución según la permutación de columnas
        x = [0.0] * n
        for i in range(n):
            x[col_order[i]] = x_perm[i]

        steps.append({
            "step": len(steps) + 1,
            "phase": "reorder",
            "description": f"Reordenamiento de columnas: {col_order} → solución final",
            "col_permutation": col_order[:],
            "matrix_state": self._snapshot(M),
        })

        return {
            "solution": x,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }


if __name__ == "__main__":
    # Caso con pivote cero: requiere pivoteo
    A = [[0, 2, 1], [1, -2, -3], [-1, 1, 2]]
    b_vec = [1, 1, 1]

    print("--- Pivoteo Parcial ---")
    r1 = GaussianPartialPivoting().solve(A, b_vec)
    print("Solución:", r1["solution"])

    print("\n--- Pivoteo Total ---")
    r2 = GaussianTotalPivoting().solve(A, b_vec)
    print("Solución:", r2["solution"])
