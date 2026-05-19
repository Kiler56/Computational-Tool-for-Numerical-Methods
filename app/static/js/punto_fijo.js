/**
 * punto_fijo.js
 * Implementacion individual del metodo de Punto Fijo.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { makeFunction } = shared;

    function puntoFijo(expr, params = {}) {
        const g = makeFunction(expr);
        let x = Number(params.x0 ?? 1.5);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let xNew = x;

        for (let i = 1; i <= N; i += 1) {
            xNew = g(x);
            const E = Math.abs(xNew - x);

            steps.push({
                step: i,
                phase: "fixed_point",
                x,
                g_x: xNew,
                error: E,
                description: `Iter ${i}: x = ${x.toPrecision(10)}, g(x) = ${xNew.toPrecision(10)}, E = ${E.toExponential(6)}`,
            });

            if (E < tol) {
                steps[steps.length - 1].phase = "converged";
                break;
            }

            x = xNew;
        }

        return {
            solution: [xNew],
            root: xNew,
            steps,
            iterations: steps.length,
            method: "punto_fijo",
        };
    }

    global.puntoFijo = puntoFijo;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.puntoFijo = puntoFijo;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = puntoFijo;
    }
}(typeof window !== "undefined" ? window : globalThis));
