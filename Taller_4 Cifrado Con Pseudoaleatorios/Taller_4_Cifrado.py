
M1 = 1_000_000_007
M2 = 998_244_353
A  = 6_271
B  = 3_571


semilla = int(input("Ingresa la semilla: "))

p = semilla % M1 or 1
q = (semilla * 1_000_003 + 1) % M2

def generar():
    global p, q
    p = (A * p + q) % M1
    q = (B * q + p * p) % M2
    return (p + q) % 101


N = 10
numeros = []

for _ in range(N):
    numeros.append(generar())

print(f"Arreglo de números generados: {numeros}")

palabra = input("Ingresa la palabra a cifrar: ")


indices = sorted(range(len(palabra)), key=lambda i: numeros[i % N])
palabra_permutada = ''.join(palabra[i] for i in indices)


cifrado = ""
estado = semilla % 256 or 1
for i, char in enumerate(palabra_permutada):
    clave = numeros[i % N]
    estado = (ord(char) * clave + estado ^ clave) % 256
    if 33 <= estado <= 126:
        cifrado += chr(estado)

print(f"Texto cifrado: {cifrado}")

cifrado_ordenado = ''.join(sorted(cifrado, key=ord))
print(f"Texto cifrado ordenado (ASCII): {cifrado_ordenado}")
