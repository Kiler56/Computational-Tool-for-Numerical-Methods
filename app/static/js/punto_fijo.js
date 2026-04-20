/**
 * punto_fijo.js
 * Wrapper del metodo Punto Fijo.
 */
(function (global) {
    function puntoFijo(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.puntoFijo) {
            throw new Error("puntoFijo no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.puntoFijo(expr, params);
    }

    global.puntoFijo = puntoFijo;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = puntoFijo;
    }
}(typeof window !== "undefined" ? window : globalThis));
