/**
 * methods_js_port.js
 * Traduccion de metodos numericos de Python a JavaScript.
 * Se puede usar en navegador (window.NumericalMethodsJS) y en Node (module.exports).
 */
(function (global) {
    const EPSILON = 1e-12;

    function snapshot(value) {
        return JSON.parse(JSON.stringify(value));
    }

    function validateSystem(A, b) {
        if (!Array.isArray(A) || !Array.isArray(b) || A.length !== b.length || A.length === 0) {
            throw new Error("Sistema invalido: A y b deben tener el mismo tamano y n > 0.");
        }
        const n = b.length;
        for (let i = 0; i < n; i += 1) {
            if (!Array.isArray(A[i]) || A[i].length !== n) {
                throw new Error("La matriz A debe ser cuadrada.");
            }
        }
        return n;
    }

    function formatNumber(value) {
        if (!Number.isFinite(value)) return String(value);
        if (Math.abs(value) < 1e-15) return "0";
        return Number(value.toPrecision(6)).toString();
    }

    function gaussianSimple(A, b) {
        const n = validateSystem(A, b);
        const M = A.map((row, i) => [...row, b[i]]);
        const steps = [];

        for (let k = 0; k < n - 1; k += 1) {
            const pivot = M[k][k];
            if (Math.abs(pivot) < EPSILON) {
                throw new Error(`Pivote cero (o casi cero) en la fila ${k}. Use un metodo con pivoteo.`);
            }

            steps.push({
                step: steps.length + 1,
                phase: "elimination",
                description: `Pivote en posicion (${k},${k}) = ${formatNumber(pivot)}`,
                pivot,
                matrix_state: snapshot(M),
            });

            for (let i = k + 1; i < n; i += 1) {
                const factor = M[i][k] / pivot;
                for (let j = k; j <= n; j += 1) {
                    M[i][j] -= factor * M[k][j];
                }
                steps.push({
                    step: steps.length + 1,
                    phase: "elimination",
                    description: `F${i + 1} <- F${i + 1} - (${formatNumber(factor)})*F${k + 1}`,
                    factor,
                    matrix_state: snapshot(M),
                });
            }
        }

        const x = Array(n).fill(0);
        for (let i = n - 1; i >= 0; i -= 1) {
            if (Math.abs(M[i][i]) < EPSILON) {
                throw new Error(`Sistema singular: pivote cero en fila ${i} durante sustitucion regresiva.`);
            }
            let s = 0;
            for (let j = i + 1; j < n; j += 1) {
                s += M[i][j] * x[j];
            }
            x[i] = (M[i][n] - s) / M[i][i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x[${i}] = (${formatNumber(M[i][n])} - ${formatNumber(s)}) / ${formatNumber(M[i][i])} = ${formatNumber(x[i])}`,
                matrix_state: snapshot(M),
            });
        }

        return { solution: x, steps, iterations: steps.length, method: "gaussian_simple" };
    }

    function gaussianPartialPivoting(A, b) {
        const n = validateSystem(A, b);
        const M = A.map((row, i) => [...row, b[i]]);
        const steps = [];

        for (let k = 0; k < n - 1; k += 1) {
            let maxVal = Math.abs(M[k][k]);
            let maxRow = k;
            for (let i = k + 1; i < n; i += 1) {
                if (Math.abs(M[i][k]) > maxVal) {
                    maxVal = Math.abs(M[i][k]);
                    maxRow = i;
                }
            }

            let swapInfo = null;
            if (maxRow !== k) {
                [M[k], M[maxRow]] = [M[maxRow], M[k]];
                swapInfo = [k, maxRow];
            }

            const pivot = M[k][k];
            if (Math.abs(pivot) < EPSILON) {
                throw new Error(`Sistema singular: pivote cero en columna ${k} incluso despues de pivoteo parcial.`);
            }

            steps.push({
                step: steps.length + 1,
                phase: "elimination",
                description: `Pivote parcial en columna ${k}: valor = ${formatNumber(pivot)}`,
                pivot,
                swap_rows: swapInfo,
                matrix_state: snapshot(M),
            });

            for (let i = k + 1; i < n; i += 1) {
                const factor = M[i][k] / pivot;
                for (let j = k; j <= n; j += 1) {
                    M[i][j] -= factor * M[k][j];
                }
                steps.push({
                    step: steps.length + 1,
                    phase: "elimination",
                    description: `F${i + 1} <- F${i + 1} - (${formatNumber(factor)})*F${k + 1}`,
                    factor,
                    matrix_state: snapshot(M),
                });
            }
        }

        const x = Array(n).fill(0);
        for (let i = n - 1; i >= 0; i -= 1) {
            if (Math.abs(M[i][i]) < EPSILON) {
                throw new Error(`Sistema singular en sustitucion regresiva (fila ${i}).`);
            }
            let s = 0;
            for (let j = i + 1; j < n; j += 1) {
                s += M[i][j] * x[j];
            }
            x[i] = (M[i][n] - s) / M[i][i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x[${i}] = ${formatNumber(x[i])}`,
                matrix_state: snapshot(M),
            });
        }

        return { solution: x, steps, iterations: steps.length, method: "gaussian_partial_pivoting" };
    }

    function gaussianTotalPivoting(A, b) {
        const n = validateSystem(A, b);
        const M = A.map((row, i) => [...row, b[i]]);
        const colOrder = Array.from({ length: n }, (_, i) => i);
        const steps = [];

        for (let k = 0; k < n - 1; k += 1) {
            let maxVal = Math.abs(M[k][k]);
            let maxRow = k;
            let maxCol = k;

            for (let i = k; i < n; i += 1) {
                for (let j = k; j < n; j += 1) {
                    if (Math.abs(M[i][j]) > maxVal) {
                        maxVal = Math.abs(M[i][j]);
                        maxRow = i;
                        maxCol = j;
                    }
                }
            }

            let rowSwap = null;
            if (maxRow !== k) {
                [M[k], M[maxRow]] = [M[maxRow], M[k]];
                rowSwap = [k, maxRow];
            }

            let colSwap = null;
            if (maxCol !== k) {
                for (const row of M) {
                    [row[k], row[maxCol]] = [row[maxCol], row[k]];
                }
                [colOrder[k], colOrder[maxCol]] = [colOrder[maxCol], colOrder[k]];
                colSwap = [k, maxCol];
            }

            const pivot = M[k][k];
            if (Math.abs(pivot) < EPSILON) {
                throw new Error(`Sistema singular: pivote cero en paso ${k} incluso despues de pivoteo total.`);
            }

            steps.push({
                step: steps.length + 1,
                phase: "elimination",
                description: `Pivote total en paso ${k}: valor = ${formatNumber(pivot)}`,
                pivot,
                max_val: maxVal,
                swap_rows: rowSwap,
                swap_cols: colSwap,
                matrix_state: snapshot(M),
            });

            for (let i = k + 1; i < n; i += 1) {
                const factor = M[i][k] / pivot;
                for (let j = k; j <= n; j += 1) {
                    M[i][j] -= factor * M[k][j];
                }
                steps.push({
                    step: steps.length + 1,
                    phase: "elimination",
                    description: `F${i + 1} <- F${i + 1} - (${formatNumber(factor)})*F${k + 1}`,
                    factor,
                    matrix_state: snapshot(M),
                });
            }
        }

        const xPerm = Array(n).fill(0);
        for (let i = n - 1; i >= 0; i -= 1) {
            if (Math.abs(M[i][i]) < EPSILON) {
                throw new Error(`Sistema singular en sustitucion regresiva (fila ${i}).`);
            }
            let s = 0;
            for (let j = i + 1; j < n; j += 1) {
                s += M[i][j] * xPerm[j];
            }
            xPerm[i] = (M[i][n] - s) / M[i][i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x_perm[${i}] = ${formatNumber(xPerm[i])}`,
                matrix_state: snapshot(M),
            });
        }

        const x = Array(n).fill(0);
        for (let i = 0; i < n; i += 1) {
            x[colOrder[i]] = xPerm[i];
        }
        steps.push({
            step: steps.length + 1,
            phase: "reorder",
            description: `Reordenamiento de columnas: [${colOrder.join(", ")}] -> solucion final`,
            col_permutation: snapshot(colOrder),
            matrix_state: snapshot(M),
        });

        return { solution: x, steps, iterations: steps.length, method: "gaussian_total_pivoting" };
    }

    function validateTridiagonal(A, n) {
        for (let i = 0; i < n; i += 1) {
            for (let j = 0; j < n; j += 1) {
                if (Math.abs(i - j) > 1 && Math.abs(A[i][j]) > EPSILON) {
                    throw new Error(`La matriz NO es tridiagonal: A[${i}][${j}] = ${A[i][j]} != 0. Use otro metodo.`);
                }
            }
        }
    }

    function gaussTridiagonal(A, b) {
        const n = validateSystem(A, b);
        validateTridiagonal(A, n);

        const a = [0, ...Array.from({ length: n - 1 }, (_, i) => A[i + 1][i])];
        const d = Array.from({ length: n }, (_, i) => A[i][i]);
        const c = [...Array.from({ length: n - 1 }, (_, i) => A[i][i + 1]), 0];
        const r = [...b];
        const steps = [];

        steps.push({
            step: 1,
            phase: "extract",
            description: "Vectores extraidos de la matriz tridiagonal",
            sub_diagonal: snapshot(a),
            main_diagonal: snapshot(d),
            super_diagonal: snapshot(c),
            rhs: snapshot(r),
        });

        for (let i = 1; i < n; i += 1) {
            if (Math.abs(d[i - 1]) < EPSILON) {
                throw new Error(`Division por cero en forward sweep (d[${i - 1}] = ${d[i - 1]}).`);
            }
            const w = a[i] / d[i - 1];
            d[i] = d[i] - w * c[i - 1];
            r[i] = r[i] - w * r[i - 1];
            steps.push({
                step: steps.length + 1,
                phase: "forward_sweep",
                description: `i=${i}: w = a[${i}]/d[${i - 1}] = ${formatNumber(w)}, d[${i}] = ${formatNumber(d[i])}, r[${i}] = ${formatNumber(r[i])}`,
                w,
                main_diagonal: snapshot(d),
                rhs: snapshot(r),
            });
        }

        const x = Array(n).fill(0);
        if (Math.abs(d[n - 1]) < EPSILON) {
            throw new Error(`Division por cero en back substitution (d[${n - 1}] = ${d[n - 1]}).`);
        }
        x[n - 1] = r[n - 1] / d[n - 1];
        steps.push({
            step: steps.length + 1,
            phase: "back_substitution",
            description: `x[${n - 1}] = r[${n - 1}] / d[${n - 1}] = ${formatNumber(x[n - 1])}`,
            solution_partial: snapshot(x),
        });

        for (let i = n - 2; i >= 0; i -= 1) {
            if (Math.abs(d[i]) < EPSILON) {
                throw new Error(`Division por cero en back substitution (d[${i}] = ${d[i]}).`);
            }
            x[i] = (r[i] - c[i] * x[i + 1]) / d[i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x[${i}] = (r[${i}] - c[${i}]*x[${i + 1}]) / d[${i}] = ${formatNumber(x[i])}`,
                solution_partial: snapshot(x),
            });
        }

        return {
            solution: x,
            steps,
            iterations: steps.length,
            lower: snapshot(a),
            upper: snapshot(c),
            method: "gauss_tridiagonal",
        };
    }

    const methodSolvers = {
        gaussian_simple: gaussianSimple,
        gaussian_partial_pivoting: gaussianPartialPivoting,
        gaussian_total_pivoting: gaussianTotalPivoting,
        gauss_tridiagonal: gaussTridiagonal,
    };

    function solve(methodName, matrix, b) {
        const solver = methodSolvers[methodName];
        if (!solver) {
            throw new Error(`Metodo no soportado en JavaScript: ${methodName}`);
        }
        return solver(matrix, b);
    }

    const api = {
        solve,
        gaussianSimple,
        gaussianPartialPivoting,
        gaussianTotalPivoting,
        gaussTridiagonal,
    };

    global.NumericalMethodsJS = api;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = api;
    }
}(typeof window !== "undefined" ? window : globalThis));
