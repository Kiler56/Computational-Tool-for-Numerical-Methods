/**
 * trisection.js
 * Wrapper del metodo Trisección.
 */
(function (global) {
    function trisection(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.trisection) {
            throw new Error("trisection no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.trisection(expr, params);
    }

    global.trisection = trisection;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = trisection;
    }
}(typeof window !== "undefined" ? window : globalThis));
