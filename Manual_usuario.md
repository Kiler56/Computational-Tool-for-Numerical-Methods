**Manual de Usuario**

**Herramienta Computacional para Métodos Numéricos**

**Información general del proyecto**

**Nombre del proyecto:** Computational Tool for Numerical Methods  
**Repositorio oficial:** [Computational Tool for Numerical Methods](https://github.com/Kiler56/Computational-Tool-for-Numerical-Methods?utm_source=chatgpt.com)

La aplicación fue desarrollada como una herramienta educativa y computacional orientada al aprendizaje, análisis y aplicación práctica de métodos numéricos utilizados en ingeniería, matemáticas y ciencias computacionales.

El sistema permite que estudiantes e ingenieros puedan:

- ejecutar diferentes métodos numéricos,
- analizar resultados iterativos,
- comprender las condiciones necesarias para aplicar cada método,
- y visualizar gráficamente el comportamiento de funciones y aproximaciones.

La plataforma integra además una graficadora que facilita la interpretación visual de los algoritmos implementados.

**1\. Introducción**

Los métodos numéricos son técnicas matemáticas utilizadas para resolver problemas que no pueden solucionarse fácilmente mediante métodos analíticos exactos.

Esta herramienta reúne diferentes algoritmos clásicos utilizados en:

- búsqueda de raíces,
- solución de sistemas de ecuaciones,
- interpolación,
- integración numérica,
- y ecuaciones diferenciales ordinarias.

El propósito principal de la aplicación es fortalecer el aprendizaje práctico mediante simulaciones, iteraciones y visualización gráfica de los métodos.

**2\. Usuarios objetivo**

La herramienta está dirigida principalmente a:

- estudiantes de ingeniería de sistemas,
- estudiantes de ingeniería matemática,
- estudiantes de ciencias aplicadas,
- docentes,
- y usuarios interesados en métodos numéricos.

**3\. Requisitos del sistema**

**Requisitos mínimos**

- Sistema operativo Windows, Linux o macOS.
- Python instalado.
- Navegador moderno o entorno gráfico compatible.
- Conexión local para ejecución del proyecto.

**Requisitos recomendados**

- 8 GB de memoria RAM o superior.
- Procesador multinúcleo.
- Resolución Full HD.

**4\. Instalación del sistema**

**Paso 1: Clonar el repositorio**

git clone <https://github.com/Kiler56/Computational-Tool-for-Numerical-Methods.git>

**Paso 2: Ingresar al directorio del proyecto**

cd Computational-Tool-for-Numerical-Methods

**Paso 3: Instalar dependencias**

pip install -r requirements.txt

**Paso 4: Ejecutar la aplicación**

python main.py

Nota: Dependiendo de la estructura del proyecto, el archivo principal puede variar.

**5\. Navegación general de la aplicación**

La plataforma se encuentra organizada por módulos de métodos numéricos.

Cada sección incluye:

- explicación básica del método,
- entradas requeridas,
- validaciones,
- tablas iterativas,
- resultados numéricos,
- y visualización gráfica.

La interfaz permite navegar entre diferentes categorías de métodos desde el menú principal.

**6\. Métodos implementados**

**6.1 Métodos de búsqueda de raíces**

Estos métodos permiten encontrar soluciones de ecuaciones no lineales.

**Métodos disponibles**

- Búsquedas incrementales
- Bisección
- Regla falsa
- Punto fijo
- Newton
- Secante
- Raíces múltiples

**6.1.1 Búsquedas Incrementales**

**Descripción**

Método utilizado para detectar intervalos donde posiblemente exista una raíz mediante cambios de signo.

**Requisitos**

- La función debe ser continua.
- Debe existir un intervalo de exploración.

**Entradas**

- Función
- Valor inicial
- Incremento
- Número máximo de iteraciones

**Resultados**

- Intervalos candidatos
- Tabla iterativa
- Representación gráfica

**6.1.2 Método de Bisección**

**Descripción**

Método iterativo que divide continuamente un intervalo para aproximar una raíz.

**Requisitos**

- La función debe ser continua.
- Debe existir cambio de signo en el intervalo.

**Entradas**

- Función (f(x))
- Intervalo inicial (\[a,b\])
- Tolerancia
- Número máximo de iteraciones

**Resultados**

- Aproximación de la raíz
- Error calculado
- Tabla iterativa
- Gráfica de la función

**6.1.3 Regla Falsa**

**Descripción**

Método similar a bisección, pero utilizando interpolación lineal para aproximar la raíz.

**Requisitos**

- Cambio de signo en el intervalo.
- Función continua.

**Resultados**

- Aproximación de la raíz
- Error relativo
- Tabla de iteraciones

**6.1.4 Punto Fijo**

**Descripción**

Método iterativo basado en la transformación (x=g(x)).

**Requisitos**

- La función transformada debe converger.
- La derivada de (g(x)) debe cumplir condiciones de convergencia.

**Resultados**

- Aproximación de la raíz
- Iteraciones realizadas
- Error obtenido

**6.1.5 Método de Newton**

**Descripción**

Método basado en derivadas para aproximar raíces rápidamente.

**Requisitos**

- La función debe ser derivable.
- La derivada no debe ser cero cerca de la raíz.

**Entradas**

- Función
- Derivada
- Valor inicial
- Tolerancia

**Resultados**

- Aproximación de la raíz
- Iteraciones
- Error
- Visualización gráfica

**6.1.6 Método de la Secante**

**Descripción**

Método iterativo que aproxima la derivada utilizando dos valores iniciales.

**Requisitos**

- Dos aproximaciones iniciales.
- Convergencia adecuada.

**Resultados**

- Aproximación numérica
- Error iterativo
- Tabla de resultados

**6.1.7 Método de Raíces Múltiples**

**Descripción**

Método diseñado para funciones con raíces repetidas.

**Requisitos**

- Conocimiento de derivadas.
- Aproximación inicial adecuada.

**Resultados**

- Aproximación de la raíz múltiple
- Convergencia iterativa

**6.2 Sistemas de ecuaciones lineales**

Estos métodos permiten resolver sistemas matriciales.

**Métodos disponibles**

- Eliminación gaussiana
- Pivoteo parcial
- Pivoteo total
- LU simple
- LU pivoteo
- Crout
- Doolittle
- Cholesky
- Jacobi
- Gauss-Seidel
- SOR

**6.2.1 Eliminación Gaussiana**

**Descripción**

Transforma el sistema en una matriz triangular superior.

**Requisitos**

- Sistema compatible.
- Pivotes válidos.

**Resultados**

- Solución del sistema
- Procedimiento paso a paso

**6.2.2 Pivoteo Parcial**

**Descripción**

Intercambia filas para mejorar estabilidad numérica.

**Resultados**

- Matriz transformada
- Solución estable

**6.2.3 Pivoteo Total**

**Descripción**

Intercambia filas y columnas para evitar errores numéricos.

**Resultados**

- Mayor estabilidad computacional
- Solución del sistema

**6.2.4 Factorización LU**

**Métodos incluidos**

- LU simple
- LU pivoteo
- Crout
- Doolittle
- Cholesky

**Descripción**

Descomponen una matriz en productos matriciales para resolver sistemas lineales.

**Requisitos**

- Matriz cuadrada.
- En Cholesky, la matriz debe ser simétrica positiva definida.

**Resultados**

- Matrices factorizadas
- Solución del sistema

**6.2.5 Métodos Iterativos**

**Métodos incluidos**

- Jacobi
- Gauss-Seidel
- SOR

**Descripción**

Métodos aproximativos para resolver sistemas lineales.

**Requisitos**

- Preferiblemente matrices diagonalmente dominantes.
- Tolerancia y máximo de iteraciones definidos.

**Resultados**

- Aproximaciones iterativas
- Error por iteración
- Convergencia

**6.3 Interpolación**

Estos métodos permiten aproximar funciones a partir de conjuntos de puntos.

**Métodos disponibles**

- Vandermonde
- Newton (Diferencias divididas)
- Lagrange

**6.3.1 Método de Vandermonde**

**Descripción**

Construye un sistema matricial utilizando los puntos dados para obtener el polinomio interpolante.

**Requisitos**

- Los valores de (x) no deben repetirse.
- Se requieren al menos dos puntos.

**Entradas**

- Vector de puntos (x)
- Vector de puntos (y)

**Resultados**

- Matriz de Vandermonde
- Polinomio interpolante
- Evaluación gráfica

**Uso recomendado**

Se utiliza para comprender la construcción algebraica del polinomio interpolante.

**6.3.2 Método de Newton por Diferencias Divididas**

**Descripción**

Construye el polinomio interpolante utilizando diferencias divididas sucesivas.

**Ventajas**

- Permite agregar nuevos puntos sin recalcular todo el polinomio.
- Mayor eficiencia computacional.

**Entradas**

- Puntos (x)
- Puntos (y)

**Resultados**

- Tabla de diferencias divididas
- Polinomio interpolante
- Aproximación gráfica

**6.3.3 Método de Lagrange**

**Descripción**

Genera un polinomio interpolante mediante polinomios base.

**Requisitos**

- Los valores de (x) deben ser distintos.

**Resultados**

- Polinomio interpolante
- Evaluación numérica
- Representación gráfica

**Uso recomendado**

Adecuado para conjuntos pequeños de datos y fines educativos.

**6.4 Integración numérica**

Permite aproximar integrales definidas.

**Métodos disponibles**

- Método de Trapecio compuesto
- Método de Simpson 1/3 compuesto
- Método de Simpson 3/8 simple

**6.4.1 Método de Trapecio Compuesto**

**Descripción**

Aproxima el área bajo la curva mediante trapecios sucesivos.

**Resultados**

- Aproximación de la integral
- Error aproximado
- Gráfica del área

**6.4.2 Método de Simpson 1/3 Compuesto**

**Requisitos**

- Número par de subintervalos.

**Resultados**

- Aproximación del área
- Tabla de cálculo
- Representación gráfica

**6.4.3 Método de Simpson 3/8 Simple**

**Descripción**

Utiliza interpolación cúbica para aproximar integrales.

**Resultados**

- Aproximación numérica
- Área visualizada gráficamente

**6.5 Ecuaciones diferenciales**

Métodos para aproximar soluciones de ecuaciones diferenciales ordinarias.

**Métodos disponibles**

- Euler
- Heun

**6.5.1 Método de Euler**

**Descripción**

Método básico para aproximar soluciones de problemas de valor inicial.

**Entradas**

- Ecuación diferencial
- Condición inicial
- Tamaño de paso
- Intervalo

**Resultados**

- Tabla de aproximaciones
- Solución gráfica

**6.5.2 Método de Heun**

**Descripción**

Mejora la aproximación del método de Euler utilizando un promedio de pendientes.

**Resultados**

- Aproximación refinada
- Comparación gráfica
- Error reducido

**7\. Graficadora integrada**

La aplicación incluye una herramienta gráfica que permite visualizar:

- funciones matemáticas,
- comportamiento iterativo,
- aproximaciones numéricas,
- convergencia de métodos,
- interpolaciones,
- y soluciones aproximadas.

**Funcionalidades principales**

- Graficación de funciones.
- Visualización de raíces.
- Comparación entre métodos.
- Representación de puntos interpolados.
- Visualización de convergencia iterativa.

La graficadora facilita la comprensión visual y el análisis matemático de cada algoritmo.

**8\. Recomendaciones de uso**

- Verificar correctamente la sintaxis de las funciones matemáticas.
- Utilizar intervalos válidos.
- Revisar condiciones de convergencia.
- Definir tolerancias apropiadas.
- Validar las condiciones de las matrices antes de ejecutar métodos iterativos.

**9\. Posibles errores comunes**

| **Error**              | **Posible causa**                  |
| ---------------------- | ---------------------------------- |
| División por cero      | Derivada nula o pivote inválido    |
| El método no converge  | Mala aproximación inicial          |
| Intervalo inválido     | No existe cambio de signo          |
| Matriz singular        | El sistema no tiene solución única |
| Error de interpolación | Datos insuficientes o repetidos    |

**10\. Conclusiones**

La herramienta proporciona un entorno educativo e interactivo para comprender y aplicar métodos numéricos clásicos mediante simulación computacional y análisis gráfico.

La integración de algoritmos matemáticos, tablas iterativas y visualización gráfica permite fortalecer el aprendizaje práctico en ingeniería, matemáticas y ciencias computacionales.

El sistema facilita tanto la comprensión teórica como la experimentación práctica de los diferentes métodos implementados.
