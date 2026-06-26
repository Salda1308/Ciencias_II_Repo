# Diseño: Simulador de Máquina Enigma — Taller 6

## Contexto

Taller universitario de criptografía (Ciencias II). Los talleres anteriores implementaron cifrado pseudoaleatorio y hash. Este taller implementa una simulación de la máquina Enigma en Python, con rotores generados dinámicamente a partir de un dato público por grupo.

---

## Flujo general

```
Entrada del usuario (por input()):
  1. dato_publico   → número entero (ej: 7391)
  2. clave_cifrada  → 3 letras en A-Z cifradas con César variable (ej: "DGP")
  3. modo           → 'C' para cifrar, 'D' para descifrar
  4. mensaje        → texto en A-Z (sin espacios ni símbolos)

Proceso:
  1. Extraer dígitos del dato_publico de forma cíclica
  2. Descifrar clave_cifrada con César variable → posiciones iniciales (ej: "WDF")
  3. Generar rotores 1, 2, 3 y reflector usando dato_publico como semilla
  4. Inicializar máquina Enigma con esos rotores y las posiciones iniciales
  5. Procesar el mensaje letra por letra
  6. Mostrar resultado

Salida esperada:
  Dato público   : 7391
  Clave cifrada  : DGP
  Posiciones init: WDF
  Mensaje        : HOLAMUNDO
  Resultado      : QRTXBFKEA
```

---

## Sección 1: Cifrado César variable (protección de clave)

El `dato_publico` es un entero. Sus dígitos se extraen y se usan cíclicamente como offsets de César:

```
dato_publico = 7391
dígitos = [7, 3, 9, 1]  # se repiten cíclicamente si hacen falta

Cifrar posición i:    cifrada[i] = chr((ord(pos[i]) - ord('A') + dígitos[i % len(dígitos)]) % 26 + ord('A'))
Descifrar posición i: pos[i]     = chr((ord(cifrada[i]) - ord('A') - dígitos[i % len(dígitos)]) % 26 + ord('A'))
```

Las 3 posiciones iniciales (una por rotor) se cifran con este método para producir la `clave_cifrada` de 3 letras que el docente entrega a cada grupo.

---

## Sección 2: Generación de rotores y reflector

Se usa `random` de Python sembrado con `dato_publico` para generar todos los componentes de forma determinista:

```python
import random
rng = random.Random(dato_publico)

# Rotor: permutación aleatoria de 0-25 + posición de muesca (notch)
def generar_rotor(rng):
    perm = list(range(26))
    rng.shuffle(perm)
    notch = rng.randint(0, 25)
    return perm, notch

rotor1, notch1 = generar_rotor(rng)
rotor2, notch2 = generar_rotor(rng)
rotor3, notch3 = generar_rotor(rng)

# Reflector: permutación auto-recíproca (si A→M entonces M→A)
# Se generan 13 pares barajando [0..25] y mapeando cada par mutuamente
reflector = generar_reflector(rng)  # shuffle de [0..25], emparejar de 2 en 2
```

El reflector garantiza la propiedad de que cifrar dos veces el mismo texto con las mismas posiciones devuelve el original.

---

## Sección 3: Mecanismo de avance (stepping)

Antes de cifrar cada letra, los rotores avanzan:

- **Rotor 1** avanza siempre.
- **Rotor 2** avanza cuando la posición actual del Rotor 1 coincide con su muesca (`notch1`).
- **Rotor 3** avanza cuando la posición actual del Rotor 2 coincide con su muesca (`notch2`).

```
pos1 = (pos1 + 1) % 26
if pos1_antes == notch1: pos2 = (pos2 + 1) % 26
if pos2_antes == notch2: pos3 = (pos3 + 1) % 26
```

---

## Sección 4: Núcleo del cifrado (por letra)

```
letra_entrada → índice (A=0 … Z=25)

Paso adelante (entrada → reflector):
  idx = (idx + pos1) % 26
  idx = rotor1[idx]
  idx = (idx - pos1 + 26) % 26

  idx = (idx + pos2) % 26
  idx = rotor2[idx]
  idx = (idx - pos2 + 26) % 26

  idx = (idx + pos3) % 26
  idx = rotor3[idx]
  idx = (idx - pos3 + 26) % 26

  idx = reflector[idx]

Paso inverso (reflector → salida):
  idx = (idx + pos3) % 26
  idx = rotor3_inv[idx]
  idx = (idx - pos3 + 26) % 26

  idx = (idx + pos2) % 26
  idx = rotor2_inv[idx]
  idx = (idx - pos2 + 26) % 26

  idx = (idx + pos1) % 26
  idx = rotor1_inv[idx]
  idx = (idx - pos1 + 26) % 26

letra_salida ← índice
```

Las permutaciones inversas se calculan una sola vez al inicializar la máquina.

---

## Restricciones

- Alfabeto: solo A-Z (26 letras). El programa convierte el mensaje a mayúsculas y omite caracteres no alfabéticos.
- Sin plugboard (Steckerbrett).
- Interfaz: 100% por `input()`, sin argumentos CLI.
- Lenguaje: Python 3.

---

## Archivos a crear

- `Taller_6 Enigma/enigma.py` — implementación completa
