/**
 * numerical_methods_shared.js
 * Utilidades compartidas para los metodos numericos portados a JavaScript.
 */
(function (global) {
    const EPSILON = 1e-12;

    function snapshot(value) {
        return JSON.parse(JSON.stringify(value));
    }

    function validateSystem(A, b) {
        if (!Array.isArray(A) || !Array.isArray(b) || A.length !== b.length || A.length === 0) {
            throw new Error("Sistema invalido: A y b deben tener el mismo tamano y n > 0.");
        }

        const n = b.length;
        for (let i = 0; i < n; i += 1) {
            if (!Array.isArray(A[i]) || A[i].length !== n) {
                throw new Error("La matriz A debe ser cuadrada.");
            }
        }

        return n;
    }

    function formatNumber(value) {
        if (!Number.isFinite(value)) {
            return String(value);
        }
        if (Math.abs(value) < 1e-15) {
            return "0";
        }
        return Number(value.toPrecision(6)).toString();
    }

    const SAFE_MATH = {
        sin: Math.sin,
        cos: Math.cos,
        tan: Math.tan,
        asin: Math.asin,
        acos: Math.acos,
        atan: Math.atan,
        sinh: Math.sinh,
        cosh: Math.cosh,
        tanh: Math.tanh,
        exp: Math.exp,
        log: Math.log,
        log10: Math.log10,
        log2: Math.log2,
        sqrt: Math.sqrt,
        abs: Math.abs,
        pi: Math.PI,
        e: Math.E,
        inf: Infinity,
    };

    function normalizeExpression(expr) {
        let normalized = String(expr ?? "").trim();
        const powerFunctions = [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "sinh",
            "cosh",
            "tanh",
            "exp",
            "log",
            "log10",
            "log2",
            "sqrt",
            "abs",
        ];

        normalized = normalized.replace(/\bln\s*\(/g, "log(");
        normalized = normalized.replace(/\be\s*\^\s*\(([^()]+)\)/g, "exp($1)");
        normalized = normalized.replace(/\be\s*\^\s*([A-Za-z0-9_.]+)/g, "exp($1)");

        for (const fnName of powerFunctions) {
            const regex = new RegExp(`\\b${fnName}\\s*\\^\\s*([\\d.]+)\\s*\\(([^()]+)\\)`, "g");
            normalized = normalized.replace(regex, `(${fnName}($2))**$1`);
        }

        normalized = normalized.replace(/\^/g, "**");
        return normalized;
    }

    function makeFunction(expr) {
        const normalizedExpr = normalizeExpression(expr);
        return function f(x) {
            const scope = { x, ...SAFE_MATH };
            const keys = Object.keys(scope);
            const values = Object.values(scope);

            try {
                return Number(Function(...keys, `"use strict"; return (${normalizedExpr});`)(...values));
            } catch (err) {
                throw new Error(`Expresion invalida: ${err.message}`);
            }
        };
    }

    function numericalDerivative(f, x, h = 1e-8) {
        return (f(x + h) - f(x - h)) / (2 * h);
    }

    function deriv(f, x, h = 1e-5) {
        return (f(x + h) - f(x - h)) / (2 * h);
    }

    function deriv2(f, x, h = 1e-5) {
        return (f(x + h) - (2 * f(x)) + f(x - h)) / (h ** 2);
    }

    function validateTridiagonal(A, n) {
        for (let i = 0; i < n; i += 1) {
            for (let j = 0; j < n; j += 1) {
                if (Math.abs(i - j) > 1 && Math.abs(A[i][j]) > EPSILON) {
                    throw new Error(`La matriz NO es tridiagonal: A[${i}][${j}] = ${A[i][j]} != 0. Use otro metodo.`);
                }
            }
        }
    }

    const api = {
        EPSILON,
        SAFE_MATH,
        snapshot,
        validateSystem,
        formatNumber,
        normalizeExpression,
        makeFunction,
        numericalDerivative,
        deriv,
        deriv2,
        validateTridiagonal,
    };

    global.NumericalMethodsShared = api;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = api;
    }
}(typeof window !== "undefined" ? window : globalThis));
