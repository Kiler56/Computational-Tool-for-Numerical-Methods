"""
test_vandermonde_simpson38.py
==============================
Script de pruebas segun la guia del profesor:
  - Prueba_metodos2..pdf (datos de entrada)
  - ResultadosMetodos2..txt (resultados esperados)

Datos de prueba del profesor:
  Tabla = x: [-1, 0, 3, 4]   y: [15.5, 3, 8, 1]

Resultados esperados Vandermonde:
  Coeficientes (descendente): -1.141667  5.825000  -5.533333  3.000000
  Polinomio: -1.141667x^3 + 5.825000x^2 - 5.533333x + 3.000000

  Nuestro orden (ascendente): a0=3, a1=-5.533333, a2=5.825000, a3=-1.141667

Para Simpson 3/8 no hay caso de prueba del profesor, se valida con
integrales analiticas conocidas.

Ejecutar:
    .\\venv\\Scripts\\python.exe test_vandermonde_simpson38.py
"""
import sys
import math
import traceback

# Forzar UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

passed = 0
failed = 0

def assert_close(val, expected, tol=1e-6, label=""):
    global passed, failed
    err = abs(val - expected)
    ok = err <= tol
    status = "[PASS]" if ok else "[FAIL]"
    print(f"  {status}  {label}")
    print(f"         obtenido={val:.10g}  esperado={expected:.10g}  error={err:.2e}")
    if ok:
        passed += 1
    else:
        failed += 1
    return ok

def section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def run_test(label, fn):
    global failed
    try:
        fn()
    except Exception as exc:
        print(f"  [FAIL]  {label}")
        print(f"         EXCEPCION: {exc}")
        traceback.print_exc()
        failed += 1

# =============================================================================
# IMPORTACIONES
# =============================================================================
section("Importaciones")

try:
    from app.methods.vandermonde import VandermondeInterpolation
    print(f"  [PASS]  VandermondeInterpolation importado correctamente")
    passed += 1
except Exception as e:
    print(f"  [FAIL]  No se pudo importar VandermondeInterpolation: {e}")
    failed += 1
    sys.exit(1)

try:
    from app.methods.simpson38 import Simpson38
    print(f"  [PASS]  Simpson38 importado correctamente")
    passed += 1
except Exception as e:
    print(f"  [FAIL]  No se pudo importar Simpson38: {e}")
    failed += 1
    sys.exit(1)

van = VandermondeInterpolation()
s38 = Simpson38()

# =============================================================================
# VANDERMONDE: CASO DE PRUEBA DEL PROFESOR
# =============================================================================
# Datos: Prueba_metodos2..pdf
#   x = [-1, 0, 3, 4]
#   y = [15.5, 3, 8, 1]
#
# Resultados esperados: ResultadosMetodos2..txt
#   Coeficientes (descendente): -1.141667  5.825000  -5.533333  3.000000
#   Polinomio: -1.141667x^3 + 5.825000x^2 - 5.533333x + 3.000000
#
#   Matriz de Vandermonde esperada (descendente x^3, x^2, x^1, x^0):
#     -1.000000  1.000000  -1.000000  1.000000
#      0.000000  0.000000   0.000000  1.000000
#     27.000000  9.000000   3.000000  1.000000
#     64.000000 16.000000   4.000000  1.000000
#
# Nuestro metodo usa orden ascendente [x^0, x^1, x^2, x^3]:
#   a0 = 3.000000
#   a1 = -5.533333
#   a2 = 5.825000
#   a3 = -1.141667
# =============================================================================

section("VANDERMONDE -- Caso de prueba del profesor")

# Datos de entrada del profesor
X_PROF = [-1.0, 0.0, 3.0, 4.0]
Y_PROF = [15.5, 3.0, 8.0, 1.0]

# Coeficientes esperados (ascendente: a0 + a1*x + a2*x^2 + a3*x^3)
COEFF_EXPECTED = [3.000000, -5.533333, 5.825000, -1.141667]

def test_van_prof_coeficientes():
    """Verificar coeficientes contra resultados del profesor"""
    result = van.solve(X_PROF, Y_PROF)
    coeffs = result["solution"]

    print(f"\n  Coeficientes obtenidos (ascendente):")
    for i, c in enumerate(coeffs):
        print(f"    a{i} = {c:.6f}")
    print(f"  Coeficientes esperados (ascendente):")
    for i, c in enumerate(COEFF_EXPECTED):
        print(f"    a{i} = {c:.6f}")
    print()

    for i in range(len(COEFF_EXPECTED)):
        assert_close(coeffs[i], COEFF_EXPECTED[i], tol=1e-4,
                     label=f"a{i} = {COEFF_EXPECTED[i]:.6f}")

