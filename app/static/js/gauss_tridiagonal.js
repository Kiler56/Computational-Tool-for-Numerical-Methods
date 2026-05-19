/**
 * gauss_tridiagonal.js
 * Implementacion individual del algoritmo de Thomas.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const {
        EPSILON,
        snapshot,
        validateSystem,
        validateTridiagonal,
        formatNumber,
    } = shared;

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
            d[i] -= w * c[i - 1];
            r[i] -= w * r[i - 1];

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

    global.gaussTridiagonal = gaussTridiagonal;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.gaussTridiagonal = gaussTridiagonal;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussTridiagonal;
    }
}(typeof window !== "undefined" ? window : globalThis));
