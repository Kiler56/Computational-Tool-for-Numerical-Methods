"""
Graficadora Universal para Métodos Numéricos.

plot_type registrados:
    root_finding      — bisection, false_position, trisection
    root_convergence  — newton, secant, fixed_point, multiple_roots,
                        steffensen, aitken, muller
    incremental       — incremental_search
    gaussian_elim     — gaussian_simple, partial_pivoting, total_pivoting
    lu_factorization  — doolittle, crout, cholesky
    tridiagonal       — gauss_tridiagonal
    iterative_matrix  — jacobi, gauss_seidel, sor
    matrix_analysis   — matrix_analysis
    interpolation     — lagrange, vandermonde, newton_interpolation
    integration       — simpson38
"""

from __future__ import annotations

from typing import Callable, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


# ═══════════════════════════════════════════════════════════════
# EXTRACTOR
# ═══════════════════════════════════════════════════════════════

class StepExtractor:
    """Extrae campos de un paso usando múltiples claves candidatas."""

    _ERROR_KEYS  = ("error", "err", "tolerance", "tol", "residual")
    _VECTOR_KEYS = ("vector", "solution_partial", "x_vector", "x_vec")
    _ROOT_KEYS   = ("xm", "x", "x_new", "root", "xr", "c", "p", "x1")
    _MATRIX_KEYS = ("matrix_state", "A", "matrix")

    @classmethod
    def error(cls, step: dict) -> Optional[float]:
        for key in cls._ERROR_KEYS:
            val = step.get(key) or step.get("data", {}).get(key)
            if val is not None:
                try:
                    v = float(val)
                    return v if v > 0 else None
                except (TypeError, ValueError):
                    pass
        return None

    @classmethod
    def vector(cls, step: dict) -> Optional[np.ndarray]:
        for key in cls._VECTOR_KEYS:
            val = step.get(key) or step.get("data", {}).get(key)
            if val is not None:
                try:
                    return np.asarray(val, dtype=float)
                except (TypeError, ValueError):
                    pass
        return None

    @classmethod
    def root_x(cls, step: dict) -> Optional[float]:
        for key in cls._ROOT_KEYS:
            if key in step:
                try:
                    return float(step[key])
                except (TypeError, ValueError):
                    pass
        return None

    @classmethod
    def matrix(cls, step: dict) -> Optional[np.ndarray]:
        for key in cls._MATRIX_KEYS:
            if key in step:
                try:
                    return np.asarray(step[key], dtype=float)
                except (TypeError, ValueError):
                    pass
        return None


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def _safe_eval_array(f: Callable, xs: np.ndarray) -> np.ndarray:
    """Evalúa f punto a punto; sustituye excepciones por NaN."""
    ys = np.empty_like(xs, dtype=float)
    for i, x in enumerate(xs):
        try:
            ys[i] = float(f(x))
        except Exception:
            ys[i] = np.nan
    return ys


def _annotate_matrix(ax, mat: np.ndarray, fmt: str = ".2f") -> None:
    """Escribe el valor numérico en cada celda del heatmap. Omite si >64 celdas."""
    rows, cols = mat.shape
    if rows * cols > 64:
        return
    vmax = np.abs(mat).max() or 1
    for i in range(rows):
        for j in range(cols):
            color = "white" if abs(mat[i, j]) > vmax * 0.6 else "black"
            ax.text(j, i, format(mat[i, j], fmt),
                    ha="center", va="center", fontsize=8, color=color)


def _print_swaps(steps: list) -> None:
    """Imprime en stdout los intercambios de filas/columnas registrados en steps."""
    row_swaps = [(s.get("step"), s["swap_rows"]) for s in steps if s.get("swap_rows")]
    col_swaps = [(s.get("step"), s["swap_cols"]) for s in steps if s.get("swap_cols")]
    if not row_swaps and not col_swaps:
        return
    print("\n========== INTERCAMBIOS ==========")
    for n, r in row_swaps:
        print(f"  Paso {n} → swap filas: {r}")
    for n, c in col_swaps:
        print(f"  Paso {n} → swap columnas: {c}")
    print("==================================\n")