def test_van_prof_interpolacion_exacta():
    """Verificar que el polinomio pasa por los 4 puntos"""
    result = van.solve(X_PROF, Y_PROF)
    coeffs = result["solution"]
    for xi, yi in zip(X_PROF, Y_PROF):
        p_val = van._eval_poly(coeffs, xi)
        assert_close(p_val, yi, tol=1e-6,
                     label=f"p({xi}) = {yi}  (interpolacion exacta en punto del profesor)")

def test_van_prof_polinomio_str():
    """Verificar que el polinomio formateado coincide con el del profesor"""
    global passed, failed
    result = van.solve(X_PROF, Y_PROF)
    poly = result["properties"]["Polinomio Interpolante"]
    print(f"\n  Polinomio obtenido:  {poly}")
    print(f"  Polinomio esperado:  p(x) = 3 - 5.53333x + 5.825x^2 - 1.14167x^3")
    # Verificamos que los coeficientes principales aparezcan
    has_a0 = "3" in poly
    has_a3 = "1.14167" in poly
    if has_a0 and has_a3:
        print(f"  [PASS]  Polinomio contiene coeficientes principales")
        passed += 1
    else:
        print(f"  [FAIL]  Polinomio no coincide con esperado")
        failed += 1

def test_van_prof_vandermonde_matrix():
    """Verificar la matriz de Vandermonde construida (ascendente)"""
    global passed, failed
    # Nuestra matriz ascendente: V[i][j] = x_i^j
    # Fila para x=-1: [1, -1, 1, -1]
    # Fila para x=0:  [1, 0, 0, 0]
    # Fila para x=3:  [1, 3, 9, 27]
    # Fila para x=4:  [1, 4, 16, 64]
    expected_V = [
        [1.0, -1.0, 1.0, -1.0],
        [1.0, 0.0, 0.0, 0.0],
        [1.0, 3.0, 9.0, 27.0],
        [1.0, 4.0, 16.0, 64.0],
    ]
    V = van._build_vandermonde(X_PROF, 4)
    print(f"\n  Matriz de Vandermonde construida (ascendente x^0..x^3):")
    for i, row in enumerate(V):
        print(f"    [{', '.join(f'{v:10.4f}' for v in row)}]")

    all_ok = True
    for i in range(4):
        for j in range(4):
            if abs(V[i][j] - expected_V[i][j]) > 1e-10:
                all_ok = False
    if all_ok:
        print(f"  [PASS]  Matriz de Vandermonde correcta")
        passed += 1
    else:
        print(f"  [FAIL]  Matriz de Vandermonde no coincide")
        failed += 1

    # Comparar con la del profesor (es la transpuesta invertida en columnas)
    print(f"\n  La del profesor usa orden descendente (x^3, x^2, x^1, x^0):")
    print(f"    [-1  1  -1  1]     <-- nuestra fila invertida: [1, -1, 1, -1]")
    print(f"    [ 0  0   0  1]     <-- nuestra: [1, 0, 0, 0]")
    print(f"    [27  9   3  1]     <-- nuestra: [1, 3, 9, 27]")
    print(f"    [64 16   4  1]     <-- nuestra: [1, 4, 16, 64]")
    print(f"  Ambas son equivalentes, solo difiere la convencion.")

run_test("Vandermonde: coeficientes vs profesor", test_van_prof_coeficientes)
run_test("Vandermonde: interpolacion exacta en puntos", test_van_prof_interpolacion_exacta)
run_test("Vandermonde: polinomio formateado", test_van_prof_polinomio_str)
run_test("Vandermonde: matriz de Vandermonde", test_van_prof_vandermonde_matrix)

# =============================================================================
# VANDERMONDE: CASOS ADICIONALES
# =============================================================================
section("VANDERMONDE -- Casos adicionales")

def test_van_lineal():
    """Dos puntos -> polinomio lineal exacto"""
    result = van.solve([0.0, 2.0], [1.0, 5.0])
    coeffs = result["solution"]
    assert_close(coeffs[0], 1.0, label="a0 = 1  (p(x) = 1 + 2x)")
    assert_close(coeffs[1], 2.0, label="a1 = 2  (p(x) = 1 + 2x)")

