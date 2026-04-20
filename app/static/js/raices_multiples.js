/**
 * raices_multiples.js
 * Wrapper del metodo Raíces Múltiples.
 */
(function (global) {
    function raicesMultiples(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.raicesMultiples) {
            throw new Error("raicesMultiples no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.raicesMultiples(expr, params);
    }

    global.raicesMultiples = raicesMultiples;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = raicesMultiples;
    }
}(typeof window !== "undefined" ? window : globalThis));
