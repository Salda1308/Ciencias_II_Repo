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
