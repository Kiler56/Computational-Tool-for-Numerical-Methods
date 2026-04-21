/**
 * gaussian_partial_pivoting.js
 * Implementacion individual de Eliminacion Gaussiana con Pivoteo Parcial.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { EPSILON, snapshot, validateSystem } = shared;

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
                description: `Pivote parcial en columna ${k}: valor = ${pivot.toPrecision(6)}`,
                pivot,
                swap_rows: swapInfo,
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
                description: `x[${i}] = ${x[i].toPrecision(6)}`,
                matrix_state: snapshot(M),
            });
        }

        return {
            solution: x,
            steps,
            iterations: steps.length,
            method: "gaussian_partial_pivoting",
        };
    }

    global.gaussianPartialPivoting = gaussianPartialPivoting;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.gaussianPartialPivoting = gaussianPartialPivoting;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussianPartialPivoting;
    }
}(typeof window !== "undefined" ? window : globalThis));