def _build_x_range(x_iter: list, root, margin_factor: float = 0.4):
    """Calcula [x_min, x_max] con margen proporcional al rango de los datos."""
    all_x = x_iter + ([root] if root is not None else [])
    if not all_x:
        return -5.0, 5.0
    span = max(all_x) - min(all_x)
    margin = max(span * margin_factor, 1.0)
    return min(all_x) - margin, max(all_x) + margin


# ═══════════════════════════════════════════════════════════════
# RENDERERS — RAÍCES
# ═══════════════════════════════════════════════════════════════

def _render_root_finding(result: dict, f: Optional[Callable] = None) -> Figure:
    """
    Grafica f(x) con la trayectoria de iteraciones y la raíz hallada.

    Claves relevantes en steps:
        "a", "b"       — intervalo activo (bisection, false_position, trisection)
        "x2"           — segundo punto (secant, muller)
    Claves relevantes en result:
        "root"         — raíz hallada
    """
    steps  = result.get("steps", [])
    root   = result.get("root")
    method = result.get("method", "")

    x_iter = [StepExtractor.root_x(s) for s in steps]
    x_iter = [x for x in x_iter if x is not None]
    x_min, x_max = _build_x_range(x_iter, root)

    fig, ax = plt.subplots(figsize=(9, 5))

    if f is not None:
        xs = np.linspace(x_min, x_max, 1000)
        ys = _safe_eval_array(f, xs)
        ax.plot(xs, ys, linewidth=1.8, label="f(x)", color="#3266ad", zorder=2)
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)

        for s in steps:
            if "a" in s and "b" in s:
                ax.axvspan(s["a"], s["b"], alpha=0.03, color="#3266ad")

        if x_iter:
            y_iter = _safe_eval_array(f, np.array(x_iter))
            ax.scatter(x_iter, y_iter, s=50, zorder=4,
                       label="Iteraciones", color="#d85a30")

        x2_list = [s["x2"] for s in steps if "x2" in s]
        if x2_list:
            y2 = _safe_eval_array(f, np.array(x2_list))
            ax.scatter(x2_list, y2, s=30, zorder=4, marker="^",
                       label="x₂", color="#1d9e75", alpha=0.7)

        if root is not None:
            try:
                yr = float(f(root))
            except Exception:
                yr = 0.0
            ax.scatter([root], [yr], s=140, marker="*",
                       color="#1d9e75", zorder=5, label=f"Raíz ≈ {root:.6f}")
    else:
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
        ax.scatter(x_iter, [0] * len(x_iter), s=50, zorder=4,
                   label="Iteraciones", color="#d85a30")
        if root is not None:
            ax.scatter([root], [0], s=140, marker="*",
                       color="#1d9e75", zorder=5, label=f"Raíz ≈ {root:.6f}")

    ax.set_title(f"Búsqueda de raíz — {method}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def _render_root_convergence(result: dict, f: Optional[Callable] = None) -> Figure:
    """
    Convergencia de métodos iterativos de raíces.

    Subplots:
        [0] aproximación x por iteración
        [1] |error| en escala logarítmica (si existe)
        [2] multiplicidad m (si existe, para multiple_roots)

    Caso especial muller: grafica x0, x1, x2 por separado si están en steps.
    """
    steps  = result.get("steps", [])
    method = result.get("method", "")

    iters, approx, errors = [], [], []
    for s in steps:
        x = StepExtractor.root_x(s)
        if x is not None:
            iters.append(s.get("step", len(iters)))
            approx.append(x)
            errors.append(StepExtractor.error(s))

    if not iters:
        raise ValueError("No hay aproximaciones en los pasos.")

    has_errors = any(e is not None for e in errors)

    muller_keys = all("x0" in s and "x1" in s and "x2" in s for s in steps[:3])
    if method == "muller" and muller_keys and len(steps) >= 2:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        for key, label, color in [("x0", "x₀", "#3266ad"),
                                   ("x1", "x₁", "#d85a30"),
                                   ("x2", "x₂", "#1d9e75")]:
            vals = [s[key] for s in steps if key in s]
            its  = [s.get("step", i) for i, s in enumerate(steps) if key in s]
            axes[0].plot(its, vals, marker="o", markersize=4,
                         label=label, color=color, linewidth=1.3)
        axes[0].set_title(f"Evolución de puntos — {method}")
        axes[0].set_xlabel("Iteración")
        axes[0].set_ylabel("x")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        if has_errors:
            valid = [(i, e) for i, e in zip(iters, errors) if e is not None]
            ei, ev = zip(*valid)
            axes[1].semilogy(ei, ev, marker="s", color="#d85a30",
                             linewidth=1.5, markersize=4)
            axes[1].set_title("|Error|")
            axes[1].set_xlabel("Iteración")
            axes[1].grid(True, alpha=0.3, which="both")
        fig.suptitle(f"Convergencia — {method}")
        fig.tight_layout()
        return fig

    mult_vals = [s.get("m") for s in steps if "m" in s]
    n_rows = 1 + int(has_errors) + int(bool(mult_vals))
    fig, axes = plt.subplots(n_rows, 1, figsize=(8, 3.5 * n_rows), sharex=True)
    if n_rows == 1:
        axes = [axes]

    axes[0].plot(iters, approx, marker="o", markersize=5,
                 color="#3266ad", linewidth=1.5)
    axes[0].set_ylabel("Aproximación x")
    axes[0].set_title(f"Convergencia — {method}")
    axes[0].grid(True, alpha=0.3)

    row = 1
    if has_errors:
        valid = [(i, e) for i, e in zip(iters, errors) if e is not None]
        ei, ev = zip(*valid)
        axes[row].semilogy(ei, ev, marker="s", markersize=4,
                           color="#d85a30", linewidth=1.5)
        axes[row].set_ylabel("|Error|")
        axes[row].grid(True, alpha=0.3, which="both")
        row += 1

    if mult_vals:
        its_m = [s.get("step", i) for i, s in enumerate(steps) if "m" in s]
        axes[row].plot(its_m, mult_vals, marker="D", markersize=4,
                       color="#7f77dd", linewidth=1.3)
        axes[row].set_ylabel("Multiplicidad m")
        axes[row].grid(True, alpha=0.3)

    axes[-1].set_xlabel("Iteración")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — BÚSQUEDA INCREMENTAL
# ═══════════════════════════════════════════════════════════════

def _render_incremental(result: dict, f: Optional[Callable] = None) -> Figure:
    """
    Grafica f(x) con los subintervalos evaluados y los cambios de signo.

    Claves relevantes en steps:
        "a", "b"        — extremos del subintervalo
        "sign_change"   — bool, True si hay cambio de signo en [a, b]
    Claves relevantes en result:
        "intervals"  o  "roots"  — lista de intervalos que contienen raíz
    """
    steps  = result.get("steps", [])
    method = result.get("method", "incremental_search")
    roots  = result.get("intervals", result.get("roots", []))

    if not steps:
        raise ValueError("No hay pasos en el resultado.")

    fig, ax = plt.subplots(figsize=(10, 5))

    a_vals = [s.get("a", s.get("x_prev")) for s in steps if "a" in s or "x_prev" in s]
    b_vals = [s.get("b", s.get("x_curr")) for s in steps if "b" in s or "x_curr" in s]

    if f is not None and a_vals and b_vals:
        x_min = min(a_vals) - 0.5
        x_max = max(b_vals) + 0.5
        xs = np.linspace(x_min, x_max, 1000)
        ys = _safe_eval_array(f, xs)
        ax.plot(xs, ys, linewidth=1.8, color="#3266ad", label="f(x)", zorder=2)
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)

    for s in steps:
        a = s.get("a", s.get("x_prev"))
        b = s.get("b", s.get("x_curr"))
        if s.get("sign_change") and a is not None and b is not None:
            ax.axvspan(a, b, alpha=0.15, color="#1d9e75", label="Cambio de signo")

    for s in steps:
        a = s.get("a", s.get("x_prev"))
        b = s.get("b", s.get("x_curr"))
        if a is not None and b is not None:
            ax.plot([a, b], [0, 0], color="#d85a30", linewidth=2, alpha=0.3)

    if roots:
        for r in roots:
            ax.axvline(r, color="#1d9e75", linewidth=1.2, linestyle=":",
                       label=f"Raíz en [{r[0]:.4f},{r[1]:.4f}]"
                       if isinstance(r, (list, tuple)) else f"x≈{r:.4f}")

    ax.set_title(f"Búsqueda incremental — {method}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    handles, labels = ax.get_legend_handles_labels()
    seen = {}
    for h, l in zip(handles, labels):
        seen[l] = h
    ax.legend(seen.values(), seen.keys(), fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — SISTEMAS LINEALES ITERATIVOS
# ═══════════════════════════════════════════════════════════════

def _render_iterative_matrix(result: dict, **_) -> Figure:
    """
    Convergencia de métodos iterativos para sistemas lineales.

    Subplots:
        izquierda — |error| por iteración en escala logarítmica
        derecha   — evolución de cada componente del vector solución

    Claves relevantes en steps:
        "vector"  — vector solución en la iteración actual
        "error"   — norma del error
    """
    steps = result.get("steps", [])
    iters, errors, vectors = [], [], []

    for s in steps:
        iters.append(s.get("step", len(iters)))
        errors.append(StepExtractor.error(s))
        vectors.append(StepExtractor.vector(s))

    has_errors  = any(e is not None for e in errors)
    has_vectors = any(v is not None for v in vectors)

    n_plots = int(has_errors) + int(has_vectors)
    if n_plots == 0:
        raise ValueError("Los pasos no contienen errores ni vectores.")

    fig, axes = plt.subplots(1, n_plots, figsize=(6 * n_plots, 5))
    if n_plots == 1:
        axes = [axes]

    idx = 0
    if has_errors:
        ax = axes[idx]
        valid = [(i, e) for i, e in zip(iters, errors) if e is not None]
        ei, ev = zip(*valid)
        ax.semilogy(ei, ev, marker="o", markersize=4,
                    color="#d85a30", linewidth=1.5)
        ax.set_title("Convergencia del error")
        ax.set_xlabel("Iteración")
        ax.set_ylabel("|Error|")
        ax.grid(True, alpha=0.3, which="both")
        idx += 1

    if has_vectors:
        ax = axes[idx]
        valid_v = [(i, v) for i, v in zip(iters, vectors) if v is not None]
        vi, vv = zip(*valid_v)
        vmat = np.vstack(vv)
        colors = plt.cm.tab10(np.linspace(0, 1, vmat.shape[1]))
        for j in range(vmat.shape[1]):
            ax.plot(vi, vmat[:, j], marker="o", markersize=3,
                    linewidth=1.3, label=f"x{j+1}", color=colors[j])
        ax.set_title("Evolución de la solución")
        ax.set_xlabel("Iteración")
        ax.set_ylabel("Valor")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    fig.suptitle(f"{result.get('method', '')} — métodos iterativos", y=1.01)
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — FACTORIZACIONES LU
# ═══════════════════════════════════════════════════════════════

def _render_lu_factorization(result: dict, **_) -> Figure:
    """
    Heatmaps de L y U con valores anotados.
    Para Cholesky añade un panel adicional con la verificación L·Lᵀ.

    Claves relevantes en result:
        "L", "U" — matrices de la factorización
    """
    matrices = {}
    for key in ("L", "U"):
        if key in result:
            try:
                matrices[key] = np.asarray(result[key], dtype=float)
            except (TypeError, ValueError):
                pass

    if not matrices:
        raise ValueError("El resultado no contiene matrices L ni U.")

    method = result.get("method", "")
    is_cholesky = "cholesky" in method.lower()

    n_extra = 1 if is_cholesky and "L" in matrices else 0
    n = len(matrices) + n_extra
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 5))
    if n == 1:
        axes = [axes]

    cmaps = {"L": "Blues", "U": "Oranges"}
    for ax, (key, mat) in zip(axes, matrices.items()):
        im = ax.imshow(mat, cmap=cmaps.get(key, "viridis"), aspect="auto")
        fig.colorbar(im, ax=ax, shrink=0.8)
        _annotate_matrix(ax, mat)
        ax.set_title(f"Matriz {key} — {method}")
        ax.set_xlabel("Columna")
        ax.set_ylabel("Fila")

    if is_cholesky and "L" in matrices:
        L   = matrices["L"]
        LLt = L @ L.T
        ax  = axes[-1]
        im  = ax.imshow(LLt, cmap="Greens", aspect="auto")
        fig.colorbar(im, ax=ax, shrink=0.8)
        _annotate_matrix(ax, LLt)
        ax.set_title("Verificación L·Lᵀ")

    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — ANÁLISIS DE MATRICES
