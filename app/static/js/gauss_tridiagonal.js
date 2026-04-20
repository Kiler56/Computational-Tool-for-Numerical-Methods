/**
 * gauss_tridiagonal.js
 * Wrapper del metodo Gauss Tridiagonal (Thomas).
 */
(function (global) {
    function gaussTridiagonal(A, b) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.gaussTridiagonal) {
            throw new Error("gaussTridiagonal no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.gaussTridiagonal(A, b);
    }

    global.gaussTridiagonal = gaussTridiagonal;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = gaussTridiagonal;
    }
}(typeof window !== "undefined" ? window : globalThis));
