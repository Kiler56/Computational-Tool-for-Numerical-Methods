/**
 * gaussian_simple.js
 * Implementacion individual de Eliminacion Gaussiana Simple.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { EPSILON, snapshot, validateSystem } = shared;

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
                description: `Pivote en posicion (${k},${k}) = ${pivot.toPrecision(6)}`,
                pivot,
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
                    description: `F${i + 1} <- F${i + 1} - (${factor.toPrecision(6)})*F${k + 1} -> Se elimina M[${i}][${k}]`,
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
                description: `x[${i}] = (${M[i][n].toPrecision(6)} - ${s.toPrecision(6)}) / ${M[i][i].toPrecision(6)} = ${x[i].toPrecision(6)}`,
                matrix_state: snapshot(M),
            });
        }

        return {
            solution: x,
            steps,
            iterations: steps.length,
            method: "gaussian_simple",
        };
    }

    global.gaussianSimple = gaussianSimple;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.gaussianSimple = gaussianSimple;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussianSimple;
    }
}(typeof window !== "undefined" ? window : globalThis));
