import math

def newton(f, x0, tolerancia=1e-6, max_iter=100):
    def derivada_aprox(f, x, h=1e-6):
        return (f(x + h) - f(x - h)) / (2*h)
    
    x = x0
    
    for i in range(max_iter):
        fx = f(x)
        dfx = derivada_aprox(f, x)
        
        if dfx == 0:
            print("Error: derivada cero.")
            return None
        
        x_nuevo = x - fx / dfx
        
        if abs(x_nuevo - x) < tolerancia:
            print(f"Convergió en {i+1} iteraciones.")
            return x_nuevo
        
        x = x_nuevo
    
    print("No convergió.")
    return None


# Pedir función al usuario
expr = input("Ingresa la función en términos de x (ej: x**2 - 2): ")

# Crear función a partir del texto
def f(x):
    return eval(expr, {"x": x, "math": math})

# Pedir valor inicial
x0 = float(input("Ingresa el valor inicial: "))

# Ejecutar
raiz = newton(f, x0)

print("Raíz aproximada:", raiz)