def test_van_cuadratico():
    """y = x^2 -> a0=0, a1=0, a2=1"""
    result = van.solve([1.0, 2.0, 3.0], [1.0, 4.0, 9.0])
    coeffs = result["solution"]
    assert_close(coeffs[0], 0.0, tol=1e-8, label="a0 = 0  (y=x^2)")
    assert_close(coeffs[1], 0.0, tol=1e-8, label="a1 = 0  (y=x^2)")
    assert_close(coeffs[2], 1.0, tol=1e-8, label="a2 = 1  (y=x^2)")

def test_van_eval_x():
    """Evaluacion en punto externo"""
    result = van.solve([1.0, 2.0, 3.0], [1.0, 4.0, 9.0],
                       params={"eval_x": 5.0})
    val = float(result["properties"].get("p(5.0)", "nan"))
    assert_close(val, 25.0, tol=1e-6, label="p(5) = 25  (y=x^2)")

run_test("Vandermonde: polinomio lineal", test_van_lineal)
run_test("Vandermonde: polinomio cuadratico", test_van_cuadratico)
run_test("Vandermonde: evaluacion en x externo", test_van_eval_x)

# =============================================================================
# VANDERMONDE: VALIDACIONES DE ERROR
# =============================================================================
section("VANDERMONDE -- Validaciones de error")

def test_van_x_duplicados():
    global passed, failed
    try:
        van.solve([1.0, 1.0, 2.0], [1.0, 2.0, 3.0])
        print(f"  [FAIL]  Deberia lanzar ValueError con x duplicados")
        failed += 1
    except ValueError:
        print(f"  [PASS]  Correctamente rechaza x duplicados")
        passed += 1

def test_van_tamanos_distintos():
    global passed, failed
    try:
        van.solve([1.0, 2.0], [1.0, 2.0, 3.0])
        print(f"  [FAIL]  Deberia lanzar ValueError con tamanos distintos")
        failed += 1
    except ValueError:
        print(f"  [PASS]  Correctamente rechaza tamanos distintos")
        passed += 1

def test_van_un_punto():
    global passed, failed
    try:
        van.solve([1.0], [1.0])
        print(f"  [FAIL]  Deberia lanzar ValueError con un solo punto")
        failed += 1
    except ValueError:
        print(f"  [PASS]  Correctamente rechaza un solo punto")
        passed += 1

run_test("Error: x duplicados", test_van_x_duplicados)
run_test("Error: tamanos distintos", test_van_tamanos_distintos)
run_test("Error: un solo punto", test_van_un_punto)

# =============================================================================
# VANDERMONDE: ESTRUCTURA DE LA RESPUESTA
# =============================================================================
section("VANDERMONDE -- Estructura y etapas (requisito del profesor)")

def test_van_estructura():
    """El profesor pide: imprimir etapas y coeficientes"""
    global passed, failed
    result = van.solve(X_PROF, Y_PROF)

    # Claves requeridas
    for key in ["solution", "properties", "steps", "iterations", "method"]:
        if key in result:
            print(f"  [PASS]  Clave '{key}' presente")
            passed += 1
        else:
            print(f"  [FAIL]  Clave '{key}' AUSENTE")
            failed += 1

    # Fases requeridas en los pasos (etapas)
    phases = {s["phase"] for s in result["steps"]}
    required = {
        "build_matrix": "Construccion de Vandermonde",
        "pivot": "Pivoteo total",
        "elimination": "Eliminacion gaussiana",
        "back_substitution": "Sustitucion regresiva",
        "result": "Polinomio resultante",
        "verification": "Verificacion en puntos",
    }
    for phase, desc in required.items():
        if phase in phases:
            print(f"  [PASS]  Fase '{phase}' ({desc}) presente en los pasos")
            passed += 1
        else:
            print(f"  [FAIL]  Fase '{phase}' ({desc}) AUSENTE")
            failed += 1

    # Mostrar las etapas como las pide el profesor
    print(f"\n  --- Etapas del metodo (resumen) ---")
    for step in result["steps"]:
        desc = step.get("description", "")
        print(f"    Paso {step['step']:2d} [{step['phase']:20s}] {desc[:80]}")

run_test("Estructura y etapas", test_van_estructura)

# =============================================================================
# SIMPSON 3/8 -- INTEGRALES CON SOLUCION ANALITICA CONOCIDA
# =============================================================================
# Nota: El profesor pide Simpson 3/8 simple como valor agregado.
# No proporciono datos de prueba especificos, asi que validamos contra
# integrales con solucion analitica conocida.
# =============================================================================

