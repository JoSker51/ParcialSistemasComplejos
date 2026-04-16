def S(n):
    return n + 1

# Suma: a + b = aplicar S b veces sobre a
def suma(a, b):
    resultado = a
    for _ in range(b):
        resultado = S(resultado)
    return resultado

# Multiplicación: a * b = sumar a consigo mismo b veces
def multiplicacion(a, b):
    if b == 0:
        return 0
    resultado = 0
    for _ in range(b):
        resultado = suma(resultado, a)
    return resultado

a = int(input("Ingresa el valor de a: "))
b = int(input("Ingresa el valor de b: "))

print("Resultado de la suma:", suma(a, b))
print("Resultado de la multiplicación:", multiplicacion(a, b))