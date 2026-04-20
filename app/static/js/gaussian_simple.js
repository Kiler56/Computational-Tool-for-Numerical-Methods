/**
 * gaussian_simple.js
 * Wrapper del metodo Eliminación Gaussiana Simple.
 */
(function (global) {
    function gaussianSimple(A, b) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.gaussianSimple) {
            throw new Error("gaussianSimple no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.gaussianSimple(A, b);
    }

    global.gaussianSimple = gaussianSimple;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussianSimple;
    }
}(typeof window !== "undefined" ? window : globalThis));
