import random

# ── Utilidades César variable ──────────────────────────────────────────────────

def extraer_digitos(n: int) -> list:
    return [int(d) for d in str(abs(n))]

def cesar_cifrar(texto: str, digitos: list) -> str:
    resultado = []
    for i, c in enumerate(texto):
        shift = digitos[i % len(digitos)]
        resultado.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
    return ''.join(resultado)

def cesar_descifrar(texto: str, digitos: list) -> str:
    resultado = []
    for i, c in enumerate(texto):
        shift = digitos[i % len(digitos)]
        resultado.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
    return ''.join(resultado)

# ── Generación de componentes desde dato público ───────────────────────────────

def generar_reflector(rng) -> list:
    indices = list(range(26))
    rng.shuffle(indices)
    reflector = [0] * 26
    for i in range(0, 26, 2):
        a, b = indices[i], indices[i + 1]
        reflector[a] = b
        reflector[b] = a
    return reflector

def generar_componentes(dato_publico: int) -> dict:
    rng = random.Random(dato_publico)
    rotores = []
    notches = []
    for _ in range(3):
        perm = list(range(26))
        rng.shuffle(perm)
        rotores.append(perm)
        notches.append(rng.randint(0, 25))
    reflector = generar_reflector(rng)
    return {"rotores": rotores, "notches": notches, "reflector": reflector}
