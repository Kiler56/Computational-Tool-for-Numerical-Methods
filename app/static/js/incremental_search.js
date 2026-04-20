/**
 * incremental_search.js
 * Wrapper del metodo Búsqueda Incremental.
 */
(function (global) {
    function incrementalSearch(expr, params) {
        if (!global.NumericalMethodsJS || !global.NumericalMethodsJS.incrementalSearch) {
            throw new Error("incrementalSearch no esta disponible en NumericalMethodsJS.");
        }
        return global.NumericalMethodsJS.incrementalSearch(expr, params);
    }

    global.incrementalSearch = incrementalSearch;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = incrementalSearch;
    }
}(typeof window !== "undefined" ? window : globalThis));
