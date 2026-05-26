**Manual de Usuario**

**Herramienta Computacional para Métodos Numéricos**

**Información General del Proyecto**

Nombre del proyecto: Computational Tool for Numerical Methods

Repositorio oficial:  
<https://github.com/Kiler56/Computational-Tool-for-Numerical-Methods>

La aplicación fue desarrollada como una herramienta educativa y computacional orientada al aprendizaje, análisis y aplicación práctica de métodos numéricos utilizados en ingeniería, matemáticas y ciencias computacionales.

El sistema permite que estudiantes e ingenieros puedan:

- Ejecutar diferentes métodos numéricos.
- Analizar resultados iterativos.
- Comprender las condiciones necesarias para aplicar cada método.
- Visualizar gráficamente funciones y aproximaciones numéricas.

La plataforma integra además una graficadora que facilita la interpretación visual de los algoritmos implementados.

**Tabla de Contenido**

- Introducción
- Usuarios Objetivo
- Requisitos del Sistema
- Instalación y Acceso a la Aplicación
- Navegación General
- Métodos Implementados
- Graficadora Integrada
- Recomendaciones de Uso
- Posibles Errores
- Conclusiones

**1\. Introducción**

Los métodos numéricos son técnicas matemáticas utilizadas para resolver problemas que no pueden solucionarse fácilmente mediante métodos analíticos exactos.

Esta herramienta reúne diferentes algoritmos clásicos utilizados en:

- Búsqueda de raíces.
- Solución de sistemas de ecuaciones.
- Interpolación.
- Integración numérica.
- Ecuaciones diferenciales ordinarias.

El propósito principal de la aplicación es fortalecer el aprendizaje práctico mediante simulaciones, iteraciones y visualización gráfica de los métodos.

**2\. Usuarios Objetivo**

La herramienta está dirigida principalmente a:

- Estudiantes de ingeniería de sistemas.
- Estudiantes de ingeniería matemática.
- Estudiantes de ciencias aplicadas.
- Docentes.
- Usuarios interesados en métodos numéricos.

**3\. Requisitos del Sistema**

**Requisitos mínimos**

- Sistema operativo Windows, Linux o macOS.
- Python instalado.
- Navegador moderno o entorno gráfico compatible.
- Conexión local para ejecución del proyecto.

**Requisitos recomendados**

- 8 GB de memoria RAM o superior.
- Procesador multinúcleo.
- Resolución Full HD.

**4\. Instalación y Acceso a la Aplicación**

La aplicación fue desplegada exitosamente y puede utilizarse tanto de manera web como de manera local.

**Acceso web**

El usuario puede acceder directamente a la plataforma desde el siguiente enlace:

<http://54.88.246.211:5000/>

Desde este entorno es posible utilizar todos los métodos numéricos implementados, realizar cálculos iterativos y visualizar resultados mediante la graficadora integrada.

**Ejecución local**

En caso de que el usuario desee ejecutar la aplicación localmente, debe seguir los siguientes pasos.

**Paso 1: Clonar el repositorio**

git clone <https://github.com/Kiler56/Computational-Tool-for-Numerical-Methods.git>

**Paso 2: Ingresar al directorio del proyecto**

cd Computational-Tool-for-Numerical-Methods

**Paso 3: Instalar dependencias**

pip install -r requirements.txt

**Paso 4: Ejecutar la aplicación**

python main.py

Nota: Dependiendo de la estructura del proyecto, el archivo principal puede variar.

**Recomendaciones de acceso**

- Se recomienda utilizar navegadores actualizados.
- Verificar conexión a internet para el acceso web.
- Para ejecución local, asegurarse de tener Python y las dependencias instaladas correctamente.

**5\. Navegación General de la Aplicación**

La plataforma se encuentra organizada por módulos de métodos numéricos.

Cada sección incluye:

- Explicación básica del método.
- Entradas requeridas.
- Validaciones.
- Tablas iterativas.
- Resultados numéricos.
- Visualización gráfica.

La interfaz permite navegar entre diferentes categorías de métodos desde el menú principal.

**6\. Métodos Implementados**

**6.1 Métodos de Búsqueda de Raíces**

Estos métodos permiten encontrar soluciones de ecuaciones no lineales.

**Métodos disponibles**

- Búsquedas incrementales
- Bisección
- Regla falsa
- Punto fijo
- Newton
- Secante
- Raíces múltiples

**Búsquedas Incrementales**

Descripción:

Método utilizado para detectar intervalos donde posiblemente exista una raíz mediante cambios de signo.

Requisitos:

- La función debe ser continua.
- Debe existir un intervalo de exploración.

Resultados:

- Intervalos candidatos
- Tabla iterativa
- Representación gráfica

**Método de Bisección**

Descripción:

Método iterativo que divide continuamente un intervalo para aproximar una raíz.

Requisitos:

- La función debe ser continua.
- Debe existir cambio de signo en el intervalo.

Resultados:

- Aproximación de la raíz
- Error calculado
- Tabla iterativa
- Gráfica de la función

**Regla Falsa**

Descripción:

Método similar a bisección, pero utilizando interpolación lineal para aproximar la raíz.

Requisitos:

- Cambio de signo en el intervalo.
- Función continua.

Resultados:

- Aproximación de la raíz
- Error relativo
- Tabla de iteraciones

**Punto Fijo**

Descripción:

Método iterativo basado en la transformación x = g(x).

Requisitos:

- La función transformada debe converger.
- La derivada de g(x) debe cumplir condiciones de convergencia.

Resultados:

- Aproximación de la raíz
- Iteraciones realizadas
- Error obtenido

**Método de Newton**

Descripción:

Método basado en derivadas para aproximar raíces rápidamente.

Requisitos:

- La función debe ser derivable.
- La derivada no debe ser cero cerca de la raíz.

Resultados:

- Aproximación de la raíz
- Iteraciones
- Error
- Visualización gráfica

**Método de la Secante**

Descripción:

Método iterativo que aproxima la derivada utilizando dos valores iniciales.

Resultados:

- Aproximación numérica
- Error iterativo
- Tabla de resultados

**Método de Raíces Múltiples**

Descripción:

Método diseñado para funciones con raíces repetidas.

Resultados:

- Aproximación de la raíz múltiple
- Convergencia iterativa

**6.2 Sistemas de Ecuaciones Lineales**

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

**Eliminación Gaussiana**

Descripción:

Transforma el sistema en una matriz triangular superior.

Resultados:

- Solución del sistema
- Procedimiento paso a paso

**Pivoteo Parcial**

Descripción:

Intercambia filas para mejorar estabilidad numérica.

Resultados:

- Matriz transformada
- Solución estable

**Pivoteo Total**

Descripción:

Intercambia filas y columnas para evitar errores numéricos.

Resultados:

- Mayor estabilidad computacional
- Solución del sistema

**Factorización LU**

Métodos incluidos:

- LU simple
- LU pivoteo
- Crout
- Doolittle
- Cholesky

Descripción:

Descomponen una matriz en productos matriciales para resolver sistemas lineales.

Resultados:

- Matrices factorizadas
- Solución del sistema

**Métodos Iterativos**

Métodos incluidos:

- Jacobi
- Gauss-Seidel
- SOR

Descripción:

Métodos aproximativos para resolver sistemas lineales.

Resultados:

- Aproximaciones iterativas
- Error por iteración
- Convergencia

**6.3 Interpolación**

Estos métodos permiten aproximar funciones a partir de conjuntos de puntos.

**Métodos disponibles**

- Vandermonde
- Newton (Diferencias divididas)
- Lagrange

**Método de Vandermonde**

Descripción:

Construye un sistema matricial utilizando los puntos dados para obtener el polinomio interpolante.

Resultados:

- Matriz de Vandermonde
- Polinomio interpolante
- Evaluación gráfica

**Método de Newton por Diferencias Divididas**

Descripción:

Construye el polinomio interpolante utilizando diferencias divididas sucesivas.

Resultados:

- Tabla de diferencias divididas
- Polinomio interpolante
- Aproximación gráfica

**Método de Lagrange**

Descripción:

Genera un polinomio interpolante mediante polinomios base.

Resultados:

- Polinomio interpolante
- Evaluación numérica
- Representación gráfica

**6.4 Integración Numérica**

Permite aproximar integrales definidas.

**Métodos disponibles**

- Método de Trapecio compuesto
- Método de Simpson 1/3 compuesto
- Método de Simpson 3/8 simple

**Método de Trapecio Compuesto**

Descripción:

Aproxima el área bajo la curva mediante trapecios sucesivos.

Resultados:

- Aproximación de la integral
- Error aproximado
- Gráfica del área

**Método de Simpson 1/3 Compuesto**

Resultados:

- Aproximación del área
- Tabla de cálculo
- Representación gráfica

**Método de Simpson 3/8 Simple**

Descripción:

Utiliza interpolación cúbica para aproximar integrales.

Resultados:

- Aproximación numérica
- Área visualizada gráficamente

**6.5 Ecuaciones Diferenciales**

Métodos para aproximar soluciones de ecuaciones diferenciales ordinarias.

**Métodos disponibles**

- Euler
- Heun

**Método de Euler**

Descripción:

Método básico para aproximar soluciones de problemas de valor inicial.

Resultados:

- Tabla de aproximaciones
- Solución gráfica

**Método de Heun**

Descripción:

Mejora la aproximación del método de Euler utilizando un promedio de pendientes.

Resultados:

- Aproximación refinada
- Comparación gráfica
- Error reducido

**7\. Graficadora Integrada**

La aplicación incluye una herramienta gráfica que permite visualizar:

- Funciones matemáticas.
- Comportamiento iterativo.
- Aproximaciones numéricas.
- Convergencia de métodos.
- Interpolaciones.
- Soluciones aproximadas.

Funcionalidades principales:

- Graficación de funciones.
- Visualización de raíces.
- Comparación entre métodos.
- Representación de puntos interpolados.
- Visualización de convergencia iterativa.

La graficadora facilita la comprensión visual y el análisis matemático de cada algoritmo.

**8\. Recomendaciones de Uso**

- Verificar correctamente la sintaxis de las funciones matemáticas.
- Utilizar intervalos válidos.
- Revisar condiciones de convergencia.
- Definir tolerancias apropiadas.
- Validar las condiciones de las matrices antes de ejecutar métodos iterativos.

**9\. Posibles Errores**

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