# ═══════════════════════════════════════════════════════════════

def _render_matrix_analysis(result: dict, **_) -> Figure:
    """
    Heatmap de valores + patrón de dispersión (spy).

    Claves relevantes en result:
        "A" | "matrix" | "L" | "U" — matriz a analizar
        "properties"               — dict con propiedades a mostrar como pie de figura
    """
    mat = None
    for s in result.get("steps", []):
        m = StepExtractor.matrix(s)
        if m is not None:
            mat = m
            break
    for key in ("L", "U", "A", "matrix"):
        if key in result and mat is None:
            try:
                mat = np.asarray(result[key], dtype=float)
            except (TypeError, ValueError):
                pass
    if mat is None:
        raise ValueError("No se encontró ninguna matriz en el resultado.")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    im = ax1.imshow(mat, cmap="coolwarm", aspect="auto")
    fig.colorbar(im, ax=ax1, shrink=0.8)
    _annotate_matrix(ax1, mat)
    ax1.set_title("Valores de la matriz")

    ax2.spy(mat, markersize=8, color="#3266ad")
    ax2.set_title("Patrón de dispersión")

    if "properties" in result:
        info = "\n".join(f"{k}: {v}" for k, v in result["properties"].items())
        fig.text(0.5, -0.04, info, ha="center", fontsize=9, color="gray", wrap=True)

    fig.suptitle(f"Análisis de matriz — {result.get('method', '')}")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — ELIMINACIÓN GAUSSIANA
