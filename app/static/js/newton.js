/**
 * newton.js
 * Wrapper del metodo Newton-Raphson.
 */
(function (global) {
    function newton(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.newton) {
            throw new Error("newton no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.newton(expr, params);
    }

    global.newton = newton;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = newton;
    }
}(typeof window !== "undefined" ? window : globalThis));