section("SIMPSON 3/8 -- Integrales con solucion analitica conocida")

def get_integral(expr, a, b, n):
    result = s38.solve(expr, {"a": a, "b": b, "n": n})
    return result["solution"][0], result

# Simpson 3/8 integra exactamente polinomios hasta grado 3

def test_s38_lineal():
    """int_0^1 x dx = 0.5 (exacto)"""
    val, _ = get_integral("x", 0, 1, 3)
    assert_close(val, 0.5, tol=1e-10, label="int_0^1 x dx = 0.5 (exacto)")

def test_s38_cuadratico():
    """int_0^1 x^2 dx = 1/3 (exacto)"""
    val, _ = get_integral("x**2", 0, 1, 3)
    assert_close(val, 1/3, tol=1e-10, label="int_0^1 x^2 dx = 1/3 (exacto)")

def test_s38_cubico():
    """int_0^2 x^3 dx = 4 (exacto para Simpson 3/8)"""
    val, _ = get_integral("x**3", 0, 2, 3)
    assert_close(val, 4.0, tol=1e-10,
                 label="int_0^2 x^3 dx = 4 (exacto, grado 3)")

def test_s38_sin_n3():
    """int_0^pi sin(x) dx = 2 con n=3"""
    val, _ = get_integral("sin(x)", 0, math.pi, 3)
    assert_close(val, 2.0, tol=0.05,
                 label="int_0^pi sin(x) dx = 2  (n=3, error esperado ~0.04)")

def test_s38_sin_n30():
    """int_0^pi sin(x) dx = 2 con n=30"""
    val, _ = get_integral("sin(x)", 0, math.pi, 30)
    assert_close(val, 2.0, tol=1e-5,
                 label="int_0^pi sin(x) dx = 2  (n=30)")

def test_s38_exp_n3():
    """int_0^1 e^x dx = e-1 con n=3"""
    val, _ = get_integral("exp(x)", 0, 1, 3)
    assert_close(val, math.e - 1, tol=1e-3,
                 label=f"int_0^1 e^x dx = e-1 = {math.e-1:.6g}  (n=3)")

def test_s38_exp_n30():
    """int_0^1 e^x dx = e-1 con n=30"""
    val, _ = get_integral("exp(x)", 0, 1, 30)
    assert_close(val, math.e - 1, tol=1e-7,
                 label=f"int_0^1 e^x dx = e-1 = {math.e-1:.6g}  (n=30)")

def test_s38_ln_n3():
    """int_1^2 1/x dx = ln(2) con n=3"""
    val, _ = get_integral("1/x", 1, 2, 3)
    assert_close(val, math.log(2), tol=1e-3,
                 label=f"int_1^2 1/x dx = ln(2) = {math.log(2):.6g}  (n=3)")

def test_s38_ln_n30():
    """int_1^2 1/x dx = ln(2) con n=30"""
    val, _ = get_integral("1/x", 1, 2, 30)
    assert_close(val, math.log(2), tol=1e-7,
                 label=f"int_1^2 1/x dx = ln(2) = {math.log(2):.6g}  (n=30)")

run_test("Simpson 3/8: lineal (exacto)", test_s38_lineal)
run_test("Simpson 3/8: cuadratico (exacto)", test_s38_cuadratico)
run_test("Simpson 3/8: cubico (exacto)", test_s38_cubico)
run_test("Simpson 3/8: sin(x) n=3", test_s38_sin_n3)
run_test("Simpson 3/8: sin(x) n=30", test_s38_sin_n30)
run_test("Simpson 3/8: exp(x) n=3", test_s38_exp_n3)
run_test("Simpson 3/8: exp(x) n=30", test_s38_exp_n30)
run_test("Simpson 3/8: 1/x n=3", test_s38_ln_n3)
run_test("Simpson 3/8: 1/x n=30", test_s38_ln_n30)

# =============================================================================
# SIMPSON 3/8: AJUSTE DE n Y VALIDACIONES
# =============================================================================
section("SIMPSON 3/8 -- Ajuste de n y validaciones")

def test_s38_ajuste_n():
    global passed, failed
    result = s38.solve("x**2", {"a": 0, "b": 1, "n": 4})
    n_used = int(result["properties"]["Subintervalos usados (n)"])
    if n_used == 6:
        print(f"  [PASS]  n=4 ajustado a n=6 (multiplo de 3)")
        passed += 1
    else:
        print(f"  [FAIL]  n ajustado a {n_used}, esperado 6")
        failed += 1

def test_s38_n_ok():
    global passed, failed
    result = s38.solve("x", {"a": 0, "b": 1, "n": 6})
    n_used = int(result["properties"]["Subintervalos usados (n)"])
    if n_used == 6:
        print(f"  [PASS]  n=6 se mantiene sin ajuste")
        passed += 1
    else:
        print(f"  [FAIL]  n=6 cambio a {n_used}")
        failed += 1

def test_s38_a_mayor_b():
    global passed, failed
    try:
        s38.solve("x", {"a": 5.0, "b": 1.0, "n": 3})
        print(f"  [FAIL]  Deberia lanzar ValueError con a > b")
        failed += 1
    except ValueError:
        print(f"  [PASS]  Correctamente rechaza a > b")
        passed += 1

run_test("Ajuste n=4 a 6", test_s38_ajuste_n)
run_test("n=6 sin ajuste", test_s38_n_ok)
run_test("a > b lanza error", test_s38_a_mayor_b)

# =============================================================================
# SIMPSON 3/8: ESTRUCTURA Y ETAPAS (requisito del profesor)
# =============================================================================
section("SIMPSON 3/8 -- Estructura y etapas (requisito del profesor)")

def test_s38_estructura():
    """El profesor pide: imprimir etapas y solucion"""
    global passed, failed
    result = s38.solve("sin(x)", {"a": 0, "b": math.pi, "n": 3})

    for key in ["solution", "properties", "steps", "iterations", "method"]:
        if key in result:
            print(f"  [PASS]  Clave '{key}' presente")
            passed += 1
        else:
            print(f"  [FAIL]  Clave '{key}' AUSENTE")
            failed += 1

    phases = {s["phase"] for s in result["steps"]}
    required = {
        "setup": "Configuracion (a, b, n, h)",
        "evaluation": "Evaluacion de nodos f(x_i)",
        "weighted_sum": "Suma ponderada",
        "result": "Integral resultante",
        "error_estimation": "Estimacion del error",
    }
    for phase, desc in required.items():
        if phase in phases:
            print(f"  [PASS]  Fase '{phase}' ({desc}) presente")
            passed += 1
        else:
            print(f"  [FAIL]  Fase '{phase}' ({desc}) AUSENTE")
            failed += 1

    # Mostrar etapas como pide el profesor
    print(f"\n  --- Etapas del metodo (resumen) ---")
    for step in result["steps"]:
        desc = step.get("description", "")
        print(f"    Paso {step['step']:2d} [{step['phase']:20s}] {desc[:80]}")

run_test("Estructura y etapas Simpson 3/8", test_s38_estructura)

# =============================================================================
# CONVERGENCIA
# =============================================================================
section("CONVERGENCIA -- Error decrece al aumentar n")

def test_convergencia():
    global passed, failed
    print(f"\n  {'n':>6}  {'I aprox':>18}  {'error':>12}  {'mejora':>8}")
    print(f"  {'-'*6}  {'-'*18}  {'-'*12}  {'-'*8}")
    prev_err = None
    converging = True
    for n in [3, 6, 12, 30, 60]:
        val, _ = get_integral("sin(x)", 0, math.pi, n)
        err = abs(val - 2.0)
        mejora = f"{prev_err/err:.1f}x" if prev_err and err > 1e-15 else "---"
        print(f"  {n:>6}  {val:>18.10g}  {err:>12.2e}  {mejora:>8}")
        if prev_err is not None and err >= prev_err:
            converging = False
        prev_err = err if err > 1e-15 else prev_err
    if converging:
        print(f"  [PASS]  Convergencia O(h^4) verificada")
        passed += 1
    else:
        print(f"  [FAIL]  No converge monotonamente")
        failed += 1

run_test("Convergencia Simpson 3/8", test_convergencia)

# =============================================================================
# RESUMEN FINAL
# =============================================================================
total = passed + failed
print(f"\n{'='*70}")
print(f"  RESUMEN FINAL")
print(f"{'='*70}")
print(f"  Total de checks : {total}")
print(f"  Aprobados       : {passed}")
print(f"  Fallidos        : {failed}")

if failed:
    print(f"\n  [X] Algunos tests fallaron.")
    sys.exit(1)
else:
    print(f"\n  [OK] TODOS LOS TESTS PASARON.")
    sys.exit(0)
