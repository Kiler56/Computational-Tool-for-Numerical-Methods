"""
Script de prueba rapida para composite_trapezoidal y verificacion global.
Evita emojis para compatibilidad con el encoding cp1252 de Windows.
"""
import sys
import traceback

from app import create_app
from app.core.method_registry import registry

app = create_app("dev")

ROOT_TESTS = {
    "incremental_search": {"expr": "x**2 - 2", "params": {"x0": -3, "h": 0.5, "max_iter": 100}},
    "bisection": {"expr": "x**2 - 2", "params": {"a": 0, "b": 2, "tol": 1e-7, "max_iter": 100}},
    "trisection": {"expr": "x**2 - 2", "params": {"a": 0, "b": 2, "tol": 1e-7, "max_iter": 100}},
    "false_position": {"expr": "x**2 - 2", "params": {"a": 0, "b": 2, "tol": 1e-7, "max_iter": 100}},
    "newton": {"expr": "x**2 - 2", "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100}},
    "punto_fijo": {"expr": "(x + 2/x)/2", "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100}},
    "secante": {"expr": "x**2 - 2", "params": {"x0": 0.5, "x1": 1.5, "tol": 1e-7, "max_iter": 100}},
    "raices_multiples": {"expr": "x**2 - 2", "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100}},
    "steffensen": {"expr": "x**2 - 2", "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100}},
    "aitken": {"expr": "(x + 2/x)/2", "params": {"x0": 1.5, "tol": 1e-7, "max_iter": 100}},
    "muller": {"expr": "x**2 - 2", "params": {"x0": 0.0, "x1": 1.0, "x2": 2.0, "tol": 1e-7, "max_iter": 100}},
    "simpson38": {"expr": "x**2", "params": {"a": 0, "b": 1, "n": 3}},
    "composite_trapezoidal": {"expr": "x**2", "params": {"a": 0, "b": 1, "n": 4}},
}

DIRECT_LINEAR_TESTS = {
    "gaussian_simple": {"A": [[2,1,-1],[-3,-1,2],[-2,1,2]], "b": [8,-11,-3]},
    "gaussian_partial_pivoting": {"A": [[2,1,-1],[-3,-1,2],[-2,1,2]], "b": [8,-11,-3]},
    "gaussian_total_pivoting": {"A": [[2,1,-1],[-3,-1,2],[-2,1,2]], "b": [8,-11,-3]},
    "gauss_tridiagonal": {"A": [[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]], "b": [1,0,0,1]},
    "crout": {"A": [[2,1,-1],[-3,-1,2],[-2,1,2]], "b": [8,-11,-3]},
    "doolittle": {"A": [[2,1,-1],[-3,-1,2],[-2,1,2]], "b": [8,-11,-3]},
    "cholesky": {"A": [[4,2],[2,3]], "b": [1,2]},
    "matrix_analysis": {"A": [[4,1,0],[1,3,1],[0,1,4]], "b": [7,11,13]},
}

ITERATIVE_LINEAR_TESTS = {
    "jacobi": {"A": [[4,1,0],[1,3,1],[0,1,4]], "b": [7,11,13], "params": {"tol": 1e-7, "max_iter": 100, "x0": "0,0,0"}},
    "gauss_seidel": {"A": [[4,1,0],[1,3,1],[0,1,4]], "b": [7,11,13], "params": {"tol": 1e-7, "max_iter": 100, "x0": "0,0,0"}},
    "sor": {"A": [[4,1,0],[1,3,1],[0,1,4]], "b": [7,11,13], "params": {"w": 1.25, "tol": 1e-7, "max_iter": 100, "x0": "0,0,0"}},
}

INTERPOLATION_POINTS_TESTS = {
    "lagrange": {"points": [[0,1],[1,2],[2,5]], "x_eval": 1.5},
    "newton_interpolation": {"points": [[0,1],[1,2],[2,5]], "x_eval": 1.5},
    "vandermonde": {"points": [[0,1],[1,2],[2,5]], "x_eval": 1.5},
}


results = []

def run(name, call_fn):
    try:
        r = call_fn()
        assert isinstance(r, dict), "Expected dict"
        assert "steps" in r, "Missing 'steps'"
        assert "method" in r, "Missing 'method'"
        sol = r.get("solution") or r.get("root")
        results.append((name, "PASS", "steps=%d sol=%s" % (len(r.get("steps", [])), str(sol)[:40])))
    except Exception as e:
        results.append((name, "FAIL", str(e)[:120]))

with app.app_context():
    all_methods = registry.list_all()
    reg_names = {m["name"] for m in all_methods}

    for name, d in ROOT_TESTS.items():
        m = registry.get(name)
        run(name, lambda m=m, d=d: m.solve(d["expr"], d["params"]))

    for name, d in DIRECT_LINEAR_TESTS.items():
        m = registry.get(name)
        run(name, lambda m=m, d=d: m.solve(d["A"], d["b"]))

    for name, d in ITERATIVE_LINEAR_TESTS.items():
        m = registry.get(name)
        run(name, lambda m=m, d=d: m.solve(d["A"], d["b"], params=d["params"]))

    for name, d in INTERPOLATION_POINTS_TESTS.items():
        m = registry.get(name)
        run(name, lambda m=m, d=d: m.solve(d["points"], x_eval=d["x_eval"]))


passed = [r for r in results if r[1] == "PASS"]
failed = [r for r in results if r[1] == "FAIL"]

print("=" * 70)
print("  RESULTADOS DE TESTS")
print("=" * 70)
for name, status, detail in results:
    icon = "[PASS]" if status == "PASS" else "[FAIL]"
    print("  %s  %-35s  %s" % (icon, name, detail))

print("=" * 70)
print("  RESUMEN: %d PASSED | %d FAILED | %d TOTAL" % (len(passed), len(failed), len(results)))
print("=" * 70)

if failed:
    print("\n  METODOS CON FALLO:")
    for name, _, detail in failed:
        print("    - %s: %s" % (name, detail))
    sys.exit(1)
else:
    print("\n  Todos los metodos pasaron correctamente.")
    sys.exit(0)