# ═══════════════════════════════════════════════════════════════

def _render_gaussian_elim(result: dict, **_) -> Figure:
    """
    Visualiza el estado final de la matriz escalonada y la evolución de pivotes.

    Paneles:
        [0] matriz escalonada final con valores anotados
        [1] magnitud |A| de la matriz final
        [2] evolución de |pivote| por paso (si existen)

    Claves relevantes en steps:
        "matrix_state" — estado de la matriz aumentada en cada paso
        "pivot"        — valor del pivote usado
        "swap_rows"    — intercambio de filas (pivoteo parcial/total)
        "swap_cols"    — intercambio de columnas (pivoteo total)
    """
    steps = result.get("steps", [])
    matrices, pivots, iters = [], [], []

    for s in steps:
        m = StepExtractor.matrix(s)
        if m is not None:
            matrices.append(m)
            iters.append(s.get("step", len(iters)))
            pivots.append(s.get("pivot"))

    if not matrices:
        raise ValueError("No hay estados de matriz en los pasos.")

    final      = matrices[-1]
    has_pivots = any(p is not None for p in pivots)
    n_plots    = 3 if has_pivots else 2

    fig, axes = plt.subplots(1, n_plots, figsize=(5 * n_plots, 5))

    im = axes[0].imshow(final, cmap="coolwarm", aspect="auto")
    fig.colorbar(im, ax=axes[0], shrink=0.8)
    _annotate_matrix(axes[0], final)
    axes[0].set_title("Matriz escalonada final")

    axes[1].imshow(np.abs(final), cmap="Greens", aspect="auto")
    axes[1].set_title("Magnitud |A|")

    if has_pivots:
        valid = [(i, abs(p)) for i, p in zip(iters, pivots) if p is not None]
        pi, pv = zip(*valid)
        axes[2].plot(pi, pv, marker="o", color="#d85a30", linewidth=1.5)
        axes[2].set_title("Evolución de pivotes")
        axes[2].set_xlabel("Paso")
        axes[2].set_ylabel("|Pivote|")
        axes[2].grid(True, alpha=0.3)

    _print_swaps(steps)
    fig.suptitle(f"{result.get('method', '')} — eliminación gaussiana")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — TRIDIAGONAL
