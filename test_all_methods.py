"""
Comprehensive test for ALL 26 numerical methods registered in the app.
Calls each method's solve() directly with appropriate test data.
"""
import sys
import traceback

# Create the Flask app so the registry is populated
from app import create_app
from app.core.method_registry import registry

app = create_app("dev")

# ──────────────────────────────────────────────────────────────────────────────
# Test data definitions per method
# ──────────────────────────────────────────────────────────────────────────────

# Root-finding methods: solve(expr, params)
ROOT_TESTS = {
    "incremental_search": {
        "expr": "x**2 - 2",
        "params": {"x0": -3, "h": 0.5, "max_iter": 100},
    },
    "bisection": {
        "expr": "x**2 - 2",
        "params": {"a": 0, "b": 2, "tol": 1e-7, "max_iter": 100},
    },
    "trisection": {
        "expr": "x**2 - 2",
        "params": {"a": 0, "b": 2, "tol": 1e-7, "max_iter": 100},
    },
    "false_position": {
        "expr": "x**2 - 2",
        "params": {"a": 0, "b": 2, "tol": 1e-7, "max_iter": 100},
    },
    "newton": {
        "expr": "x**2 - 2",
        "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100},
    },
    "punto_fijo": {
        "expr": "(x + 2/x)/2",   # g(x) for x^2 - 2 = 0
        "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100},
    },
    "secante": {
        "expr": "x**2 - 2",
        "params": {"x0": 0.5, "x1": 1.5, "tol": 1e-7, "max_iter": 100},
    },
    "raices_multiples": {
        "expr": "x**2 - 2",
        "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100},
    },
    "steffensen": {
        "expr": "x**2 - 2",
        "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100},
    },
    "aitken": {
        "expr": "(x + 2/x)/2",   # g(x) iteration function
        "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100},
    },
    "muller": {
        "expr": "x**2 - 2",
        "params": {"x0": 0.0, "x1": 1.0, "x2": 2.0, "tol": 1e-7, "max_iter": 100},
    },
    "simpson38": {
        "expr": "x**2",
        "params": {"a": 0, "b": 1, "n": 3},
    },
}

# Direct linear system methods: solve(A, b) — no params
DIRECT_LINEAR_TESTS = {
    "gaussian_simple": {
        "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
        "b": [8, -11, -3],
    },
    "gaussian_partial_pivoting": {
        "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
        "b": [8, -11, -3],
    },
    "gaussian_total_pivoting": {
        "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
        "b": [8, -11, -3],
    },
    "gauss_tridiagonal": {
        "A": [[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 2]],
        "b": [1, 0, 0, 1],
    },
    "crout": {
        "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
        "b": [8, -11, -3],
    },
    "doolittle": {
        "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
        "b": [8, -11, -3],
    },
    "cholesky": {
        "A": [[4, 2], [2, 3]],
        "b": [1, 2],
    },
    "matrix_analysis": {
        "A": [[4, 1, 0], [1, 3, 1], [0, 1, 4]],
        "b": [7, 11, 13],
    },
}

# Iterative linear system methods: solve(A, b, params=...)
ITERATIVE_LINEAR_TESTS = {
    "jacobi": {
        "A": [[4, 1, 0], [1, 3, 1], [0, 1, 4]],
        "b": [7, 11, 13],
        "params": {"tol": 1e-7, "max_iter": 100, "x0": "0,0,0"},
    },
    "gauss_seidel": {
        "A": [[4, 1, 0], [1, 3, 1], [0, 1, 4]],
        "b": [7, 11, 13],
        "params": {"tol": 1e-7, "max_iter": 100, "x0": "0,0,0"},
    },
    "sor": {
        "A": [[4, 1, 0], [1, 3, 1], [0, 1, 4]],
        "b": [7, 11, 13],
        "params": {"w": 1.25, "tol": 1e-7, "max_iter": 100, "x0": "0,0,0"},
    },
}

# Interpolation: points-based (solve(points, x_eval=...))
INTERPOLATION_POINTS_TESTS = {
    "lagrange": {
        "points": [[0, 1], [1, 2], [2, 5]],
        "x_eval": 1.5,
    },
    "newton_interpolation": {
        "points": [[0, 1], [1, 2], [2, 5]],
        "x_eval": 1.5,
    },
}

# Interpolation: x/y based (solve(x_points, y_points, params=...))
INTERPOLATION_XY_TESTS = {
    "vandermonde": {
        "x_points": [0, 1, 2],
        "y_points": [1, 2, 5],
        "params": {"eval_x": 1.5},
    },
}


# ──────────────────────────────────────────────────────────────────────────────
# Run tests
# ──────────────────────────────────────────────────────────────────────────────

results = []  # list of (name, method_type, status, detail)

