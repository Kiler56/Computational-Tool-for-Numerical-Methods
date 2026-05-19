/**
 * raices_multiples.js
 * Implementacion individual del metodo de Raices Multiples.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { makeFunction, deriv, deriv2 } = shared;

    function raicesMultiples(expr, params = {}) {
        const f = makeFunction(expr);
        let x = Number(params.x0 ?? 1.5);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let xNew = x;

        for (let i = 1; i <= N; i += 1) {
            const fx = f(x);
            const dfx = deriv(f, x);
            const d2fx = deriv2(f, x);
            const denom = (dfx ** 2) - (fx * d2fx);

            if (denom === 0) {
                throw new Error(`Division por cero en iteracion ${i}: f'^2 - f*f'' = 0.`);
            }

            xNew = x - ((fx * dfx) / denom);
            const E = Math.abs(xNew - x);

            steps.push({
                step: i,
                phase: "multiple_roots",
                x,
                f_x: fx,
                df_x: dfx,
                d2f_x: d2fx,
                x_new: xNew,
                error: E,
                description: `Iter ${i}: x=${x.toPrecision(10)}, f=${fx.toExponential(6)}, f'=${dfx.toExponential(6)}, f''=${d2fx.toExponential(6)}, x_new=${xNew.toPrecision(10)}, E=${E.toExponential(6)}`,
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
            method: "raices_multiples",
        };
    }

    global.raicesMultiples = raicesMultiples;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.raicesMultiples = raicesMultiples;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = raicesMultiples;
    }
}(typeof window !== "undefined" ? window : globalThis));