# ═══════════════════════════════════════════════════════════════

def _render_tridiagonal(result: dict, **_) -> Figure:
    """
    Grafica la estructura de diagonales y la evolución de la solución parcial.

    Claves relevantes en result:
        "lower" — subdiagonal
        "upper" — superdiagonal
    Claves relevantes en steps:
        "solution_partial" — vector solución parcial en cada paso
    """
    lower = result.get("lower")
    upper = result.get("upper")
    steps = result.get("steps", [])

    has_diag    = lower is not None and upper is not None
    has_partial = any("solution_partial" in s for s in steps)

    n_plots = int(has_diag) + int(has_partial)
    if n_plots == 0:
        raise ValueError("No hay datos de estructura ni solución parcial.")

    fig, axes = plt.subplots(1, n_plots, figsize=(6 * n_plots, 5))
    if n_plots == 1:
        axes = [axes]

    idx = 0
    if has_diag:
        ax = axes[idx]
        ax.plot(lower, marker="o", label="Subdiagonal",   color="#3266ad")
        ax.plot(upper, marker="s", label="Superdiagonal", color="#d85a30")
        ax.set_title("Estructura tridiagonal")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        ax.legend()
        ax.grid(True, alpha=0.3)
        idx += 1

    if has_partial:
        ax       = axes[idx]
        partials = [s["solution_partial"] for s in steps if "solution_partial" in s]
        iters_p  = [s.get("step", i) for i, s in enumerate(steps) if "solution_partial" in s]
        pmat     = np.array(partials)
        colors   = plt.cm.tab10(np.linspace(0, 1, pmat.shape[1]))
        for j in range(pmat.shape[1]):
            ax.plot(iters_p, pmat[:, j], marker="o", markersize=3,
                    linewidth=1.3, label=f"x{j}", color=colors[j])
        ax.set_title("Evolución solución parcial")
        ax.set_xlabel("Paso")
        ax.set_ylabel("Valor")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    fig.suptitle(f"{result.get('method', '')} — tridiagonal")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — INTERPOLACIÓN
