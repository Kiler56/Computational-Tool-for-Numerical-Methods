# 🧮 Manual de Usuario: NumCalc (Calculadora de Métodos Numéricos)

## 1. Introducción
**NumCalc** es una potente plataforma web diseñada para resolver problemas matemáticos mediante algoritmos numéricos. Fue creada para proporcionar no solo la respuesta final, sino también **el paso a paso**, visualizaciones gráficas interactivas y un robusto sistema de prevención de fallos. 

Este manual te guiará sobre cómo interactuar correctamente con la plataforma, introducir datos matemáticos y entender los resultados y posibles excepciones.

---

## 2. Acceso y Navegación Básica
Para utilizar la calculadora, abre tu navegador web (recomendado Chrome, Firefox o Edge) e ingresa a la siguiente dirección URL: **[http://54.88.246.211:5000](http://54.88.246.211:5000)**.

### Estructura de la Interfaz
- **Barra Lateral (Menú):** Te permite alternar entre las tres grandes familias de métodos:
  1. Ecuaciones de Una Variable (No Lineales).
  2. Sistemas de Ecuaciones Lineales.
  3. Interpolación.
- **Panel de Configuración:** Ubicado a la izquierda o arriba (dependiendo del tamaño de tu pantalla). Aquí introduces funciones, matrices, puntos y parámetros (tolerancia, iteraciones).
- **Área de Resultados:** Muestra tablas interactivas con las iteraciones, matrices transformadas (como L y U), y polinomios resultantes.
- **Graficador Interactivo:** Un módulo independiente que renderiza la función evaluada y resalta los puntos clave (como las raíces encontradas o los puntos interpolados). Puedes hacer zoom, mover el plano o exportar la gráfica como imagen.

---

## 3. Guía de Uso por Métodos

### A. Ecuaciones de Una Variable
**Métodos disponibles:** Bisección, Regla Falsa, Punto Fijo, Newton-Raphson, Secante y Raíces Múltiples.

**Instrucciones:**
1. **Ingreso de la Función $f(x)$:** Debes utilizar la sintaxis matemática estándar adaptada a programación. 
   - **Multiplicación:** Siempre usa asterisco `*`. (Ej: Escribe `2*x` en lugar de `2x`).
   - **Potencias:** Usa `^` o `**`. (Ej: `x^2` o `x**2`).
   - **Funciones trigonométricas/exponenciales:** Usa `sin(x)`, `cos(x)`, `tan(x)`, `exp(x)`, `log(x)`. *(No uses "sen", el estándar es "sin" en inglés).*
2. **Valores Iniciales:** Dependiendo del método, necesitarás un intervalo `[xi, xs]` (métodos cerrados) o puntos iniciales `x0, x1` (métodos abiertos). 
   - *Tip:* Utiliza el graficador preliminar para ver dónde cruza la gráfica el eje X y escoger puntos cercanos.
3. **Tolerancia ($Tol$):** Define qué tan pequeña debe ser la diferencia o el error para considerar que llegamos a la respuesta (Ej: `1e-7` que significa $1 \times 10^{-7}$).

### B. Sistemas de Ecuaciones Lineales
**Métodos disponibles:** Eliminación Gaussiana (Simple, Parcial, Total), Factorización LU (Simple, Parcial, Crout, Doolittle, Cholesky) y Métodos Iterativos (Jacobi, Gauss-Seidel, SOR).

**Instrucciones:**
1. **Tamaño del Sistema ($n$):** Primero define la dimensión de tu matriz cuadrada (ej. $3$ para un sistema $3 \times 3$).
2. **Ingreso de la Matriz $A$ y el vector $b$:** Llena las casillas que aparecerán dinámicamente en la pantalla. Puedes usar números enteros (`5`), decimales (`-3.14`) o fracciones.
3. **Para Métodos Iterativos:** Si usas Jacobi, Gauss-Seidel o SOR, el sistema solicitará adicionalmente:
   - **Vector Inicial $x_0$:** Una aproximación de partida (suele ser un vector de ceros).
   - **Relajación ($\omega$):** Un valor entre 0 y 2 exclusivo para el método SOR.

### C. Interpolación
**Métodos disponibles:** Vandermonde, Diferencias Divididas de Newton, Lagrange y Trazadores (Splines Lineales, Cuadráticos, Cúbicos).

**Instrucciones:**
1. **Número de Puntos:** Indica cuántas coordenadas $(X, Y)$ vas a ingresar.
2. **Ingreso de Coordenadas:** Llena las tablas con los valores de $X$ y $Y$. 
   - **¡Cuidado!** Nunca ingreses valores repetidos en $X$, ya que matemáticamente una función no puede tener dos valores de $Y$ distintos para un mismo $X$ (provocaría división por cero).

---

## 4. Diccionario de Excepciones y Solución de Errores

El "Backend" (servidor) de NumCalc está blindado mediante bloques `try-catch` y un manejador global de excepciones. Si algo sale mal matemáticamente, la plataforma **no se caerá**, sino que te mostrará una alerta explicativa. Aquí están las más comunes:

| Mensaje de Error / Excepción | ¿Por qué ocurre? | ¿Cómo solucionarlo? |
| :--- | :--- | :--- |
| **"ZeroDivisionError: División por cero detectada"** | 1. En Newton-Raphson, la derivada $f'(x)$ evaluada en tu punto inicial dio cero.<br>2. En Gauss/LU, un elemento de la diagonal principal (pivote) es 0. | - Cambia el valor inicial $x_0$ por otro un poco más lejano.<br>- En sistemas de ecuaciones, activa el **Pivoteo Parcial o Total** para que el sistema reorganice las filas automáticamente y evite el 0. |
| **"LinAlgError: Matriz Singular"** | El determinante de la matriz es cero. Esto significa que el sistema no tiene una solución única (tiene infinitas soluciones o ninguna). | Revisa los coeficientes de tu matriz. Es muy probable que una fila sea múltiplo de otra (Ej: Fila 1 es `[1, 2]` y Fila 2 es `[2, 4]`). |
| **"OverflowError: Resultado matemático demasiado grande"** | El método está divergiendo. En lugar de acercarse a la raíz, los números se hacen tan enormes que escapan la capacidad de memoria de Python. | - El punto inicial está muy lejos de la raíz.<br>- La función no es continua en ese tramo.<br>👉 **Solución:** Mira la gráfica y elige un punto más cercano. |
| **"MaxIterReached: El método no converge tras N iteraciones"** | Se alcanzó el límite máximo de iteraciones sin lograr llegar a la tolerancia deseada. | - Aumenta el número máximo de iteraciones (ej. de 100 a 500).<br>- Si el error sigue rebotando, el método oscila; prueba con otro método (ej. Bisección en vez de Newton). |
| **"Sintaxis inválida al evaluar la función"** | El procesador matemático (`sympify` o `eval`) no entendió lo que escribiste. | Revisa que estés usando `*` para multiplicar y paréntesis correctos. Ej: `2*x*(x-1)` en lugar de `2x(x-1)`. |

---

## 5. Buenas Prácticas Generales
1. **Usa el Historial:** A la derecha de la pantalla encontrarás un panel lateral con el historial. Úsalo para recuperar parámetros de ecuaciones complejas que escribiste antes, incluso si la ejecución anterior arrojó un error de división por cero.
2. **Aprovecha el Graficador Desacoplado:** El graficador Frontend ahora es completamente independiente. Pasa el cursor sobre la gráfica para inspeccionar las coordenadas de las intersecciones en el eje X antes de siquiera iniciar el cálculo iterativo.
3. **Cifras Significativas vs Tolerancia:** Si se te pide un ejercicio con "Tolerancia de $10^{-7}$", ingresa `1e-7`. El sistema calculará el error automáticamente utilizando notación científica moderna.
