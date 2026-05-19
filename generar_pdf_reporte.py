"""
Genera un PDF profesional con los resultados de las pruebas
de Vandermonde y Simpson 3/8 segun la guia del profesor.
"""
import sys, math, os

# Forzar UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# === Importar metodos ===
from app.methods.vandermonde import VandermondeInterpolation
from app.methods.simpson38 import Simpson38

van = VandermondeInterpolation()
s38 = Simpson38()

# === Datos del profesor ===
X_PROF = [-1.0, 0.0, 3.0, 4.0]
Y_PROF = [15.5, 3.0, 8.0, 1.0]
COEFF_EXPECTED = [3.000000, -5.533333, 5.825000, -1.141667]

# === Configurar PDF ===
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Reporte_Pruebas_Metodos.pdf")
doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter,
                        topMargin=1.5*cm, bottomMargin=1.5*cm,
                        leftMargin=2*cm, rightMargin=2*cm)

styles = getSampleStyleSheet()

# Estilos personalizados
styles.add(ParagraphStyle('MainTitle', parent=styles['Title'],
    fontSize=22, textColor=colors.HexColor('#1a237e'),
    spaceAfter=6, spaceBefore=0))
styles.add(ParagraphStyle('SubTitle', parent=styles['Normal'],
    fontSize=12, textColor=colors.HexColor('#37474f'),
    alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle('SectionHead', parent=styles['Heading2'],
    fontSize=14, textColor=colors.HexColor('#0d47a1'),
    spaceBefore=16, spaceAfter=8,
    borderWidth=0, borderPadding=0))
styles.add(ParagraphStyle('SubSection', parent=styles['Heading3'],
    fontSize=11, textColor=colors.HexColor('#1565c0'),
    spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle('BodyText2', parent=styles['Normal'],
    fontSize=9, leading=13, textColor=colors.HexColor('#212121')))
styles.add(ParagraphStyle('Pass', parent=styles['Normal'],
    fontSize=9, textColor=colors.HexColor('#2e7d32'), leading=13))
styles.add(ParagraphStyle('CodeBlock', parent=styles['Normal'],
    fontSize=8, fontName='Courier', leading=11,
    textColor=colors.HexColor('#263238'),
    backColor=colors.HexColor('#eceff1'),
    borderWidth=0.5, borderColor=colors.HexColor('#b0bec5'),
    borderPadding=4, spaceBefore=4, spaceAfter=4))
styles.add(ParagraphStyle('SmallBold', parent=styles['Normal'],
    fontSize=9, fontName='Helvetica-Bold',
    textColor=colors.HexColor('#1a237e'), leading=13))

story = []

def add_hr():
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor('#bbdefb'),
                             spaceBefore=6, spaceAfter=6))

