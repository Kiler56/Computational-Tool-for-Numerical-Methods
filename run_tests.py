import requests
import json

URL = "http://localhost:5000/api/solve"

def solve(method, expr=None, params=None, matrix=None, b_=None):
    payload = {"method": method}
    if expr:
        payload["expr"] = expr
        payload["params"] = params
    if matrix:
        payload["matrix"] = matrix
        payload["b"] = b_
    
    resp = requests.post(URL, json=payload)
    if resp.status_code != 200:
        print(f"Error in {method}: {resp.text}")
        return None
    return resp.json()

def main():
    f = "log(sin(x)**2 + 1) - 0.5"
    h = "exp(x) - x - 1"
    
    A = [
        [2, -1, 0, 3],
        [1, 0.5, 3, 8],
        [0, 13, -2, 11],
        [14, 5, -2, 3]
    ]
    b = [1, 1, 1, 1]

    tests = [
        ("incremental_search", f, {"x0": -3, "step": 0.5, "max_iter": 100}),
        ("bisection", f, {"a": 0, "b": 1, "tol": 1e-7, "max_iter": 100}),
        ("trisection", f, {"a": 0, "b": 1, "tol": 1e-7, "max_iter": 100}),
        ("false_position", f, {"a": 0, "b": 1, "tol": 1e-7, "max_iter": 100}),
        ("newton", f, {"x0": 0.5, "tol": 1e-7, "max_iter": 100}),
        ("punto_fijo", f, {"x0": -0.5, "tol": 1e-7, "max_iter": 100}),
        ("secante", f, {"x0": 0.5, "x1": 1.0, "tol": 1e-7, "max_iter": 100}),
        ("raices_multiples", h, {"x0": 1.0, "tol": 1e-7, "max_iter": 100}),
        ("steffensen", f, {"x0": 0.5, "tol": 1e-7, "max_iter": 100}),
        ("aitken", f, {"x0": -0.5, "tol": 1e-7, "max_iter": 100}),
        ("muller", f, {"x0": 0.0, "x1": 0.5, "x2": 1.0, "tol": 1e-7, "max_iter": 100}),
    ]

    for meth, expr, params in tests:
        print(f"--- {meth.upper()} ---")
        res = solve(meth, expr=expr, params=params)
        if res:
            root = res.get('root') or res.get('solution')
            print(f"Root: {root}")
            print(f"Iters: {res.get('iterations')}")
            # Print last step if available
            if res.get('steps'):
                print("Last step:", res['steps'][-1])
        print()
        
    # Tridiagonal testing matrix
    A_tri = [
        [2, -1, 0, 0],
        [-1, 2, -1, 0],
        [0, -1, 2, -1],
        [0, 0, -1, 2]
    ]
    b_tri = [1, 0, 0, 1]

    print("--- GAUSS_TRIDIAGONAL ---")
    res = solve("gauss_tridiagonal", matrix=A_tri, b_=b_tri)
    if res:
        print(f"Solution: {res.get('solution')}")
        print(f"Total Steps: {len(res.get('steps', []))}")
        if res.get('steps'):
            print("Last step:", res['steps'][-1])
    print()

    for meth in ["gaussian_simple", "gaussian_pivoting", "gaussian_total_pivoting"]:
        print(f"--- {meth.upper()} ---")
        res = solve(meth, matrix=A, b_=b)
        if res:
            print(f"Solution: {res.get('solution')}")
            print(f"Total Steps: {len(res.get('steps', []))}")
            if res.get('steps'):
                print("Last step:", res['steps'][-1])
        print()

if __name__ == "__main__":
    main()
