/**
 * gaussian_partial_pivoting.js
 * Wrapper del metodo Pivoteo Parcial.
 */
(function (global) {
    function gaussianPartialPivoting(A, b) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.gaussianPartialPivoting) {
            throw new Error("gaussianPartialPivoting no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.gaussianPartialPivoting(A, b);
    }

    global.gaussianPartialPivoting = gaussianPartialPivoting;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussianPartialPivoting;
    }
}(typeof window !== "undefined" ? window : globalThis));
