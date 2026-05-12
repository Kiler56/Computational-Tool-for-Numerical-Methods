from app.core.base_method import NumericalMethod
from app.core.safe_eval import make_function


class Simpson13Compuesto(NumericalMethod):

    @property
    def name(self) -> str:
        return "simpson_13_compuesto"

    @property
    def description(self) -> str:
        return "Integración numérica por Simpson 1/3 compuesto"

    @property
    def method_type(self) -> str:
        return "integration"

    @property
    def params_schema(self) -> list:
        return [
            {
                "key": "a",
                "label_es": "Límite inferior (a)",
                "label_en": "Lower limit (a)",
                "type": "float",
                "default": 0,
            },
            {
                "key": "b",
                "label_es": "Límite superior (b)",
                "label_en": "Upper limit (b)",
                "type": "float",
                "default": 1,
            },
            {
                "key": "n",
                "label_es": "Número de subintervalos (par)",
                "label_en": "Number of subintervals (even)",
                "type": "int",
                "default": 4,
            },
        ]

    @property
    def instructions(self) -> dict:
        return {
            "es": (
                "<ul>"
                "<li>Ingrese una función continua <code>f(x)</code>.</li>"
                "<li>El método aproxima la integral definida usando parábolas sobre subintervalos.</li>"
                "<li>El número de subintervalos <code>n</code> debe ser par.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Enter a continuous function <code>f(x)</code>.</li>"
                "<li>The method approximates the definite integral using parabolas over subintervals.</li>"
                "<li>The number of subintervals <code>n</code> must be even.</li>"
                "</ul>"
            ),
        }

    def solve(self, expr: str, params: dict) -> dict:

        f = make_function(expr)

        a = float(params.get("a", 0))
        b = float(params.get("b", 1))
        n = int(params.get("n", 4))

        if n % 2 != 0:
            raise ValueError(
                "El número de subintervalos n debe ser par."
            )

        h = (b - a) / n

        suma_impares = 0
        suma_pares = 0

        steps = []

        # Evaluaciones internas
        for i in range(1, n):

            x_i = a + i * h
            fx_i = f(x_i)

            if i % 2 == 0:
                suma_pares += fx_i
                coef = 2
                phase = "even"
            else:
                suma_impares += fx_i
                coef = 4
                phase = "odd"

            steps.append({
                "step": i,
                "phase": phase,
                "x": x_i,
                "fx": fx_i,
                "coefficient": coef,
                "description": (
                    f"i={i}, x={x_i:.6f}, "
                    f"f(x)={fx_i:.6f}, coef={coef}"
                )
            })

        fa = f(a)
        fb = f(b)

        integral = (
            h / 3
        ) * (
            fa
            + fb
            + 4 * suma_impares
            + 2 * suma_pares
        )

        steps.append({
            "step": n,
            "phase": "result",
            "h": h,
            "fa": fa,
            "fb": fb,
            "sum_odd": suma_impares,
            "sum_even": suma_pares,
            "integral": integral,
            "description": (
                f"Integral ≈ {integral:.10f}"
            )
        })

        return {
            "solution": [integral],
            "integral": integral,
            "steps": steps,
            "iterations": len(steps),
            "method": self.name,
        }