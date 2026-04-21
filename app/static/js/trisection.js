/**
 * trisection.js
 * Implementacion individual del metodo de Triseccion.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { makeFunction } = shared;

    function trisection(expr, params = {}) {
        const f = makeFunction(expr);
        let a = Number(params.a ?? 0);
        let b = Number(params.b ?? 2);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);

        const steps = [];
        let E = null;

        for (let i = 1; i <= N; i += 1) {
            const x1 = a + ((b - a) / 3);
            const x2 = b - ((b - a) / 3);
            const fa = f(a);
            const fx1 = f(x1);
            const fx2 = f(x2);

            steps.push({
                step: i,
                phase: "trisection",
                a,
                b,
                x1,
                x2,
                f_x1: fx1,
                f_x2: fx2,
                error: E,
                description: `Iter ${i}: x1 = ${x1.toPrecision(10)}, x2 = ${x2.toPrecision(10)}, f(x1) = ${fx1.toExponential(6)}, f(x2) = ${fx2.toExponential(6)}${E !== null ? `, E = ${E.toExponential(6)}` : ""}`,
            });

            if (fx1 === 0) {
                a = x1;
                b = x1;
            } else if (fx2 === 0) {
                a = x2;
                b = x2;
            } else if (fa * fx1 < 0) {
                b = x1;
            } else if (fx1 * fx2 < 0) {
                a = x1;
                b = x2;
            } else {
                a = x2;
            }

            E = Math.abs(b - a);
            if (E < tol) {
                break;
            }
        }

        const root = (a + b) / 2;
        return {
            solution: [root],
            root,
            steps,
            iterations: steps.length,
            method: "trisection",
        };
    }

    global.trisection = trisection;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.trisection = trisection;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = trisection;
    }
}(typeof window !== "undefined" ? window : globalThis));
