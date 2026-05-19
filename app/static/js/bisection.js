/**
 * bisection.js
 * Implementacion individual del metodo de Biseccion.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { makeFunction } = shared;

    function bisection(expr, params = {}) {
        const f = makeFunction(expr);
        let a = Number(params.a ?? 0);
        let b = Number(params.b ?? 2);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);

        let fa = f(a);
        const fb = f(b);
        if (fa * fb > 0) {
            throw new Error("f(a) y f(b) deben tener signos opuestos.");
        }

        const steps = [];
        let xm = (a + b) / 2;
        let E = null;

        for (let i = 1; i <= N; i += 1) {
            const fxm = f(xm);
            steps.push({
                step: i,
                phase: "bisection",
                a,
                b,
                xm,
                f_xm: fxm,
                error: E,
                description: `Iter ${i}: xm = ${xm.toPrecision(10)}, f(xm) = ${fxm.toExponential(6)}${E !== null ? `, E = ${E.toExponential(6)}` : ""}`,
            });

            if (fa * fxm < 0) {
                b = xm;
            } else {
                a = xm;
                fa = f(a);
            }

            const xOld = xm;
            xm = (a + b) / 2;
            E = Math.abs(xm - xOld);

            if (E < tol) {
                steps.push({
                    step: i + 1,
                    phase: "converged",
                    description: `Convergio: xm = ${xm.toPrecision(10)}, E = ${E.toExponential(6)}`,
                    a,
                    b,
                    xm,
                    f_xm: f(xm),
                    error: E,
                });
                break;
            }
        }

        return {
            solution: [xm],
            root: xm,
            steps,
            iterations: steps.length,
            method: "bisection",
        };
    }

    global.bisection = bisection;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.bisection = bisection;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = bisection;
    }
}(typeof window !== "undefined" ? window : globalThis));
