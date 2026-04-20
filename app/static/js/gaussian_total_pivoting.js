/**
 * gaussian_total_pivoting.js
 * Wrapper del metodo Pivoteo Total.
 */
(function (global) {
    function gaussianTotalPivoting(A, b) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.gaussianTotalPivoting) {
            throw new Error("gaussianTotalPivoting no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.gaussianTotalPivoting(A, b);
    }

    global.gaussianTotalPivoting = gaussianTotalPivoting;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussianTotalPivoting;
    }
}(typeof window !== "undefined" ? window : globalThis));
