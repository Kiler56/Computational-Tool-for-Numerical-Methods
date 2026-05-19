const methods = {
    incrementalSearch: require("./app/static/js/incremental_search"),
    bisection: require("./app/static/js/bisection"),
    falsePosition: require("./app/static/js/false_position"),
    trisection: require("./app/static/js/trisection"),
    newton: require("./app/static/js/newton"),
    puntoFijo: require("./app/static/js/punto_fijo"),
    secante: require("./app/static/js/secante"),
    raicesMultiples: require("./app/static/js/raices_multiples"),
    gaussianSimple: require("./app/static/js/gaussian_simple"),
    gaussianPartialPivoting: require("./app/static/js/gaussian_partial_pivoting"),
    gaussianTotalPivoting: require("./app/static/js/gaussian_total_pivoting"),
    gaussTridiagonal: require("./app/static/js/gauss_tridiagonal"),
};

const shared = require("./app/static/js/numerical_methods_shared");

const academicExpressions = {
    f: "ln(sin^2(x) + 1) - 0.5",
    g: "ln(sin^2(x) + 1) - 0.5",
    h: "e^x - x - 1",
};

const baseMatrix = [
    [2, -1, 0, 3],
    [1, 0.5, 3, 8],
    [0, 13, -2, 11],
    [14, 5, -2, 3],
];

const baseVector = [1, 1, 1, 1];

const tridiagonalExample = {
    A: [
        [2, -1, 0, 0],
        [-1, 2, -1, 0],
        [0, -1, 2, -1],
        [0, 0, -1, 2],
    ],
    b: [1, 0, 0, 1],
};

function summarize(result) {
    return {
        method: result.method,
        root: result.root ?? null,
        solution: result.solution ?? null,
        iterations: result.iterations,
    };
}

function runCase(fn) {
    try {
        return {
            status: "ok",
            ...summarize(fn()),
        };
    } catch (error) {
        return {
            status: "error",
            message: error.message,
        };
    }
}

function runAllTests() {
    return {
        source_notation: academicExpressions,
        normalized_examples: {
            f: shared.normalizeExpression(academicExpressions.f),
            h: shared.normalizeExpression(academicExpressions.h),
        },
        root_methods: {
            incremental_search: runCase(() => methods.incrementalSearch(academicExpressions.f, {
                x0: -3,
                h: 0.5,
                max_iter: 100,
            })),
            bisection: runCase(() => methods.bisection(academicExpressions.f, {
                a: 0,
                b: 1,
                tol: 1e-7,
                max_iter: 100,
            })),
            false_position: runCase(() => methods.falsePosition(academicExpressions.f, {
                a: 0,
                b: 1,
                tol: 1e-7,
                max_iter: 100,
            })),
            trisection: runCase(() => methods.trisection(academicExpressions.f, {
                a: 0,
                b: 1,
                tol: 1e-7,
                max_iter: 100,
            })),
            newton: runCase(() => methods.newton(academicExpressions.f, {
                x0: 0.5,
                tol: 1e-7,
                max_iter: 100,
            })),
            punto_fijo: runCase(() => methods.puntoFijo(academicExpressions.g, {
                x0: -0.5,
                tol: 1e-7,
                max_iter: 100,
            })),
            secante: runCase(() => methods.secante(academicExpressions.f, {
                x0: 0.5,
                x1: 1.0,
                tol: 1e-7,
                max_iter: 100,
            })),
            raices_multiples: runCase(() => methods.raicesMultiples(academicExpressions.h, {
                x0: 1.0,
                tol: 1e-7,
                max_iter: 100,
            })),
        },
        system_methods: {
            gaussian_simple: runCase(() => methods.gaussianSimple(baseMatrix, baseVector)),
            gaussian_partial_pivoting: runCase(() => methods.gaussianPartialPivoting(baseMatrix, baseVector)),
            gaussian_total_pivoting: runCase(() => methods.gaussianTotalPivoting(baseMatrix, baseVector)),
            gauss_tridiagonal_with_prueba_matrix: runCase(() => methods.gaussTridiagonal(baseMatrix, baseVector)),
            gauss_tridiagonal_valid_example: runCase(() => methods.gaussTridiagonal(
                tridiagonalExample.A,
                tridiagonalExample.b,
            )),
        },
    };
}

if (require.main === module) {
    console.log(JSON.stringify(runAllTests(), null, 2));
}

module.exports = {
    runAllTests,
};
