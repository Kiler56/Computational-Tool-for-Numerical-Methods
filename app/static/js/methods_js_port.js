/**
 * methods_js_port.js
 * Traduccion de metodos numericos de Python a JavaScript.
 * Se puede usar en navegador (window.NumericalMethodsJS) y en Node (module.exports).
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
        if (!Number.isFinite(value)) return String(value);
        if (Math.abs(value) < 1e-15) return "0";
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

    function makeFunction(expr) {
        return function f(x) {
            const scope = { x, ...SAFE_MATH };
            const keys = Object.keys(scope);
            const values = Object.values(scope);
            try {
                return Number(Function(...keys, `"use strict"; return (${expr});`)(...values));
            } catch (err) {
                throw new Error(`Expresion invalida: ${err.message}`);
            }
        };
    }

    function incrementalSearch(expr, params = {}) {
        const f = makeFunction(expr);
        const x0 = Number(params.x0 ?? -3);
        const h = Number(params.h ?? 0.5);
        const N = Number(params.max_iter ?? 100);

        let xPrev = x0;
        let fPrev = f(xPrev);
        const steps = [];
        const foundIntervals = [];

        for (let i = 1; i <= N; i += 1) {
            const xCurr = xPrev + h;
            const fCurr = f(xCurr);

            const step = {
                step: i,
                phase: "search",
                x_prev: xPrev,
                x_curr: xCurr,
                f_prev: fPrev,
                f_curr: fCurr,
                description: `Iter ${i}: [${xPrev.toPrecision(6)}, ${xCurr.toPrecision(6)}], f = [${fPrev.toExponential(6)}, ${fCurr.toExponential(6)}]`,
            };

            if (fPrev * fCurr < 0) {
                step.phase = "root_found";
                step.description += ` <- Raiz en [${xPrev.toPrecision(6)}, ${xCurr.toPrecision(6)}]`;
                foundIntervals.push([xPrev, xCurr]);
            }

            steps.push(step);
            xPrev = xCurr;
            fPrev = fCurr;
        }

        if (foundIntervals.length > 0) {
            const midpoint = (foundIntervals[0][0] + foundIntervals[0][1]) / 2;
            return {
                solution: [midpoint],
                root: midpoint,
                intervals: foundIntervals,
                steps,
                iterations: steps.length,
                method: "incremental_search",
            };
        }

        throw new Error("No se encontro ningun intervalo con cambio de signo en el rango explorado.");
    }

    function bisection(expr, params = {}) {
        const f = makeFunction(expr);
        let a = Number(params.a ?? 0);
        let b = Number(params.b ?? 2);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);

        let fa = f(a);
        const fb = f(b);
        if (fa * fb > 0) {
            throw new Error("f(a) y f(b) deben tener signos opuestos.");
        }

        const steps = [];
        let xm = (a + b) / 2;
        let E = null;

        for (let i = 1; i <= N; i += 1) {
            const fxm = f(xm);
            const step = {
                step: i,
                phase: "bisection",
                a,
                b,
                xm,
                f_xm: fxm,
                error: E,
                description: `Iter ${i}: xm = ${xm.toPrecision(10)}, f(xm) = ${fxm.toExponential(6)}${E !== null ? `, E = ${E.toExponential(6)}` : ""}`,
            };
            steps.push(step);

            if (fa * fxm < 0) {
                b = xm;
            } else {
                a = xm;
                fa = f(a);
            }

            const xOld = xm;
            xm = (a + b) / 2;
            E = Math.abs(xm - xOld);

            if (E < tol) {
                steps.push({
                    step: i + 1,
                    phase: "converged",
                    description: `Convergio: xm = ${xm.toPrecision(10)}, E = ${E.toExponential(6)}`,
                    a,
                    b,
                    xm,
                    f_xm: f(xm),
                    error: E,
                });
                break;
            }
        }

        return {
            solution: [xm],
            root: xm,
            steps,
            iterations: steps.length,
            method: "bisection",
        };
    }

    function falsePosition(expr, params = {}) {
        const f = makeFunction(expr);
        let a = Number(params.a ?? 0);
        let b = Number(params.b ?? 2);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);

        let fa = f(a);
        let fb = f(b);
        if (fa * fb > 0) {
            throw new Error("f(a) y f(b) deben tener signos opuestos.");
        }

        let xm = ((fb * a) - (fa * b)) / (fb - fa);
        const steps = [];
        let E = null;

        for (let i = 1; i <= N; i += 1) {
            const fxm = f(xm);
            steps.push({
                step: i,
                phase: "false_position",
                a,
                b,
                xm,
                f_xm: fxm,
                error: E,
                description: `Iter ${i}: xm = ${xm.toPrecision(10)}, f(xm) = ${fxm.toExponential(6)}${E !== null ? `, E = ${E.toExponential(6)}` : ""}`,
            });

            if (fa * fxm < 0) {
                b = xm;
                fb = f(b);
            } else {
                a = xm;
                fa = f(a);
            }

            const xOld = xm;
            xm = ((fb * a) - (fa * b)) / (fb - fa);
            E = Math.abs(xm - xOld);

            if (E < tol) {
                steps.push({
                    step: i + 1,
                    phase: "converged",
                    description: `Convergio: xm = ${xm.toPrecision(10)}, E = ${E.toExponential(6)}`,
                    a,
                    b,
                    xm,
                    f_xm: f(xm),
                    error: E,
                });
                break;
            }
        }

        return {
            solution: [xm],
            root: xm,
            steps,
            iterations: steps.length,
            method: "false_position",
        };
    }

    function trisection(expr, params = {}) {
        const f = makeFunction(expr);
        let a = Number(params.a ?? 0);
        let b = Number(params.b ?? 2);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);

        const steps = [];
        let E = null;

        for (let i = 1; i <= N; i += 1) {
            const x1 = a + ((b - a) / 3);
            const x2 = b - ((b - a) / 3);

            steps.push({
                step: i,
                phase: "trisection",
                a,
                b,
                x1,
                x2,
                f_x1: f(x1),
                f_x2: f(x2),
                error: E,
                description: `Iter ${i}: a=${a.toPrecision(8)}, x1=${x1.toPrecision(8)}, x2=${x2.toPrecision(8)}, b=${b.toPrecision(8)}${E ? `, E=${E.toExponential(6)}` : ""}`,
            });

            const fa = f(a);
            if (fa * f(x1) < 0) {
                b = x1;
            } else if (f(x1) * f(x2) < 0) {
                a = x1;
                b = x2;
            } else {
                a = x2;
            }

            E = Math.abs(b - a);
            if (E < tol) {
                break;
            }
        }

        const xm = (a + b) / 2;
        steps.push({
            step: steps.length + 1,
            phase: "converged",
            description: `Convergio: raiz ≈ ${xm.toPrecision(10)}, E = ${E.toExponential(6)}`,
            a,
            b,
            xm,
            f_xm: f(xm),
            error: E,
        });

        return {
            solution: [xm],
            root: xm,
            steps,
            iterations: steps.length,
            method: "trisection",
        };
    }

    function numericalDerivative(f, x, h = 1e-8) {
        return (f(x + h) - f(x - h)) / (2 * h);
    }

    function newton(expr, params = {}) {
        const f = makeFunction(expr);
        let x = Number(params.x0 ?? 1.5);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let xNew = x;

        for (let i = 1; i <= N; i += 1) {
            const fx = f(x);
            const dfx = numericalDerivative(f, x);

            if (Math.abs(dfx) < 1e-15) {
                throw new Error(`Derivada cero en x = ${x.toPrecision(10)}. No se puede continuar.`);
            }

            xNew = x - (fx / dfx);
            const E = Math.abs(xNew - x);

            steps.push({
                step: i,
                phase: "newton",
                x,
                f_x: fx,
                df_x: dfx,
                x_new: xNew,
                error: E,
                description: `Iter ${i}: x = ${x.toPrecision(10)}, f(x) = ${fx.toExponential(6)}, f'(x) = ${dfx.toExponential(6)}, x_new = ${xNew.toPrecision(10)}, E = ${E.toExponential(6)}`,
            });

            if (E < tol) {
                steps[steps.length - 1].phase = "converged";
                break;
            }

            x = xNew;
        }

        return {
            solution: [xNew],
            root: xNew,
            steps,
            iterations: steps.length,
            method: "newton",
        };
    }

    function puntoFijo(expr, params = {}) {
        const g = makeFunction(expr);
        let x = Number(params.x0 ?? 1.5);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let xNew = x;

        for (let i = 1; i <= N; i += 1) {
            xNew = g(x);
            const E = Math.abs(xNew - x);

            steps.push({
                step: i,
                phase: "fixed_point",
                x,
                g_x: xNew,
                error: E,
                description: `Iter ${i}: x = ${x.toPrecision(10)}, g(x) = ${xNew.toPrecision(10)}, E = ${E.toExponential(6)}`,
            });

            if (E < tol) {
                steps[steps.length - 1].phase = "converged";
                break;
            }

            x = xNew;
        }

        return {
            solution: [xNew],
            root: xNew,
            steps,
            iterations: steps.length,
            method: "punto_fijo",
        };
    }

    function secante(expr, params = {}) {
        const f = makeFunction(expr);
        let x0 = Number(params.x0 ?? 0);
        let x1 = Number(params.x1 ?? 2);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let x2 = x1;

        for (let i = 1; i <= N; i += 1) {
            const f0 = f(x0);
            const f1 = f(x1);
            const denom = f1 - f0;
            if (Math.abs(denom) < 1e-15) {
                throw new Error(`Division por cero: f(x1) - f(x0) ≈ 0 en iteracion ${i}.`);
            }

            x2 = x1 - ((f1 * (x1 - x0)) / denom);
            const E = Math.abs(x2 - x1);

            steps.push({
                step: i,
                phase: "secante",
                x0,
                x1,
                x2,
                f_x0: f0,
                f_x1: f1,
                error: E,
                description: `Iter ${i}: x0=${x0.toPrecision(8)}, x1=${x1.toPrecision(8)}, x2=${x2.toPrecision(10)}, E = ${E.toExponential(6)}`,
            });

            if (E < tol) {
                steps[steps.length - 1].phase = "converged";
                break;
            }

            x0 = x1;
            x1 = x2;
        }

        return {
            solution: [x2],
            root: x2,
            steps,
            iterations: steps.length,
            method: "secante",
        };
    }

    function deriv(f, x, h = 1e-5) {
        return (f(x + h) - f(x - h)) / (2 * h);
    }

    function deriv2(f, x, h = 1e-5) {
        return (f(x + h) - (2 * f(x)) + f(x - h)) / (h ** 2);
    }

    function raicesMultiples(expr, params = {}) {
        const f = makeFunction(expr);
        let x = Number(params.x0 ?? 1.5);
        const tol = Number(params.tol ?? 1e-7);
        const N = Number(params.max_iter ?? 100);
        const steps = [];
        let xNew = x;

        for (let i = 1; i <= N; i += 1) {
            const fx = f(x);
            const dfx = deriv(f, x);
            const d2fx = deriv2(f, x);

            const denom = (dfx ** 2) - (fx * d2fx);
            if (Math.abs(denom) < 1e-15) {
                throw new Error(`Division por cero en iteracion ${i}: f'² - f·f'' ≈ 0.`);
            }

            xNew = x - ((fx * dfx) / denom);
            const E = Math.abs(xNew - x);

            steps.push({
                step: i,
                phase: "multiple_roots",
                x,
                f_x: fx,
                df_x: dfx,
                d2f_x: d2fx,
                x_new: xNew,
                error: E,
                description: `Iter ${i}: x=${x.toPrecision(10)}, f=${fx.toExponential(6)}, f'=${dfx.toExponential(6)}, f''=${d2fx.toExponential(6)}, x_new=${xNew.toPrecision(10)}, E=${E.toExponential(6)}`,
            });

            if (E < tol) {
                steps[steps.length - 1].phase = "converged";
                break;
            }

            x = xNew;
        }

        return {
            solution: [xNew],
            root: xNew,
            steps,
            iterations: steps.length,
            method: "raices_multiples",
        };
    }

    function gaussianSimple(A, b) {
        const n = validateSystem(A, b);
        const M = A.map((row, i) => [...row, b[i]]);
        const steps = [];

        for (let k = 0; k < n - 1; k += 1) {
            const pivot = M[k][k];
            if (Math.abs(pivot) < EPSILON) {
                throw new Error(`Pivote cero (o casi cero) en la fila ${k}. Use un metodo con pivoteo.`);
            }

            steps.push({
                step: steps.length + 1,
                phase: "elimination",
                description: `Pivote en posicion (${k},${k}) = ${formatNumber(pivot)}`,
                pivot,
                matrix_state: snapshot(M),
            });

            for (let i = k + 1; i < n; i += 1) {
                const factor = M[i][k] / pivot;
                for (let j = k; j <= n; j += 1) {
                    M[i][j] -= factor * M[k][j];
                }
                steps.push({
                    step: steps.length + 1,
                    phase: "elimination",
                    description: `F${i + 1} <- F${i + 1} - (${formatNumber(factor)})*F${k + 1}`,
                    factor,
                    matrix_state: snapshot(M),
                });
            }
        }

        const x = Array(n).fill(0);
        for (let i = n - 1; i >= 0; i -= 1) {
            if (Math.abs(M[i][i]) < EPSILON) {
                throw new Error(`Sistema singular: pivote cero en fila ${i} durante sustitucion regresiva.`);
            }
            let s = 0;
            for (let j = i + 1; j < n; j += 1) {
                s += M[i][j] * x[j];
            }
            x[i] = (M[i][n] - s) / M[i][i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x[${i}] = (${formatNumber(M[i][n])} - ${formatNumber(s)}) / ${formatNumber(M[i][i])} = ${formatNumber(x[i])}`,
                matrix_state: snapshot(M),
            });
        }

        return { solution: x, steps, iterations: steps.length, method: "gaussian_simple" };
    }

    function gaussianPartialPivoting(A, b) {
        const n = validateSystem(A, b);
        const M = A.map((row, i) => [...row, b[i]]);
        const steps = [];

        for (let k = 0; k < n - 1; k += 1) {
            let maxVal = Math.abs(M[k][k]);
            let maxRow = k;
            for (let i = k + 1; i < n; i += 1) {
                if (Math.abs(M[i][k]) > maxVal) {
                    maxVal = Math.abs(M[i][k]);
                    maxRow = i;
                }
            }

            let swapInfo = null;
            if (maxRow !== k) {
                [M[k], M[maxRow]] = [M[maxRow], M[k]];
                swapInfo = [k, maxRow];
            }

            const pivot = M[k][k];
            if (Math.abs(pivot) < EPSILON) {
                throw new Error(`Sistema singular: pivote cero en columna ${k} incluso despues de pivoteo parcial.`);
            }

            steps.push({
                step: steps.length + 1,
                phase: "elimination",
                description: `Pivote parcial en columna ${k}: valor = ${formatNumber(pivot)}`,
                pivot,
                swap_rows: swapInfo,
                matrix_state: snapshot(M),
            });

            for (let i = k + 1; i < n; i += 1) {
                const factor = M[i][k] / pivot;
                for (let j = k; j <= n; j += 1) {
                    M[i][j] -= factor * M[k][j];
                }
                steps.push({
                    step: steps.length + 1,
                    phase: "elimination",
                    description: `F${i + 1} <- F${i + 1} - (${formatNumber(factor)})*F${k + 1}`,
                    factor,
                    matrix_state: snapshot(M),
                });
            }
        }

        const x = Array(n).fill(0);
        for (let i = n - 1; i >= 0; i -= 1) {
            if (Math.abs(M[i][i]) < EPSILON) {
                throw new Error(`Sistema singular en sustitucion regresiva (fila ${i}).`);
            }
            let s = 0;
            for (let j = i + 1; j < n; j += 1) {
                s += M[i][j] * x[j];
            }
            x[i] = (M[i][n] - s) / M[i][i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x[${i}] = ${formatNumber(x[i])}`,
                matrix_state: snapshot(M),
            });
        }

        return { solution: x, steps, iterations: steps.length, method: "gaussian_partial_pivoting" };
    }

    function gaussianTotalPivoting(A, b) {
        const n = validateSystem(A, b);
        const M = A.map((row, i) => [...row, b[i]]);
        const colOrder = Array.from({ length: n }, (_, i) => i);
        const steps = [];

        for (let k = 0; k < n - 1; k += 1) {
            let maxVal = Math.abs(M[k][k]);
            let maxRow = k;
            let maxCol = k;

            for (let i = k; i < n; i += 1) {
                for (let j = k; j < n; j += 1) {
                    if (Math.abs(M[i][j]) > maxVal) {
                        maxVal = Math.abs(M[i][j]);
                        maxRow = i;
                        maxCol = j;
                    }
                }
            }

            let rowSwap = null;
            if (maxRow !== k) {
                [M[k], M[maxRow]] = [M[maxRow], M[k]];
                rowSwap = [k, maxRow];
            }

            let colSwap = null;
            if (maxCol !== k) {
                for (const row of M) {
                    [row[k], row[maxCol]] = [row[maxCol], row[k]];
                }
                [colOrder[k], colOrder[maxCol]] = [colOrder[maxCol], colOrder[k]];
                colSwap = [k, maxCol];
            }

            const pivot = M[k][k];
            if (Math.abs(pivot) < EPSILON) {
                throw new Error(`Sistema singular: pivote cero en paso ${k} incluso despues de pivoteo total.`);
            }

            steps.push({
                step: steps.length + 1,
                phase: "elimination",
                description: `Pivote total en paso ${k}: valor = ${formatNumber(pivot)}`,
                pivot,
                max_val: maxVal,
                swap_rows: rowSwap,
                swap_cols: colSwap,
                matrix_state: snapshot(M),
            });

            for (let i = k + 1; i < n; i += 1) {
                const factor = M[i][k] / pivot;
                for (let j = k; j <= n; j += 1) {
                    M[i][j] -= factor * M[k][j];
                }
                steps.push({
                    step: steps.length + 1,
                    phase: "elimination",
                    description: `F${i + 1} <- F${i + 1} - (${formatNumber(factor)})*F${k + 1}`,
                    factor,
                    matrix_state: snapshot(M),
                });
            }
        }

        const xPerm = Array(n).fill(0);
        for (let i = n - 1; i >= 0; i -= 1) {
            if (Math.abs(M[i][i]) < EPSILON) {
                throw new Error(`Sistema singular en sustitucion regresiva (fila ${i}).`);
            }
            let s = 0;
            for (let j = i + 1; j < n; j += 1) {
                s += M[i][j] * xPerm[j];
            }
            xPerm[i] = (M[i][n] - s) / M[i][i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x_perm[${i}] = ${formatNumber(xPerm[i])}`,
                matrix_state: snapshot(M),
            });
        }

        const x = Array(n).fill(0);
        for (let i = 0; i < n; i += 1) {
            x[colOrder[i]] = xPerm[i];
        }
        steps.push({
            step: steps.length + 1,
            phase: "reorder",
            description: `Reordenamiento de columnas: [${colOrder.join(", ")}] -> solucion final`,
            col_permutation: snapshot(colOrder),
            matrix_state: snapshot(M),
        });

        return { solution: x, steps, iterations: steps.length, method: "gaussian_total_pivoting" };
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

    function gaussTridiagonal(A, b) {
        const n = validateSystem(A, b);
        validateTridiagonal(A, n);

        const a = [0, ...Array.from({ length: n - 1 }, (_, i) => A[i + 1][i])];
        const d = Array.from({ length: n }, (_, i) => A[i][i]);
        const c = [...Array.from({ length: n - 1 }, (_, i) => A[i][i + 1]), 0];
        const r = [...b];
        const steps = [];

        steps.push({
            step: 1,
            phase: "extract",
            description: "Vectores extraidos de la matriz tridiagonal",
            sub_diagonal: snapshot(a),
            main_diagonal: snapshot(d),
            super_diagonal: snapshot(c),
            rhs: snapshot(r),
        });

        for (let i = 1; i < n; i += 1) {
            if (Math.abs(d[i - 1]) < EPSILON) {
                throw new Error(`Division por cero en forward sweep (d[${i - 1}] = ${d[i - 1]}).`);
            }
            const w = a[i] / d[i - 1];
            d[i] = d[i] - w * c[i - 1];
            r[i] = r[i] - w * r[i - 1];
            steps.push({
                step: steps.length + 1,
                phase: "forward_sweep",
                description: `i=${i}: w = a[${i}]/d[${i - 1}] = ${formatNumber(w)}, d[${i}] = ${formatNumber(d[i])}, r[${i}] = ${formatNumber(r[i])}`,
                w,
                main_diagonal: snapshot(d),
                rhs: snapshot(r),
            });
        }

        const x = Array(n).fill(0);
        if (Math.abs(d[n - 1]) < EPSILON) {
            throw new Error(`Division por cero en back substitution (d[${n - 1}] = ${d[n - 1]}).`);
        }
        x[n - 1] = r[n - 1] / d[n - 1];
        steps.push({
            step: steps.length + 1,
            phase: "back_substitution",
            description: `x[${n - 1}] = r[${n - 1}] / d[${n - 1}] = ${formatNumber(x[n - 1])}`,
            solution_partial: snapshot(x),
        });

        for (let i = n - 2; i >= 0; i -= 1) {
            if (Math.abs(d[i]) < EPSILON) {
                throw new Error(`Division por cero en back substitution (d[${i}] = ${d[i]}).`);
            }
            x[i] = (r[i] - c[i] * x[i + 1]) / d[i];
            steps.push({
                step: steps.length + 1,
                phase: "back_substitution",
                description: `x[${i}] = (r[${i}] - c[${i}]*x[${i + 1}]) / d[${i}] = ${formatNumber(x[i])}`,
                solution_partial: snapshot(x),
            });
        }

        return {
            solution: x,
            steps,
            iterations: steps.length,
            lower: snapshot(a),
            upper: snapshot(c),
            method: "gauss_tridiagonal",
        };
    }

    const methodSolvers = {
        gaussian_simple: gaussianSimple,
        gaussian_partial_pivoting: gaussianPartialPivoting,
        gaussian_total_pivoting: gaussianTotalPivoting,
        gauss_tridiagonal: gaussTridiagonal,
        incremental_search: incrementalSearch,
        bisection,
        false_position: falsePosition,
        trisection,
        newton,
        punto_fijo: puntoFijo,
        secante,
        raices_multiples: raicesMultiples,
    };

    function solve(methodName, inputA, inputB) {
        const solver = methodSolvers[methodName];
        if (!solver) {
            throw new Error(`Metodo no soportado en JavaScript: ${methodName}`);
        }
        return solver(inputA, inputB);
    }

    const api = {
        solve,
        gaussianSimple,
        gaussianPartialPivoting,
        gaussianTotalPivoting,
        gaussTridiagonal,
        incrementalSearch,
        bisection,
        falsePosition,
        trisection,
        newton,
        puntoFijo,
        secante,
        raicesMultiples,
    };

    global.NumericalMethodsJS = api;
    if (typeof module !== "undefined" && module.exports) {
        module.exports = api;
    }
}(typeof window !== "undefined" ? window : globalThis));
