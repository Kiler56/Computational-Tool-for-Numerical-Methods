/**
 * newton.js
 * Implementacion individual del metodo de Newton-Raphson.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { makeFunction, numericalDerivative } = shared;

    function newton(expr, params = {}) {
        const f = makeFunction(expr);
        let x = Number(params.x0 ?? 1.5);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let xNew = x;

        for (let i = 1; i <= N; i += 1) {
            const fx = f(x);
            const dfx = numericalDerivative(f, x);

            if (Math.abs(dfx) < 1e-15) {
                throw new Error(`Derivada cero en x = ${x.toPrecision(10)}. No se puede continuar.`);
            }

            xNew = x - (fx / dfx);
            const E = Math.abs(xNew - x);

            steps.push({
                step: i,
                phase: "newton",
                x,
                f_x: fx,
                df_x: dfx,
                x_new: xNew,
                error: E,
                description: `Iter ${i}: x = ${x.toPrecision(10)}, f(x) = ${fx.toExponential(6)}, f'(x) = ${dfx.toExponential(6)}, x_new = ${xNew.toPrecision(10)}, E = ${E.toExponential(6)}`,
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
            method: "newton",
        };
    }

    global.newton = newton;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.newton = newton;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = newton;
    }
}(typeof window !== "undefined" ? window : globalThis));
