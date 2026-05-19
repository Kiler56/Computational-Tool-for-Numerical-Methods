# Euler and Heun Methods — Results Table

**Author branch:** `carlos-ochoa`  
**Methods:** `euler`, `heun` (`app/methods/`)

## Test problem

| Item | Value |
|------|-------|
| ODE | y' = f(t, y) = y − t² + 1 |
| Initial condition | y(0) = 0.5 |
| Interval | t ∈ [0, 1] |
| Step size | h = 0.25 |
| Exact solution | y(t) = (t + 1)² − ½·e^t |

## Approximate vs exact solution

### Euler's method (`euler`)

| Step n | t | y (numerical) | y (exact) | Absolute error \|y − y_exact\| |
|--------|---|---------------|-----------|--------------------------------|
| 0 | 0.00 | 0.50000000 | 0.50000000 | 0.000000e+00 |
| 1 | 0.25 | 0.87500000 | 0.92048729 | 4.548729e-02 |
| 2 | 0.50 | 1.32812500 | 1.42563936 | 9.751436e-02 |
| 3 | 0.75 | 1.84765625 | 2.00399999 | 1.563437e-01 |
| 4 | 1.00 | 2.41894531 | 2.64085909 | **2.219138e-01** |

**Global error at t = 1:** 2.22×10⁻¹ (first order, O(h)).

---

### Heun's method (`heun`)

| Step n | t | y (numerical) | y (exact) | Absolute error \|y − y_exact\| |
|--------|---|---------------|-----------|--------------------------------|
| 0 | 0.00 | 0.50000000 | 0.50000000 | 0.000000e+00 |
| 1 | 0.25 | 0.91406250 | 0.92048729 | 6.424792e-03 |
| 2 | 0.50 | 1.41137695 | 1.42563936 | 1.426241e-02 |
| 3 | 0.75 | 1.98020172 | 2.00399999 | 2.379827e-02 |
| 4 | 1.00 | 2.60549283 | 2.64085909 | **3.536626e-02** |

**Global error at t = 1:** 3.54×10⁻² (second order, O(h²)).

---

## Comparison summary (t = 1)

| Method | y(1) approximate | y(1) exact | Global error |
|--------|------------------|------------|----------------|
| Euler | 2.41894531 | 2.64085909 | 2.22×10⁻¹ |
| Heun | 2.60549283 | 2.64085909 | 3.54×10⁻² |

With the same step size h = 0.25, **Heun is about 6× more accurate** than Euler on this problem.

## API example

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "method": "euler",
    "expr": "y - t**2 + 1",
    "params": {"t0": 0, "y0": 0.5, "tf": 1, "h": 0.25}
  }'
```

Replace `"method": "euler"` with `"heun"` for Heun's method.
