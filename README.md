# Calculadora de Métodos Numéricos

Herramienta computacional web para resolver y analizar sistemas de ecuaciones lineales usando diferentes métodos numéricos. Visualiza cada paso intermedio de la solución.

## Arquitectura — Monolito Modular

```
app/
├── __init__.py          ← Application Factory (create_app)
├── config.py            ← Configuración por entorno
├── routes.py            ← Blueprint: vistas HTML + API REST
├── core/
│   ├── base_method.py   ← ABC NumericalMethod
│   └── method_registry.py ← Autodiscovery via pkgutil
├── methods/             ← Cada archivo = un método autodescubierto
├── static/              ← CSS + JS (servidos por Flask)
└── templates/           ← Jinja2 (base, index, solver)
```

**Principio clave:** agregar un nuevo método = crear UN archivo en `app/methods/`. Sin tocar nada más.

## Métodos Implementados

| Método | Archivo | Descripción |
|--------|---------|-------------|
| Eliminación Gaussiana Simple | `gaussian_simple.py` | Sin pivoteo, eliminación directa |
| Pivoteo Parcial | `gaussian_pivoting.py` | Máximo en columna |
| Pivoteo Total | `gaussian_pivoting.py` | Máximo en submatriz + permutación de columnas |
| Gauss Tridiagonal | `gauss_tridiagonal.py` | Algoritmo de Thomas (TDMA) — O(n) |

## Inicio Rápido

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en modo desarrollo
python run.py
```

→ App disponible en http://localhost:5000

### Docker (Producción)

```bash
docker compose up --build
```

→ App disponible en http://localhost:5000

## API REST

### `GET /api/methods`

Lista los métodos disponibles.

```bash
curl http://localhost:5000/api/methods
```

### `POST /api/solve`

Resuelve un sistema Ax = b.

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "method": "gaussian_simple",
    "matrix": [[2,1,-1],[-3,-1,2],[-2,1,2]],
    "b": [8,-11,-3]
  }'
```

### `GET /api/health`

```bash
curl http://localhost:5000/api/health
# {"status": "ok"}
```

## Agregar un Nuevo Método

1. Crear `app/methods/mi_metodo.py`
2. Implementar clase que herede de `NumericalMethod`:

```python
from app.core.base_method import NumericalMethod

class MiMetodo(NumericalMethod):
    @property
    def name(self): return "mi_metodo"

    @property
    def description(self): return "Mi Método Custom"

    def solve(self, A, b):
        # ... lógica ...
        return {"solution": [...], "steps": [...], "method": self.name}
```

3. Reiniciar la app → el método aparece automáticamente en la UI y la API.
