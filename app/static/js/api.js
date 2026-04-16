/**
 * api.js — Wrapper fetch() para la API interna del monolito.
 */

/**
 * Envía la matriz y el vector al backend para resolver con el método indicado.
 * @param {string} methodName  - slug del método (e.g. "gaussian_simple")
 * @param {number[][]} matrix  - Matriz A (nxn)
 * @param {number[]} b         - Vector b
 * @returns {Promise<Object>}  - Respuesta JSON del backend
 */
async function solveMethod(methodName, matrix, b) {
    const response = await fetch('/api/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ method: methodName, matrix, b }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || `Error HTTP ${response.status}`);
    }

    return data;
}
