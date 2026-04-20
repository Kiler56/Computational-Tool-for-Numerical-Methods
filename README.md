# Numerical Methods Calculator

Web-based computational tool to solve and analyze linear systems of equations and root-finding algorithms using different numerical methods. It visualizes each intermediate step of the solution and provides a dynamic, user-friendly interface.

## Architecture — Modular Monolith

```
app/
├── __init__.py          ← Application Factory (create_app)
├── config.py            ← Environment configuration
├── routes.py            ← Blueprint: HTML views + REST API
├── core/
│   ├── base_method.py   ← ABC NumericalMethod (schema defined here)
│   └── method_registry.py ← Autodiscovery via pkgutil
├── methods/             ← Each file = an autodiscovered method
├── static/              ← CSS + JS (served by Flask + i18n + JS ports)
└── templates/           ← Jinja2 (base, index, solver)
```

**Key Principle:** To add a new method, simply create ONE file in `app/methods/`. No other files need to be modified.

## Implemented Methods

| Category | Method | File | Description |
|----------|--------|------|-------------|
| **Roots** | Bisection | `bisection.py` | Brackets a root by halving intervals |
| **Roots** | False Position | `false_position.py` | Uses linear interpolation |
| **Roots** | Incremental | `incremental_search.py` | Evaluates function at regular steps |
| **Roots** | Trisection | `trisection.py` | Value-added: splits interval in three |
| **Roots** | Newton | `newton.py` | Numerical derivative optimization |
| **Roots** | Secant | `secante.py` | Two-point approximation |
| **Roots** | Fixed Point | `punto_fijo.py` | Functional iteration (x = g(x)) |
| **Roots** | Multiple Roots | `raices_multiples.py` | Handles multiplicy > 1 |
| **Roots** | Steffensen | `steffensen.py` | Value-added: Newton-like |
| **Roots** | Aitken | `aitken.py` | Value-added: Convergence acceleration |
| **Roots** | Müller | `muller.py` | Value-added: Quadratic interpolation |
| **Systems** | Gauss Simple | `gaussian_simple.py` | Direct forward elimination |
| **Systems** | Partial Pivoting| `gaussian_pivoting.py` | Column max swapping |
| **Systems** | Total Pivoting | `gaussian_pivoting.py` | Matrix max swapping |
| **Systems** | Tridiagonal | `gauss_tridiagonal.py` | Value-added: Thomas algorithm |

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
python run.py
```

→ App available at http://localhost:5000

### Docker (Production)

```bash
docker compose up --build
```

→ App available at http://localhost:5000

## REST API

### `GET /api/methods`

Lists all available auto-discovered methods.

```bash
curl http://localhost:5000/api/methods
```

### `POST /api/solve`

Resolves a numerical problem (either a matrix system or an algebraic equation).

```bash
# Example System
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "method": "gaussian_simple",
    "matrix": [[2,1,-1],[-3,-1,2],[-2,1,2]],
    "b": [8,-11,-3]
  }'

# Example Root Finding
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "method": "newton",
    "expr": "exp(x) - 2",
    "params": {"x0": 1.0, "tol": 1e-7, "max_iter": 100}
  }'
```

### `GET /api/health`

```bash
curl http://localhost:5000/api/health
```

## Adding a New Method

1. Create `app/methods/my_method.py`
2. Implement a class inheriting from `NumericalMethod`:

```python
from app.core.base_method import NumericalMethod

class MyMethod(NumericalMethod):
    @property
    def name(self): return "my_method"

    @property
    def description(self): return "My Custom Method"

    @property
    def method_type(self): return "root" # or "linear_system"

    # ... schema and instructions properties ...

    def solve(self, expr, params):
        # ... logic ...
        return {"solution": [...], "steps": [...], "method": self.name}
```

3. Restart the app → the method automatically appears in the UI and API.

## About Value Additions (Entrega 1)
This project successfully integrates all requested functionality and value additions:
- **English Support**: Full GUI translations via i18n and fully translated documentation.
- **Extra Methods**: Steffensen, Aitken, Müller, Trisection, and Tridiagonal.
- **Second Language**: Full implementation of methods in Javascript (`methods_js_port.js`).
