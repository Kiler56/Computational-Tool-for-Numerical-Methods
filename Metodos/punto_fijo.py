import math

def punto_fijo(g, x0, tolerancia=1e-6, max_iter=100):
    x = x0
    
    for i in range(max_iter):
        x_nuevo = g(x)
        
        if abs(x_nuevo - x) < tolerancia:
            print(f"Convergió en {i+1} iteraciones.")
            return x_nuevo
        
        x = x_nuevo
    
    print("No convergió.")
    return None


# Pedir g(x)
expr = input("Ingresa g(x) (ej: (x+2/x)/2 ): ")

# Convertir texto a función
def g(x):
    return eval(expr, {"x": x, "math": math})

# Pedir valor inicial
x0 = float(input("Ingresa el valor inicial: "))

# Ejecutar método
raiz = punto_fijo(g, x0)

print("Resultado:", raiz)