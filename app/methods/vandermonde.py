"""
Método de Interpolación de Vandermonde
=======================================
Construye la matriz de Vandermonde V a partir de n puntos (x_i, y_i) y resuelve
el sistema lineal V·a = y usando Eliminación Gaussiana con Pivoteo Total para
obtener los coeficientes del polinomio interpolante:

    p(x) = a_0 + a_1·x + a_2·x² + … + a_{n-1}·x^{n-1}

Implementado por: Andrés Yue — rama feature/vandermonde-simpson38
"""
from app.core.base_method import NumericalMethod


class VandermondeInterpolation(NumericalMethod):

    # ── Metadatos ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "vandermonde"

    @property
    def description(self) -> str:
        return "Interpolación de Vandermonde"

    @property
    def method_type(self) -> str:
        return "interpolation"

    @property
    def params_schema(self) -> list:
        return [
            {
                "key": "eval_x",
                "label_es": "Evaluar p(x) en x =",
                "label_en": "Evaluate p(x) at x =",
                "type": "float",
                "default": 0,
                "required": False,
            }
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese los puntos (x, y) que desea interpolar. Los x deben ser únicos.</li>"
                "<li>El método construye la <strong>matriz de Vandermonde</strong> V donde V<sub>ij</sub> = x<sub>i</sub><sup>j</sup>.</li>"
                "<li>Se resuelve V·<b>a</b> = <b>y</b> con <strong>Eliminación Gaussiana con Pivoteo Total</strong> para mayor estabilidad numérica.</li>"
                "<li>Retorna los coeficientes a<sub>0</sub>, a<sub>1</sub>, …, a<sub>n-1</sub> del polinomio p(x).</li>"
                "<li>Opcionalmente ingrese un valor x para evaluar p(x).</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter the (x, y) points to interpolate. All x values must be unique.</li>"
                "<li>The method builds the <strong>Vandermonde matrix</strong> V where V<sub>ij</sub> = x<sub>i</sub><sup>j</sup>.</li>"
                "<li>The system V·<b>a</b> = <b>y</b> is solved with <strong>Gaussian Elimination with Total Pivoting</strong> for maximum numerical stability.</li>"
                "<li>Returns coefficients a<sub>0</sub>, a<sub>1</sub>, …, a<sub>n-1</sub> of polynomial p(x).</li>"
                "<li>Optionally provide an x value to evaluate p(x).</li>"
                "</ul>"
            ),
        }

    # ── Kernel numérico ───────────────────────────────────────────────────────

    @staticmethod
    def _build_vandermonde(x_points: list, n: int) -> list:
        """Construye la matriz de Vandermonde n×n.
        Fila i → [1, x_i, x_i², …, x_i^{n-1}]
        """
        V = []
        for xi in x_points:
            row = [float(xi) ** j for j in range(n)]
            V.append(row)
        return V

    @staticmethod
    def _gauss_total_pivot(A: list, b: list):
        """Eliminación Gaussiana con Pivoteo Total (in-place).
        Devuelve (solución, pasos, vector de permutación de columnas).
        """
        n = len(b)
        # Matriz aumentada [A | b]
        M = [A[i][:] + [float(b[i])] for i in range(n)]
        col_order = list(range(n))   # permutación de columnas
        steps = []

        for k in range(n - 1):
            # Buscar el máximo absoluto en la submatriz M[k:n, k:n]
            max_val = 0.0
            max_r, max_c = k, k
            for r in range(k, n):
                for c in range(k, n):
                    if abs(M[r][c]) > max_val:
                        max_val = abs(M[r][c])
                        max_r, max_c = r, c

            # Intercambio de filas
            row_swap = None
            if max_r != k:
                M[k], M[max_r] = M[max_r], M[k]
                row_swap = [k + 1, max_r + 1]   # 1-indexed para display

            # Intercambio de columnas (sólo en las primeras n cols, no la aumentada)
            col_swap = None
            if max_c != k:
                for row in M:
                    row[k], row[max_c] = row[max_c], row[k]
                col_order[k], col_order[max_c] = col_order[max_c], col_order[k]
                col_swap = [k, max_c]

            pivot = M[k][k]
            if abs(pivot) < 1e-14:
                raise ValueError(
                    f"Sistema singular: pivote ≈ 0 en el paso {k + 1}. "
                    "Los puntos x pueden estar demasiado cerca o repetidos."
                )

            steps.append({
                "step": len(steps) + 1,
                "phase": "pivot",
                "description": (
                    f"Paso {k + 1}: pivote total = {pivot:.6g}"
                    + (f" | intercambio filas F{row_swap[0]}↔F{row_swap[1]}" if row_swap else "")
                    + (f" | intercambio cols C{col_swap[0]+1}↔C{col_swap[1]+1}" if col_swap else "")
                ),
                "pivot": pivot,
                "swap_rows": row_swap,
                "swap_cols": col_swap,
                "matrix_state": [r[:] for r in M],
            })

            # Eliminación
            for i in range(k + 1, n):
                if abs(M[k][k]) < 1e-14:
                    continue
                factor = M[i][k] / M[k][k]
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]
                M[i][k] = 0.0

                steps.append({
                    "step": len(steps) + 1,
                    "phase": "elimination",
                    "description": f"F{i+1} ← F{i+1} - ({factor:.6g})·F{k+1}",
                    "factor": factor,
                    "matrix_state": [r[:] for r in M],
                })

        # Sustitución regresiva
        x_perm = [0.0] * n
        for i in range(n - 1, -1, -1):
            if abs(M[i][i]) < 1e-14:
                raise ValueError(f"Sistema singular en sustitución regresiva (fila {i + 1}).")
            s = sum(M[i][j] * x_perm[j] for j in range(i + 1, n))
            x_perm[i] = (M[i][n] - s) / M[i][i]
            steps.append({
                "step": len(steps) + 1,
                "phase": "back_substitution",
                "description": f"a_perm[{i}] = ({M[i][n]:.6g} - suma) / {M[i][i]:.6g} = {x_perm[i]:.8g}",
                "value": x_perm[i],
                "matrix_state": [r[:] for r in M],
            })

        # Reordenar coeficientes según permutación de columnas
        coeffs = [0.0] * n
        for i in range(n):
            coeffs[col_order[i]] = x_perm[i]

        steps.append({
            "step": len(steps) + 1,
            "phase": "reorder",
            "description": f"Reordenamiento de columnas {col_order} → coeficientes finales: {[f'{c:.6g}' for c in coeffs]}",
            "col_permutation": col_order[:],
            "coefficients": coeffs[:],
            "matrix_state": [r[:] for r in M],
        })

        return coeffs, steps

    @staticmethod
    def _eval_poly(coeffs: list, x: float) -> float:
        """Evalúa p(x) usando el esquema de Horner para mayor estabilidad."""
        result = 0.0
        for c in reversed(coeffs):
            result = result * x + c
        return result

    @staticmethod
    def _poly_to_str(coeffs: list) -> str:
        """Genera la cadena legible del polinomio."""
        terms = []
        for i, c in enumerate(coeffs):
            if abs(c) < 1e-12:
                continue
            sign = "+" if c >= 0 else "-"
            val = abs(c)
            if i == 0:
                terms.append(f"{c:.6g}")
            elif i == 1:
                terms.append(f"{sign} {val:.6g}x")
            else:
                terms.append(f"{sign} {val:.6g}x^{i}")
        if not terms:
            return "p(x) = 0"
        poly = terms[0]
        for t in terms[1:]:
            poly += f" {t}"
        return f"p(x) = {poly}"

    # ── Punto de entrada público ───────────────────────────────────────────────

    def solve(self, x_points: list, y_points: list, params: dict = None) -> dict:
        params = params or {}
        n = len(x_points)

        # ── Validaciones ──────────────────────────────────────────────────────
        if len(y_points) != n:
            raise ValueError("Las listas X e Y deben tener el mismo tamaño.")
        if n < 2:
            raise ValueError("Se necesitan al menos 2 puntos para interpolar.")
        if len(set(float(x) for x in x_points)) != n:
            raise ValueError("Todos los valores X deben ser únicos.")

        x_f = [float(v) for v in x_points]
        y_f = [float(v) for v in y_points]

        steps = []

        # ── Paso 1: Construcción de la matriz de Vandermonde ──────────────────
        V = self._build_vandermonde(x_f, n)
        steps.append({
            "step": 1,
            "phase": "build_matrix",
            "description": (
                f"Construcción de la matriz de Vandermonde {n}×{n}. "
                f"V[i][j] = x_i^j  →  x = {x_f}"
            ),
            "matrix_state": [row[:] + [y_f[i]] for i, row in enumerate(V)],
        })

        # ── Paso 2: Resolución con Pivoteo Total ──────────────────────────────
        try:
            coeffs, gauss_steps = self._gauss_total_pivot(V, y_f)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

        # Renumerar pasos desde 2
        for i, s in enumerate(gauss_steps):
            s["step"] = i + 2
        steps.extend(gauss_steps)

        # ── Paso 3: Polinomio resultante ──────────────────────────────────────
        poly_str = self._poly_to_str(coeffs)
        steps.append({
            "step": len(steps) + 1,
            "phase": "result",
            "description": f"Polinomio interpolante: {poly_str}",
            "coefficients": coeffs[:],
        })

        # ── Paso 4: Verificación en los puntos originales ─────────────────────
        errors = []
        for xi, yi in zip(x_f, y_f):
            p_val = self._eval_poly(coeffs, xi)
            err = abs(p_val - yi)
            errors.append(err)
            steps.append({
                "step": len(steps) + 1,
                "phase": "verification",
                "description": f"p({xi}) = {p_val:.8g}  (esperado {yi}, error = {err:.2e})",
                "x": xi,
                "p_x": p_val,
                "expected": yi,
                "error": err,
            })

        # ── Paso 5 (opcional): Evaluación en x pedido por el usuario ─────────
        eval_result = None
        if "eval_x" in params and params["eval_x"] is not None:
            try:
                ex = float(params["eval_x"])
                eval_result = self._eval_poly(coeffs, ex)
                steps.append({
                    "step": len(steps) + 1,
                    "phase": "evaluation",
                    "description": f"Evaluación solicitada: p({ex}) = {eval_result:.10g}",
                    "eval_x": ex,
                    "eval_y": eval_result,
                })
            except (TypeError, ValueError):
                pass

        # ── Propiedades para la UI ────────────────────────────────────────────
        coeff_str = ", ".join(
            f"a{i}={c:.6g}" for i, c in enumerate(coeffs)
        )
        props = {
            "Polinomio Interpolante": poly_str,
            "Coeficientes": coeff_str,
            "Grado del polinomio": str(n - 1),
            "Error máximo en puntos originales": f"{max(errors):.2e}",
        }
        if eval_result is not None:
            props[f"p({params['eval_x']})"] = f"{eval_result:.10g}"

        return {
            "solution": coeffs,
            "properties": props,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
