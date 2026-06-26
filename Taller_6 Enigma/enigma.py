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

# ── Núcleo de la máquina Enigma ────────────────────────────────────────────────

def invertir_permutacion(perm: list) -> list:
    inv = [0] * len(perm)
    for i, v in enumerate(perm):
        inv[v] = i
    return inv

def avanzar_rotores(pos: list, notches: list) -> list:
    p = pos[:]
    avanza_2 = (p[0] == notches[0])
    avanza_3 = (p[1] == notches[1])
    p[0] = (p[0] + 1) % 26
    if avanza_2:
        p[1] = (p[1] + 1) % 26
    if avanza_3:
        p[2] = (p[2] + 1) % 26
    return p

def _pasar_rotor(idx: int, perm: list, offset: int) -> int:
    return (perm[(idx + offset) % 26] - offset) % 26

def _pasar_rotor_inv(idx: int, inv_perm: list, offset: int) -> int:
    return (inv_perm[(idx + offset) % 26] - offset) % 26

def cifrar_letra(idx: int, rotores: list, inv_rotores: list, reflector: list, pos: list) -> int:
    # Ida: rotor 0 → rotor 1 → rotor 2 → reflector
    idx = _pasar_rotor(idx, rotores[0], pos[0])
    idx = _pasar_rotor(idx, rotores[1], pos[1])
    idx = _pasar_rotor(idx, rotores[2], pos[2])
    idx = reflector[idx]
    # Vuelta: rotor 2 inv → rotor 1 inv → rotor 0 inv
    idx = _pasar_rotor_inv(idx, inv_rotores[2], pos[2])
    idx = _pasar_rotor_inv(idx, inv_rotores[1], pos[1])
    idx = _pasar_rotor_inv(idx, inv_rotores[0], pos[0])
    return idx

def cifrar_mensaje(mensaje: str, dato_publico: int, posiciones_init: list) -> str:
    comp = generar_componentes(dato_publico)
    rotores = comp["rotores"]
    notches = comp["notches"]
    reflector = comp["reflector"]
    inv_rotores = [invertir_permutacion(r) for r in rotores]

    pos = posiciones_init[:]
    resultado = []
    for c in mensaje.upper():
        if not c.isalpha():
            continue
        pos = avanzar_rotores(pos, notches)
        idx = ord(c) - ord('A')
        idx = cifrar_letra(idx, rotores, inv_rotores, reflector, pos)
        resultado.append(chr(idx + ord('A')))
    return ''.join(resultado)

# ── Interfaz de usuario ────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("       MÁQUINA ENIGMA — Taller 6")
    print("=" * 50)

    dato_publico = int(input("\nIngresa el dato público (número entero): "))
    clave_cifrada = input("Ingresa la clave cifrada (3 letras A-Z): ").upper().strip()

    if len(clave_cifrada) != 3 or not clave_cifrada.isalpha():
        print("Error: la clave cifrada debe ser exactamente 3 letras A-Z.")
        return

    digitos = extraer_digitos(dato_publico)
    posiciones_str = cesar_descifrar(clave_cifrada, digitos)
    posiciones_init = [ord(c) - ord('A') for c in posiciones_str]

    print(f"\nPosiciones iniciales de rotores: {posiciones_str}")

    modo = input("\nModo — Cifrar (C) / Descifrar (D): ").upper().strip()
    if modo not in ("C", "D"):
        print("Error: ingresa 'C' para cifrar o 'D' para descifrar.")
        return

    mensaje = input("Ingresa el mensaje (solo letras A-Z): ").upper()
    letras = ''.join(c for c in mensaje if c.isalpha())

    if not letras:
        print("Error: el mensaje no contiene letras.")
        return

    resultado = cifrar_mensaje(letras, dato_publico, posiciones_init)

    print("\n" + "=" * 50)
    print(f"Dato público   : {dato_publico}")
    print(f"Clave cifrada  : {clave_cifrada}")
    print(f"Posiciones init: {posiciones_str}")
    accion = "Cifrado" if modo == "C" else "Descifrado"
    print(f"Mensaje        : {letras}")
    print(f"{accion}      : {resultado}")
    print("=" * 50)


if __name__ == "__main__":
    main()
