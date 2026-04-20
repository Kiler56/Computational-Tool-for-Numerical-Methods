/**
 * bisection.js
 * Wrapper del metodo Bisección.
 */
(function (global) {
    function bisection(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.bisection) {
            throw new Error("bisection no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.bisection(expr, params);
    }

    global.bisection = bisection;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = bisection;
    }
}(typeof window !== "undefined" ? window : globalThis));