def run_test(name, method_type_label, call_fn):
    """Execute a test and record the result."""
    try:
        result = call_fn()
        # Basic validation
        if not isinstance(result, dict):
            results.append((name, method_type_label, "FAIL", f"Expected dict, got {type(result).__name__}"))
            return
        if "steps" not in result:
            results.append((name, method_type_label, "FAIL", "Missing 'steps' key in result"))
            return
        if "method" not in result:
            results.append((name, method_type_label, "FAIL", "Missing 'method' key in result"))
            return

        sol = result.get("solution") or result.get("root")
        n_steps = len(result.get("steps", []))
        results.append((name, method_type_label, "PASS", f"solution={sol}, steps={n_steps}"))
    except Exception as e:
        tb = traceback.format_exc()
        results.append((name, method_type_label, "FAIL", f"{type(e).__name__}: {e}\n{tb}"))


with app.app_context():
    # Discover all methods
    all_methods = registry.list_all()
    registered_names = {m["name"] for m in all_methods}

    print(f"{'='*70}")
    print(f"  Registered methods: {len(all_methods)}")
    print(f"{'='*70}")
    for m in sorted(all_methods, key=lambda x: (x["method_type"], x["name"])):
        print(f"  [{m['method_type']:15}] {m['name']}")
    print(f"{'='*70}\n")

    # ── Root methods ──────────────────────────────────────────────────────────
    for name, test_data in ROOT_TESTS.items():
        if name not in registered_names:
            results.append((name, "root", "SKIP", "Not registered"))
            continue
        method = registry.get(name)
        run_test(name, "root", lambda m=method, d=test_data: m.solve(d["expr"], d["params"]))

    # ── Direct linear system methods ──────────────────────────────────────────
    for name, test_data in DIRECT_LINEAR_TESTS.items():
        if name not in registered_names:
            results.append((name, "linear_system", "SKIP", "Not registered"))
            continue
        method = registry.get(name)
        run_test(name, "linear_system", lambda m=method, d=test_data: m.solve(d["A"], d["b"]))

    # ── Iterative linear system methods ───────────────────────────────────────
    for name, test_data in ITERATIVE_LINEAR_TESTS.items():
        if name not in registered_names:
            results.append((name, "linear_system", "SKIP", "Not registered"))
            continue
        method = registry.get(name)
        run_test(name, "linear_system (iterative)", lambda m=method, d=test_data: m.solve(d["A"], d["b"], params=d["params"]))

    # ── Interpolation (points-based) ──────────────────────────────────────────
    for name, test_data in INTERPOLATION_POINTS_TESTS.items():
        if name not in registered_names:
            results.append((name, "interpolation", "SKIP", "Not registered"))
            continue
        method = registry.get(name)
        run_test(name, "interpolation", lambda m=method, d=test_data: m.solve(d["points"], x_eval=d["x_eval"]))

    # ── Interpolation (x/y-based — Vandermonde) ───────────────────────────────
    for name, test_data in INTERPOLATION_XY_TESTS.items():
        if name not in registered_names:
            results.append((name, "interpolation", "SKIP", "Not registered"))
            continue
        method = registry.get(name)
        run_test(name, "interpolation", lambda m=method, d=test_data: m.solve(d["x_points"], d["y_points"], params=d["params"]))

    # ── Check for any registered methods that we didn't test ──────────────────
    tested_names = set(ROOT_TESTS) | set(DIRECT_LINEAR_TESTS) | set(ITERATIVE_LINEAR_TESTS) | set(INTERPOLATION_POINTS_TESTS) | set(INTERPOLATION_XY_TESTS)
    untested = registered_names - tested_names
    for name in sorted(untested):
        results.append((name, "???", "UNTESTED", "No test data defined for this method"))


# ──────────────────────────────────────────────────────────────────────────────
# Print summary
# ──────────────────────────────────────────────────────────────────────────────

print(f"\n{'='*70}")
print(f"  TEST RESULTS")
print(f"{'='*70}")

passed = [r for r in results if r[2] == "PASS"]
failed = [r for r in results if r[2] == "FAIL"]
skipped = [r for r in results if r[2] in ("SKIP", "UNTESTED")]

for name, mtype, status, detail in results:
    icon = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️", "UNTESTED": "⚠️"}.get(status, "?")
    print(f"  {icon} [{mtype:25}] {name:30} {status}")
    if status == "FAIL":
        # Print first 5 lines of error detail
        for line in detail.split("\n")[:5]:
            print(f"      {line}")

print(f"\n{'='*70}")
print(f"  SUMMARY: {len(passed)} PASSED | {len(failed)} FAILED | {len(skipped)} SKIPPED/UNTESTED | {len(results)} TOTAL")
print(f"{'='*70}")

if failed:
    print("\n  ❌ FAILED METHODS:")
    for name, mtype, status, detail in failed:
        print(f"    - {name} ({mtype})")
        for line in detail.split("\n")[:3]:
            print(f"        {line}")
    sys.exit(1)
else:
    print("\n  🎉 All tested methods passed!")
    sys.exit(0)
