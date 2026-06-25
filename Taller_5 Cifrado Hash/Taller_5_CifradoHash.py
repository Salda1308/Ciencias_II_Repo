
M1 = 1_000_000_007
M2 = 998_244_353
A  = 6_271
B  = 3_571


semilla = int(input("Ingresa la semilla: "))

p_init = semilla % M1 or 1
q_init = (semilla * 1_000_003 + 1) % M2

N = 10

def generar_numeros(p, q):
    nums = []
    for _ in range(N):
        p = (A * p + q) % M1
        q = (B * q + p * p) % M2
        nums.append((p + q) % 101)
    return nums

numeros = generar_numeros(p_init, q_init)
print(f"Arreglo de números generados: {numeros}")


def calcular_hash(palabra):
    LONGITUD = 32
    indices = sorted(range(len(palabra)), key=lambda i: numeros[i % N])
    palabra_permutada = ''.join(palabra[i] for i in indices)

    estado = semilla % 256 or 1
    for i, char in enumerate(palabra_permutada):
        clave = numeros[i % N]
        estado = (ord(char) * clave + estado ^ clave) % 256

    cifrado = ""
    for i in range(LONGITUD):
        clave = numeros[i % N]
        estado = (A * estado + clave * B + i) % 256
        cifrado += chr((estado % 94) + 33)

    return cifrado


# Registro de hashes: hash -> primera palabra que lo produjo
registro_hashes = {}

while True:
    palabra = input("\nIngresa la palabra a cifrar (o 'salir' para terminar): ")
    if palabra.lower() == "salir":
        break

    cifrado = calcular_hash(palabra)
    cifrado_ordenado = ''.join(sorted(cifrado, key=ord))

    print(f"Texto cifrado: {cifrado}")
    print(f"Longitud: {len(cifrado)} caracteres")
    print(f"Texto cifrado ordenado (ASCII): {cifrado_ordenado}")

    # Validación de colisiones
    if cifrado in registro_hashes:
        palabra_anterior = registro_hashes[cifrado]
        if palabra_anterior != palabra:
            print(f"\n⚠ COLISION DETECTADA:")
            print(f"  '{palabra_anterior}' y '{palabra}' producen el mismo hash.")
        else:
            print("(Misma palabra ingresada anteriormente, mismo hash esperado.)")
    else:
        registro_hashes[cifrado] = palabra
        print(f"Hash registrado. Total de hashes únicos: {len(registro_hashes)}")

print(f"\nResumen: {len(registro_hashes)} hashes únicos de {sum(1 for _ in registro_hashes)} entradas distintas.")
