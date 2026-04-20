"""
Método de Müller — Encuentra raíces interpolando una parábola por 3 puntos.
Puede encontrar raíces complejas, aunque aquí limitaremos a reales por UI.
"""
from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function
import math


class Muller(NumericalMethod):

    @property
    def name(self) -> str:
        return "muller"

    @property
    def description(self) -> str:
        return "Müller"

    @property
    def method_type(self) -> str:
        return "root"

    @property
    def params_schema(self) -> list:
        return [
            {"key": "x0", "label_es": "x₀", "label_en": "x₀", "type": "float", "default": 0.0},
            {"key": "x1", "label_es": "x₁", "label_en": "x₁", "type": "float", "default": 0.5},
            {"key": "x2", "label_es": "x₂", "label_en": "x₂", "type": "float", "default": 1.0},
            {"key": "tol", "label_es": "Tolerancia", "label_en": "Tolerance", "type": "float", "default": 1e-7},
            {"key": "max_iter", "label_es": "Máx. iteraciones", "label_en": "Max iterations", "type": "int", "default": 100},
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese <code>f(x)</code> y tres aproximaciones iniciales <code>x₀, x₁, x₂</code>.</li>"
                "<li>Interpola un polinomio cuadrático y saca la raíz más cercana a x₂.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter <code>f(x)</code> and three initial approximations <code>x₀, x₁, x₂</code>.</li>"
                "<li>Interpolates a quadratic polynomial and finds the root closest to x₂.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:
        f = make_function(expr)
        x0 = float(params.get("x0", 0.0))
        x1 = float(params.get("x1", 0.5))
        x2 = float(params.get("x2", 1.0))
        tol = float(params.get("tol", 1e-7))
        N = int(params.get("max_iter", 100))
        steps = []

        for i in range(1, N + 1):
            f0 = f(x0)
            f1 = f(x1)
            f2 = f(x2)
            
            h1 = x1 - x0
            h2 = x2 - x1
            
            if h1 == 0 or h2 == 0 or (h1 + h2) == 0:
                raise ValueError("Puntos coincidentes, no se puede construir la parábola.")

            d1 = (f1 - f0) / h1
            d2 = (f2 - f1) / h2
            d = (d2 - d1) / (h2 + h1)
            
            b = d2 + h2 * d
            
            # Raíz del discriminante
            disc = b**2 - 4 * f2 * d
            if disc < 0:
                # Müller puede generar raíces complejas.
                raise ValueError("El discriminante es negativo; el método de Müller generaría una raíz compleja "
                                 "(nuestra interfaz actual se centra en reales). ¡Intente otros puntos iniciales!")
            
            sqrt_disc = math.sqrt(disc)
            
            # Denominador de mayor magnitud
            if abs(b + sqrt_disc) > abs(b - sqrt_disc):
                E = b + sqrt_disc
            else:
                E = b - sqrt_disc
                
            if E == 0:
                raise ValueError("El denominador es cero.")
            
            h = -2 * f2 / E
            x3 = x2 + h
            
            err = abs(x3 - x2)

            steps.append({
                "step": i, "phase": "muller",
                "x_new": x3, "error": err,
                "description": f"Iter {i}: x_new={x3:.6f}, E={err:.6e}"
            })

            if err < tol:
                steps[-1]["phase"] = "converged"
                break
                
            # Desplazar variables
            x0 = x1
            x1 = x2
            x2 = x3

        return {
            "solution": [x3],
            "root": x3,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }
