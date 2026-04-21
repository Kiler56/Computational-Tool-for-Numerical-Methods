/**
 * gaussian_total_pivoting.js
 * Implementacion individual de Eliminacion Gaussiana con Pivoteo Total.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { EPSILON, snapshot, validateSystem } = shared;

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
                description: `Pivote total en paso ${k}: valor = ${pivot.toPrecision(6)}`,
                pivot,
                max_val: maxVal,
                swap_rows: rowSwap,
                swap_cols: colSwap,
                matrix_state: snapshot(M),
            });

            for (let i = k + 1; i < n; i += 1) {
                const factor = M[i][k] / pivot;
                for (let j = k; j < n + 1; j += 1) {
                    M[i][j] -= factor * M[k][j];
                }

                steps.push({
                    step: steps.length + 1,
                    phase: "elimination",
                    description: `F${i + 1} <- F${i + 1} - (${factor.toPrecision(6)})*F${k + 1}`,
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
                description: `x_perm[${i}] = ${xPerm[i].toPrecision(6)}`,
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

        return {
            solution: x,
            steps,
            iterations: steps.length,
            method: "gaussian_total_pivoting",
        };
    }

    global.gaussianTotalPivoting = gaussianTotalPivoting;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.gaussianTotalPivoting = gaussianTotalPivoting;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussianTotalPivoting;
    }
}(typeof window !== "undefined" ? window : globalThis));