# ═══════════════════════════════════════════════════════════════

def _render_interpolation(result: dict, f: Optional[Callable] = None) -> Figure:
    """
    Grafica el polinomio interpolante sobre los nodos dados.

    Claves relevantes en result:
        "x_points"   — nodos x
        "y_points"   — valores y en los nodos
        "polynomial" — callable P(x) (prioritario sobre coeffs)
        "coeffs"     — coeficientes para numpy.polyval (fallback)
        "eval_point" — punto de evaluación solicitado
        "eval_value" — P(eval_point)
    Claves relevantes en steps:
        "divided_diff" — tabla de diferencias divididas (Newton); genera heatmap
    """
    method  = result.get("method", "interpolation")
    x_pts   = np.asarray(result.get("x_points", []), dtype=float)
    y_pts   = np.asarray(result.get("y_points", []), dtype=float)
    poly_fn = result.get("polynomial")
    coeffs  = result.get("coeffs")
    x_eval  = result.get("eval_point")
    y_eval  = result.get("eval_value")

    if len(x_pts) == 0:
        raise ValueError("'x_points' requerido para interpolation.")

    x_min = x_pts.min() - abs(x_pts.min() - x_pts.max()) * 0.15 - 0.5
    x_max = x_pts.max() + abs(x_pts.min() - x_pts.max()) * 0.15 + 0.5
    xs    = np.linspace(x_min, x_max, 600)

    ys_poly = None
    if poly_fn is not None and callable(poly_fn):
        ys_poly = _safe_eval_array(poly_fn, xs)
    elif coeffs is not None:
        ys_poly = np.polyval(np.asarray(coeffs, dtype=float), xs)

    has_dd  = any("divided_diff" in s for s in result.get("steps", []))
    n_plots = 1 + int(has_dd)
    fig, axes = plt.subplots(1, n_plots, figsize=(7 * n_plots, 5))
    if n_plots == 1:
        axes = [axes]

    ax = axes[0]
    if f is not None:
        ax.plot(xs, _safe_eval_array(f, xs), linewidth=1.2, linestyle="--",
                color="#888", label="f(x) original", alpha=0.7)
    if ys_poly is not None:
        ax.plot(xs, ys_poly, linewidth=1.8, color="#3266ad", label="P(x) interpolante")
    ax.scatter(x_pts, y_pts, s=70, zorder=5, color="#d85a30",
               label="Nodos", edgecolors="white", linewidths=0.5)
    if x_eval is not None and y_eval is not None:
        ax.scatter([x_eval], [y_eval], s=120, marker="*", zorder=6,
                   color="#1d9e75", label=f"P({x_eval:.3f}) = {y_eval:.5f}")
    ax.set_title(f"Interpolación — {method}")
    ax.set_xlabel("x")
    ax.set_ylabel("P(x)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    if has_dd:
        dd_steps = [s["divided_diff"] for s in result.get("steps", []) if "divided_diff" in s]
        dd_mat   = np.array(dd_steps, dtype=float)
        ax2      = axes[1]
        im       = ax2.imshow(dd_mat, cmap="coolwarm", aspect="auto")
        fig.colorbar(im, ax=ax2, shrink=0.8)
        _annotate_matrix(ax2, dd_mat, fmt=".3f")
        ax2.set_title("Diferencias divididas")
        ax2.set_xlabel("Orden")
        ax2.set_ylabel("Nodo")

    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# RENDERERS — INTEGRACIÓN
# ═══════════════════════════════════════════════════════════════

def _render_integration(result: dict, f: Optional[Callable] = None) -> Figure:
    """
    Grafica f(x) con el área sombreada y los paneles de integración.

    Claves relevantes en result:
        "a"        — límite inferior
        "b"        — límite superior
        "integral" — valor aproximado
        "exact"    — valor exacto (opcional)
        "panels"   — list[{"a","b","area"}] subpaneles (opcional)

    Si "exact" y "panels" están presentes genera un subplot adicional
    con el error absoluto por panel.
    """
    method   = result.get("method", "integration")
    a        = result.get("a")
    b        = result.get("b")
    integral = result.get("integral")
    exact    = result.get("exact")
    panels   = result.get("panels", [])

    if a is None or b is None:
        raise ValueError("'a' y 'b' son requeridos para integration.")

    has_panels = bool(panels)
    has_error  = exact is not None and has_panels
    n_plots    = 1 + int(has_error)

    fig, axes = plt.subplots(1, n_plots, figsize=(7 * n_plots, 5))
    if n_plots == 1:
        axes = [axes]

    ax      = axes[0]
    xs_full = np.linspace(a, b, 600)

    if f is not None:
        ys_full = _safe_eval_array(f, xs_full)
        ax.plot(xs_full, ys_full, linewidth=1.8, color="#3266ad", label="f(x)")
        ax.fill_between(xs_full, ys_full, alpha=0.12, color="#3266ad")
        panel_colors = plt.cm.tab10(np.linspace(0, 0.5, max(len(panels), 1)))
        for pi, panel in enumerate(panels):
            pa, pb = panel.get("a", a), panel.get("b", b)
            xs_p   = np.linspace(pa, pb, 80)
            ys_p   = _safe_eval_array(f, xs_p)
            ax.fill_between(xs_p, ys_p, alpha=0.25,
                            color=panel_colors[pi % len(panel_colors)])
            ax.axvline(pa, color="gray", linewidth=0.5, alpha=0.4)
        ax.axvline(b, color="gray", linewidth=0.5, alpha=0.4)
        ax.axhline(0, color="gray", linewidth=0.6, linestyle="--", alpha=0.4)

    label = f"∫f dx ≈ {integral:.6f}" if integral is not None else "Integración"
    if exact is not None:
        err_rel = abs(integral - exact) / abs(exact) * 100 if exact != 0 else 0
        label  += f"\nExacto: {exact:.6f}  |  Error: {err_rel:.4f}%"
    ax.set_title(f"{method} — {label}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    if has_error:
        ax2          = axes[1]
        panel_errors = [abs(p.get("area", 0) - exact / len(panels)) for p in panels]
        ax2.bar(range(len(panels)), panel_errors, color="#d85a30",
                alpha=0.7, edgecolor="white")
        ax2.set_title("Error absoluto por panel")
        ax2.set_xlabel("Panel")
        ax2.set_ylabel("|Error|")
        ax2.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# REGISTRO DE RENDERERS
# ═══════════════════════════════════════════════════════════════

_RENDERERS: dict[str, Callable] = {
    "root_finding":     _render_root_finding,
    "root_convergence": _render_root_convergence,
    "incremental":      _render_incremental,
    "gaussian_elim":    _render_gaussian_elim,
    "lu_factorization": _render_lu_factorization,
    "tridiagonal":      _render_tridiagonal,
    "iterative_matrix": _render_iterative_matrix,
    "matrix_analysis":  _render_matrix_analysis,
    "interpolation":    _render_interpolation,
    "integration":      _render_integration,
}


# ═══════════════════════════════════════════════════════════════
# TABLA DE INFERENCIA method → plot_type
# ═══════════════════════════════════════════════════════════════

METHOD_TO_PLOT_TYPE: dict[str, str] = {
    "bisection":              "root_finding",
    "false_position":         "root_finding",
    "trisection":             "root_finding",
    "incremental_search":     "incremental",
    "newton":                 "root_convergence",
    "secante":                "root_convergence",
    "punto_fijo":             "root_convergence",
    "raices_multiples":       "root_convergence",
    "steffensen":             "root_convergence",
    "aitken":                 "root_convergence",
    "muller":                 "root_convergence",
    "gaussian_simple":        "gaussian_elim",
    "gaussian_partial_pivoting": "gaussian_elim",
    "gaussian_total_pivoting":   "gaussian_elim",
    "doolittle":              "lu_factorization",
    "crout":                  "lu_factorization",
    "cholesky":               "lu_factorization",
    "gauss_tridiagonal":      "tridiagonal",
    "jacobi":                 "iterative_matrix",
    "gauss_seidel":           "iterative_matrix",
    "sor":                    "iterative_matrix",
    "matrix_analysis":        "matrix_analysis",
    "lagrange":               "interpolation",
    "vandermonde":            "interpolation",
    "newton_interpolation":   "interpolation",
    "simpson38":              "integration",
}


def suggest_plot_type(method_name: str) -> str:
    """Devuelve el plot_type correspondiente a un nombre de método."""
    key = method_name.lower().replace(" ", "_")
    pt  = METHOD_TO_PLOT_TYPE.get(key)
    if pt is None:
        available = ", ".join(sorted(METHOD_TO_PLOT_TYPE.keys()))
        raise KeyError(f"Método '{method_name}' no reconocido. Disponibles: {available}")
    return pt


# ═══════════════════════════════════════════════════════════════
# CLASE PÚBLICA
# ═══════════════════════════════════════════════════════════════

class UniversalPlotter:
    """
    Graficadora desacoplada para métodos numéricos.

    Parameters
    ----------
    result : dict
        Diccionario devuelto por el método numérico.
        Debe incluir "plot_type"; si no está se intenta inferir de "method".
    f : callable, opcional
        Función f(x). Requerida para root_finding, incremental,
        interpolation e integration.
    show : bool
        Si True llama plt.show() tras generar la figura.
    """

    def __init__(
        self,
        result: dict,
        f: Optional[Callable] = None,
        show: bool = False,
    ) -> None:
        self.result    = result
        self.f         = f
        self.show      = show
        self.method    = result.get("method", "unknown")
        if "plot_type" not in result:
            try:
                result["plot_type"] = suggest_plot_type(self.method)
            except KeyError:
                pass
        self.plot_type = result.get("plot_type", "")

    def plot(self) -> Figure:
        """Selecciona el renderer por plot_type y retorna la Figure generada."""
        renderer = _RENDERERS.get(self.plot_type)
        if renderer is None:
            available = ", ".join(_RENDERERS.keys())
            raise ValueError(
                f"plot_type '{self.plot_type}' no registrado. "
                f"Valores válidos: {available}"
            )
        fig = renderer(self.result, f=self.f)
        if self.show:
            plt.show()
        return fig

    def summary(self) -> None:
        """Imprime un resumen textual del resultado en stdout."""
        print("\n========== RESUMEN ==========")
        print(f"  Método     : {self.method}")
        print(f"  Plot type  : {self.plot_type}")
        print(f"  Iteraciones: {self.result.get('iterations', '—')}")
        if "solution" in self.result:
            print(f"  Solución   : {np.array2string(np.asarray(self.result['solution']), precision=6)}")
        if "root"       in self.result: print(f"  Raíz       : {self.result['root']}")
        if "integral"   in self.result: print(f"  Integral   : {self.result['integral']}")
        if "eval_value" in self.result: print(f"  P(x_eval)  : {self.result['eval_value']}")
        if "properties" in self.result:
            print("  Propiedades:")
            for k, v in self.result["properties"].items():
                print(f"    {k}: {v}")
        print("=============================\n")

    @staticmethod
    def register(plot_type: str, renderer: Callable) -> None:
        """Registra un renderer externo para un plot_type nuevo."""
        if not callable(renderer):
            raise TypeError("El renderer debe ser callable.")
        _RENDERERS[plot_type] = renderer

    @staticmethod
    def available_plot_types() -> list[str]:
        """Retorna la lista de plot_types registrados."""
        return list(_RENDERERS.keys())
