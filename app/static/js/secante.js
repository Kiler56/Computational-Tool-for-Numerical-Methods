/**
 * secante.js
 * Implementacion individual del metodo de la Secante.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { makeFunction } = shared;

    function secante(expr, params = {}) {
        const f = makeFunction(expr);
        let x0 = Number(params.x0 ?? 0);
        let x1 = Number(params.x1 ?? 1);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let x2 = x1;

        for (let i = 1; i <= N; i += 1) {
            const fx0 = f(x0);
            const fx1 = f(x1);
            const denom = fx1 - fx0;

            if (Math.abs(denom) < 1e-15) {
                throw new Error(`Division por cero en iteracion ${i}: f(x1) - f(x0) = 0.`);
            }

            x2 = x1 - ((fx1 * (x1 - x0)) / denom);
            const E = Math.abs(x2 - x1);

            steps.push({
                step: i,
                phase: "secant",
                x0,
                x1,
                x2,
                f_x0: fx0,
                f_x1: fx1,
                error: E,
                description: `Iter ${i}: x0 = ${x0.toPrecision(10)}, x1 = ${x1.toPrecision(10)}, x2 = ${x2.toPrecision(10)}, E = ${E.toExponential(6)}`,
            });

            if (E < tol) {
                steps[steps.length - 1].phase = "converged";
                break;
            }

            x0 = x1;
            x1 = x2;
        }

        return {
            solution: [x2],
            root: x2,
            steps,
            iterations: steps.length,
            method: "secante",
        };
    }

    global.secante = secante;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.secante = secante;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = secante;
    }
}(typeof window !== "undefined" ? window : globalThis));
