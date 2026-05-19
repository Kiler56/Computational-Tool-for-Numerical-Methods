/**
 * incremental_search.js
 * Implementacion individual de Busqueda Incremental.
 */
(function (global) {
    const shared = global.NumericalMethodsShared || (typeof require !== "undefined" ? require("./numerical_methods_shared") : null);
    if (!shared) {
        throw new Error("NumericalMethodsShared no esta disponible.");
    }

    const { makeFunction } = shared;

    function incrementalSearch(expr, params = {}) {
        const f = makeFunction(expr);
        const x0 = Number(params.x0 ?? -3);
        const h = Number(params.h ?? 0.5);
        const N = Number(params.max_iter ?? 100);

        let xPrev = x0;
        let fPrev = f(xPrev);
        const steps = [];
        const foundIntervals = [];

        for (let i = 1; i <= N; i += 1) {
            const xCurr = xPrev + h;
            const fCurr = f(xCurr);

            const step = {
                step: i,
                phase: "search",
                x_prev: xPrev,
                x_curr: xCurr,
                f_prev: fPrev,
                f_curr: fCurr,
                description: `Iter ${i}: [${xPrev.toPrecision(6)}, ${xCurr.toPrecision(6)}], f = [${fPrev.toExponential(6)}, ${fCurr.toExponential(6)}]`,
            };

            if (fPrev * fCurr < 0) {
                step.phase = "root_found";
                step.description += ` <- Raiz en [${xPrev.toPrecision(6)}, ${xCurr.toPrecision(6)}]`;
                foundIntervals.push([xPrev, xCurr]);
            }

            steps.push(step);
            xPrev = xCurr;
            fPrev = fCurr;
        }

        if (foundIntervals.length > 0) {
            const midpoint = (foundIntervals[0][0] + foundIntervals[0][1]) / 2;
            return {
                solution: [midpoint],
                root: midpoint,
                intervals: foundIntervals,
                steps,
                iterations: steps.length,
                method: "incremental_search",
            };
        }

        throw new Error("No se encontro ningun intervalo con cambio de signo en el rango explorado.");
    }

    global.incrementalSearch = incrementalSearch;
    global.NumericalMethodsJS = global.NumericalMethodsJS || {};
    global.NumericalMethodsJS.incrementalSearch = incrementalSearch;

    if (typeof module !== "undefined" && module.exports) {
        module.exports = incrementalSearch;
    }
}(typeof window !== "undefined" ? window : globalThis));