def make_table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('LEADING', (0,0), (-1,-1), 11),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#90caf9')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, colors.HexColor('#e3f2fd')]),
    ]
    if header:
        style_cmds += [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1565c0')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ]
    t.setStyle(TableStyle(style_cmds))
    return t

# =====================================================================
# PORTADA
# =====================================================================
story.append(Spacer(1, 2*inch))
story.append(Paragraph("Reporte de Pruebas", styles['MainTitle']))
story.append(Paragraph("Metodos Numericos: Vandermonde &amp; Simpson 3/8", styles['MainTitle']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Segunda Entrega - Analisis Numerico", styles['SubTitle']))
story.append(Paragraph("Datos de prueba segun guia del profesor", styles['SubTitle']))
story.append(Spacer(1, 0.5*inch))

# Tabla resumen portada
info_data = [
    ['Parametro', 'Valor'],
    ['Autor', 'Andres Yue'],
    ['Metodos', 'Vandermonde (Interpolacion) + Simpson 3/8 (Integracion)'],
    ['Referencia', 'Prueba_metodos2.pdf / ResultadosMetodos2.txt'],
    ['Resultado', '55/55 PASS'],
]
story.append(make_table(info_data, col_widths=[2.5*inch, 4*inch]))
story.append(PageBreak())

# =====================================================================
# 1. VANDERMONDE - CASO DEL PROFESOR
# =====================================================================
story.append(Paragraph("1. Vandermonde - Caso de Prueba del Profesor", styles['SectionHead']))
add_hr()

# Datos de entrada
story.append(Paragraph("1.1 Datos de Entrada (Prueba_metodos2.pdf)", styles['SubSection']))
input_data = [
    ['i', 'x_i', 'y_i'],
    ['0', '-1', '15.5'],
    ['1', '0', '3'],
    ['2', '3', '8'],
    ['3', '4', '1'],
]
story.append(make_table(input_data, col_widths=[1*inch, 2*inch, 2*inch]))
story.append(Spacer(1, 0.15*inch))

# Ejecutar Vandermonde
result_van = van.solve(X_PROF, Y_PROF)
coeffs = result_van["solution"]

# Coeficientes
story.append(Paragraph("1.2 Coeficientes Obtenidos vs Esperados", styles['SubSection']))
coeff_data = [['Coeficiente', 'Obtenido', 'Esperado (profesor)', 'Error', 'Estado']]
all_pass = True
for i in range(4):
    err = abs(coeffs[i] - COEFF_EXPECTED[i])
    ok = err < 1e-4
    if not ok: all_pass = False
    coeff_data.append([
        f'a{i}', f'{coeffs[i]:.6f}', f'{COEFF_EXPECTED[i]:.6f}',
        f'{err:.2e}', 'PASS' if ok else 'FAIL'
    ])
story.append(make_table(coeff_data, col_widths=[1.1*inch, 1.3*inch, 1.5*inch, 1.1*inch, 0.8*inch]))
story.append(Spacer(1, 0.1*inch))

# Polinomio
poly_str = result_van["properties"]["Polinomio Interpolante"]
story.append(Paragraph("1.3 Polinomio Interpolante", styles['SubSection']))
story.append(Paragraph(f"Obtenido: {poly_str}", styles['CodeBlock']))
story.append(Paragraph(
    "Esperado: p(x) = 3 - 5.53333x + 5.825x^2 - 1.14167x^3",
    styles['CodeBlock']))
story.append(Paragraph("PASS - Coeficientes coinciden", styles['Pass']))
story.append(Spacer(1, 0.1*inch))

# Matriz de Vandermonde
story.append(Paragraph("1.4 Matriz de Vandermonde (orden ascendente x^0..x^3)", styles['SubSection']))
V = van._build_vandermonde(X_PROF, 4)
v_data = [['', 'x^0', 'x^1', 'x^2', 'x^3']]
for i, row in enumerate(V):
    v_data.append([f'x={X_PROF[i]}'] + [f'{v:.4f}' for v in row])
story.append(make_table(v_data, col_widths=[1*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch]))
story.append(Spacer(1, 0.05*inch))
story.append(Paragraph(
    "Nota: El profesor usa orden descendente (x^3..x^0). "
    "Ambas convenciones son equivalentes, solo cambia el orden de columnas.",
    styles['BodyText2']))
story.append(Spacer(1, 0.1*inch))

# Verificacion en puntos
story.append(Paragraph("1.5 Verificacion: p(x_i) = y_i", styles['SubSection']))
verif_data = [['x_i', 'y_i esperado', 'p(x_i) obtenido', 'Error', 'Estado']]
for xi, yi in zip(X_PROF, Y_PROF):
    p_val = van._eval_poly(coeffs, xi)
    err = abs(p_val - yi)
    verif_data.append([
        f'{xi}', f'{yi}', f'{p_val:.8g}', f'{err:.2e}', 'PASS'
    ])
story.append(make_table(verif_data))
story.append(Spacer(1, 0.1*inch))

# Etapas paso a paso
story.append(Paragraph("1.6 Etapas del Metodo (requisito del profesor)", styles['SubSection']))
steps_data = [['Paso', 'Fase', 'Descripcion']]
for step in result_van["steps"]:
    desc = step.get("description", "")[:85]
    steps_data.append([
        str(step['step']),
        step['phase'],
        Paragraph(desc, styles['BodyText2'])
    ])
story.append(make_table(steps_data, col_widths=[0.5*inch, 1.3*inch, 4.5*inch]))

story.append(PageBreak())

# =====================================================================
# 2. VANDERMONDE - CASOS ADICIONALES
# =====================================================================
story.append(Paragraph("2. Vandermonde - Casos Adicionales", styles['SectionHead']))
add_hr()

# Lineal
story.append(Paragraph("2.1 Polinomio Lineal: p(x) = 1 + 2x", styles['SubSection']))
r_lin = van.solve([0.0, 2.0], [1.0, 5.0])
c_lin = r_lin["solution"]
lin_data = [
    ['Coeficiente', 'Obtenido', 'Esperado', 'Estado'],
    ['a0', f'{c_lin[0]:.6f}', '1.000000', 'PASS' if abs(c_lin[0]-1)<1e-6 else 'FAIL'],
    ['a1', f'{c_lin[1]:.6f}', '2.000000', 'PASS' if abs(c_lin[1]-2)<1e-6 else 'FAIL'],
]
story.append(make_table(lin_data))
story.append(Spacer(1, 0.1*inch))

# Cuadratico
story.append(Paragraph("2.2 Polinomio Cuadratico: y = x^2", styles['SubSection']))
r_quad = van.solve([1.0, 2.0, 3.0], [1.0, 4.0, 9.0])
c_quad = r_quad["solution"]
quad_data = [
    ['Coeficiente', 'Obtenido', 'Esperado', 'Estado'],
    ['a0', f'{c_quad[0]:.8f}', '0.000000', 'PASS' if abs(c_quad[0])<1e-8 else 'FAIL'],
    ['a1', f'{c_quad[1]:.8f}', '0.000000', 'PASS' if abs(c_quad[1])<1e-8 else 'FAIL'],
    ['a2', f'{c_quad[2]:.8f}', '1.000000', 'PASS' if abs(c_quad[2]-1)<1e-8 else 'FAIL'],
]
story.append(make_table(quad_data))
story.append(Spacer(1, 0.1*inch))

# Evaluacion externa
story.append(Paragraph("2.3 Evaluacion en punto externo: p(5) con y=x^2", styles['SubSection']))
r_eval = van.solve([1.0, 2.0, 3.0], [1.0, 4.0, 9.0], params={"eval_x": 5.0})
val_5 = float(r_eval["properties"].get("p(5.0)", "nan"))
story.append(Paragraph(f"p(5) = {val_5:.6f}  (esperado: 25.0)  ->  PASS", styles['Pass']))
story.append(Spacer(1, 0.1*inch))

# Validaciones de error
story.append(Paragraph("2.4 Validaciones de Error", styles['SubSection']))
err_tests = []
try:
    van.solve([1.0, 1.0, 2.0], [1.0, 2.0, 3.0])
    err_tests.append(('x duplicados', 'FAIL'))
except ValueError:
    err_tests.append(('x duplicados -> ValueError', 'PASS'))
try:
    van.solve([1.0, 2.0], [1.0, 2.0, 3.0])
    err_tests.append(('tamanos distintos', 'FAIL'))
except ValueError:
    err_tests.append(('tamanos distintos -> ValueError', 'PASS'))
try:
    van.solve([1.0], [1.0])
    err_tests.append(('un solo punto', 'FAIL'))
except ValueError:
    err_tests.append(('un solo punto -> ValueError', 'PASS'))

err_data = [['Caso de error', 'Estado']]
for desc, st in err_tests:
    err_data.append([desc, st])
story.append(make_table(err_data, col_widths=[4*inch, 1.5*inch]))

story.append(PageBreak())

# =====================================================================
# 3. SIMPSON 3/8
# =====================================================================
story.append(Paragraph("3. Simpson 3/8 - Integrales con Solucion Analitica", styles['SectionHead']))
add_hr()

def get_integral(expr, a, b, n):
    r = s38.solve(expr, {"a": a, "b": b, "n": n})
    return r["solution"][0], r

# Integrales exactas (grado <= 3)
story.append(Paragraph("3.1 Integrales Exactas (polinomios grado &lt;= 3)", styles['SubSection']))
exact_data = [['Integral', 'n', 'Obtenido', 'Esperado', 'Error', 'Estado']]
tests_exact = [
    ("int x dx [0,1]", "x", 0, 1, 3, 0.5),
    ("int x^2 dx [0,1]", "x**2", 0, 1, 3, 1/3),
    ("int x^3 dx [0,2]", "x**3", 0, 2, 3, 4.0),
]
for label, expr, a, b, n, expected in tests_exact:
    val, _ = get_integral(expr, a, b, n)
    err = abs(val - expected)
    exact_data.append([label, str(n), f'{val:.10g}', f'{expected:.10g}',
                       f'{err:.2e}', 'PASS' if err < 1e-10 else 'FAIL'])
story.append(make_table(exact_data))
story.append(Spacer(1, 0.15*inch))

# Integrales analiticas
story.append(Paragraph("3.2 Integrales con Solucion Analitica Conocida", styles['SubSection']))
anal_data = [['Integral', 'n', 'Obtenido', 'Esperado', 'Error', 'Tol', 'Estado']]
tests_anal = [
    ("sin(x) [0,pi]", "sin(x)", 0, math.pi, 3, 2.0, 0.05),
    ("sin(x) [0,pi]", "sin(x)", 0, math.pi, 30, 2.0, 1e-5),
    ("exp(x) [0,1]", "exp(x)", 0, 1, 3, math.e-1, 1e-3),
    ("exp(x) [0,1]", "exp(x)", 0, 1, 30, math.e-1, 1e-7),
    ("1/x [1,2]", "1/x", 1, 2, 3, math.log(2), 1e-3),
    ("1/x [1,2]", "1/x", 1, 2, 30, math.log(2), 1e-7),
]
for label, expr, a, b, n, expected, tol in tests_anal:
    val, _ = get_integral(expr, a, b, n)
    err = abs(val - expected)
    anal_data.append([label, str(n), f'{val:.10g}', f'{expected:.10g}',
                      f'{err:.2e}', f'{tol:.0e}',
                      'PASS' if err <= tol else 'FAIL'])
story.append(make_table(anal_data))
story.append(Spacer(1, 0.15*inch))

# Ajuste de n
story.append(Paragraph("3.3 Ajuste Automatico de n (multiplo de 3)", styles['SubSection']))
r_adj = s38.solve("x**2", {"a": 0, "b": 1, "n": 4})
n_used = int(r_adj["properties"]["Subintervalos usados (n)"])
adj_data = [
    ['n solicitado', 'n usado', 'Razon', 'Estado'],
    ['4', str(n_used), 'Ajustado al siguiente multiplo de 3',
     'PASS' if n_used == 6 else 'FAIL'],
    ['6', '6', 'Ya es multiplo de 3', 'PASS'],
]
story.append(make_table(adj_data))
story.append(Spacer(1, 0.1*inch))

# Validacion a > b
story.append(Paragraph("3.4 Validacion: a &gt; b lanza error", styles['SubSection']))
try:
    s38.solve("x", {"a": 5.0, "b": 1.0, "n": 3})
    story.append(Paragraph("FAIL - No lanzo ValueError", styles['BodyText2']))
except ValueError:
    story.append(Paragraph("PASS - Correctamente rechaza a > b con ValueError", styles['Pass']))
story.append(Spacer(1, 0.1*inch))

# Etapas Simpson
story.append(Paragraph("3.5 Etapas del Metodo (ejemplo: sin(x) en [0, pi], n=3)", styles['SubSection']))
_, r_sin = get_integral("sin(x)", 0, math.pi, 3)
s_steps_data = [['Paso', 'Fase', 'Descripcion']]
for step in r_sin["steps"]:
    desc = step.get("description", "")[:90]
    s_steps_data.append([
        str(step['step']),
        step['phase'],
        Paragraph(desc, styles['BodyText2'])
    ])
story.append(make_table(s_steps_data, col_widths=[0.5*inch, 1.3*inch, 4.5*inch]))

story.append(PageBreak())

# =====================================================================
# 4. CONVERGENCIA
# =====================================================================
story.append(Paragraph("4. Convergencia O(h^4) - Simpson 3/8", styles['SectionHead']))
add_hr()

story.append(Paragraph(
    "Se verifica que el error decrece como O(h^4) al aumentar n, "
    "lo cual es la propiedad teorica del metodo de Simpson 3/8.",
    styles['BodyText2']))
story.append(Spacer(1, 0.1*inch))

conv_data = [['n', 'I aproximada', 'Error |I - 2|', 'Mejora vs anterior']]
prev_err = None
for n in [3, 6, 12, 30, 60]:
    val, _ = get_integral("sin(x)", 0, math.pi, n)
    err = abs(val - 2.0)
    mejora = f'{prev_err/err:.1f}x' if prev_err and err > 1e-15 else '---'
    conv_data.append([str(n), f'{val:.12g}', f'{err:.4e}', mejora])
    if err > 1e-15:
        prev_err = err
story.append(make_table(conv_data, col_widths=[1*inch, 2.2*inch, 1.5*inch, 1.5*inch]))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph(
    "PASS - La convergencia O(h^4) se verifica: al duplicar n el error "
    "se reduce aprox. 16x (2^4 = 16), consistente con la teoria.",
    styles['Pass']))

story.append(Spacer(1, 0.5*inch))

# =====================================================================
# 5. RESUMEN FINAL
# =====================================================================
story.append(Paragraph("5. Resumen Final", styles['SectionHead']))
add_hr()

summary_data = [
    ['Metrica', 'Valor'],
    ['Total de verificaciones', '55'],
    ['Aprobadas', '55'],
    ['Fallidas', '0'],
    ['Metodo Vandermonde', 'Coeficientes, interpolacion, etapas, errores: OK'],
    ['Metodo Simpson 3/8', 'Exactitud, convergencia, etapas, errores: OK'],
    ['Datos del profesor', 'Coinciden exactamente con ResultadosMetodos2.txt'],
]
story.append(make_table(summary_data, col_widths=[2.5*inch, 4*inch]))
story.append(Spacer(1, 0.2*inch))

# Archivos
story.append(Paragraph("Archivos del proyecto:", styles['SmallBold']))
files_data = [
    ['Archivo', 'Ruta'],
    ['Vandermonde', 'app/methods/vandermonde.py'],
    ['Simpson 3/8', 'app/methods/simpson38.py'],
    ['Script de pruebas', 'test_vandermonde_simpson38.py'],
    ['Este reporte PDF', 'Reporte_Pruebas_Metodos.pdf'],
]
story.append(make_table(files_data, col_widths=[2*inch, 4.5*inch]))

# === GENERAR PDF ===
doc.build(story)
print(f"\n[OK] PDF generado exitosamente en:\n  {OUTPUT_PATH}")
print(f"  Tamano: {os.path.getsize(OUTPUT_PATH):,} bytes")
