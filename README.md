# Numerical Methods Calculator

Web application to solve linear systems, interpolate data with Lagrange polynomials, and find roots of scalar equations—with a step-by-step trace for each algorithm.

## Architecture — modular monolith

```
app/
├── __init__.py          ← Application factory (create_app)
├── config.py            ← Environment configuration
├── routes.py            ← Blueprint: HTML views + REST API
├── core/
│   ├── base_method.py   ← NumericalMethod ABC
│   └── method_registry.py ← Autodiscovery via pkgutil
├── methods/             ← One module per method (auto-discovered)
├── static/              ← CSS + JS (served by Flask)
└── templates/           ← Jinja2 (base, index, solver, …)
```

**Convention:** add a new numerical method by dropping **one** file under `app/methods/` that subclasses `NumericalMethod`. Restart the app to register it.

## Implemented methods

| Category | Method | Module | Notes |
|----------|--------|--------|--------|
| Linear systems | Gaussian elimination (no pivoting) | `gaussian_simple.py` | Fails on zero pivots |
| | Partial pivoting | `gaussian_pivoting.py` | Column pivot |
| | Total pivoting | `gaussian_pivoting.py` | Row + column permutations |
| | Tridiagonal (Thomas) | `gauss_tridiagonal.py` | O(n) |
| Interpolation | Lagrange | `lagrange.py` | Evaluate P(x) at a point |
| Root finding | Bisection, Regula Falsi, incremental search, fixed-point, Newton, secant, multiple roots, trisection | `bisection.py`, … | Expression parser + parameters |

Pseudocode drafts live under `docs/pseudocodes/` (including `lagrange.txt`).

## Quick start

### Local development

```bash
pip install -r requirements.txt
python run.py
```

→ http://localhost:5000

### Docker

```bash
docker compose up --build
```

→ http://localhost:5000

## REST API

### `GET /api/methods`

Lists registered methods (name, description, `method_type`, `params_schema`).

### `POST /api/solve`

Payload depends on `method_type`:

**Linear system** (`matrix`, `b`):

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"method":"gaussian_simple","matrix":[[2,1,-1],[-3,-1,2],[-2,1,2]],"b":[8,-11,-3]}'
```

**Root finding** (`expr`, `params`):

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"method":"newton","expr":"x**2 - 2","params":{"x0":1.5,"tol":1e-7,"max_iter":100}}'
```

**Lagrange interpolation** (`points`, `x_eval`):

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"method":"lagrange","points":[[0,1],[1,2],[2,5]],"x_eval":1.5}'
```

### `GET /api/health`

Returns `{"status":"ok"}`.

## Adding a new method

1. Create `app/methods/my_method.py`.
2. Implement a `NumericalMethod` subclass with `name`, `description`, `instructions`, `method_type`, and `solve(...)`.
3. Restart the app — the method appears in the sidebar and in `/api/methods`.

```python
from app.core.base_method import NumericalMethod

class MyMethod(NumericalMethod):
    @property
    def name(self): return "my_method"

    @property
    def description(self): return "My method"

    def solve(self, A, b):
        return {"solution": [...], "steps": [...], "method": self.name}
```
