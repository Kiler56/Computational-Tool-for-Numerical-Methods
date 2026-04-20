/**
 * secante.js
 * Wrapper del metodo Secante.
 */
(function (global) {
    function secante(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.secante) {
            throw new Error("secante no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.secante(expr, params);
    }

    global.secante = secante;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = secante;
    }
}(typeof window !== "undefined" ? window : globalThis));
