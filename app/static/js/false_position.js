/**
 * false_position.js
 * Wrapper del metodo Regla Falsa.
 */
(function (global) {
    function falsePosition(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.falsePosition) {
            throw new Error("falsePosition no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.falsePosition(expr, params);
    }

    global.falsePosition = falsePosition;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = falsePosition;
    }
}(typeof window !== "undefined" ? window : globalThis));
