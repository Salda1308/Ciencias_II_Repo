import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from enigma import extraer_digitos, cesar_cifrar, cesar_descifrar, generar_componentes, generar_reflector
from enigma import cifrar_mensaje, invertir_permutacion
import random as _random

def test_extraer_digitos():
    assert extraer_digitos(7391) == [7, 3, 9, 1]
    assert extraer_digitos(5) == [5]
    assert extraer_digitos(100) == [1, 0, 0]
    print("PASS test_extraer_digitos")

def test_cesar_cifrar_descifrar():
    digitos = [7, 3, 9]
    original = "ACF"
    cifrado = cesar_cifrar(original, digitos)
    assert len(cifrado) == 3
    assert cifrado != original
    assert cesar_descifrar(cifrado, digitos) == original
    print("PASS test_cesar_cifrar_descifrar")

def test_cesar_borde_z():
    # Desplazamiento debe hacer wrap-around del alfabeto
    digitos = [3]
    # 'Z' + 3 = 'C'
    assert cesar_cifrar("Z", digitos) == "C"
    assert cesar_descifrar("C", digitos) == "Z"
    print("PASS test_cesar_borde_z")

def test_generar_componentes_estructura():
    comp = generar_componentes(7391)
    assert len(comp["rotores"]) == 3
    assert len(comp["notches"]) == 3
    assert len(comp["reflector"]) == 26
    for r in comp["rotores"]:
        assert sorted(r) == list(range(26)), "Rotor no es permutación válida"
    print("PASS test_generar_componentes_estructura")

def test_reflector_autorecíproco():
    comp = generar_componentes(7391)
    ref = comp["reflector"]
    for i in range(26):
        assert ref[ref[i]] == i, f"Reflector no es auto-recíproco en índice {i}"
    print("PASS test_reflector_autorecíproco")

def test_generacion_determinista():
    c1 = generar_componentes(12345)
    c2 = generar_componentes(12345)
    assert c1["rotores"] == c2["rotores"]
    assert c1["reflector"] == c2["reflector"]
    print("PASS test_generacion_determinista")

def test_invertir_permutacion():
    perm = [1, 0, 3, 2]  # permutación simple
    inv = invertir_permutacion(perm)
    assert inv == [1, 0, 3, 2]  # esta permutación es su propia inversa
    perm2 = [2, 0, 1]
    inv2 = invertir_permutacion(perm2)
    for i in range(3):
        assert perm2[inv2[i]] == i
    print("PASS test_invertir_permutacion")

def test_enigma_simetria():
    # Cifrar dos veces con mismas posiciones iniciales debe dar el texto original
    msg = "HOLA"
    dato = 7391
    clave_cifrada = "DGP"
    digitos = extraer_digitos(dato)
    pos_init = [ord(c) - ord('A') for c in cesar_descifrar(clave_cifrada, digitos)]
    cifrado = cifrar_mensaje(msg, dato, pos_init)
    descifrado = cifrar_mensaje(cifrado, dato, pos_init)
    assert descifrado == msg, f"Esperaba '{msg}', obtuve '{descifrado}'"
    print("PASS test_enigma_simetria")

def test_enigma_no_mapea_a_si_misma():
    # En Enigma, ninguna letra se cifra a sí misma
    dato = 9999
    posiciones = [0, 0, 0]
    for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        cifrada = cifrar_mensaje(letra, dato, [0, 0, 0])
        assert cifrada != letra, f"'{letra}' se mapeó a sí misma"
    print("PASS test_enigma_no_mapea_a_si_misma")

if __name__ == "__main__":
    test_extraer_digitos()
    test_cesar_cifrar_descifrar()
    test_cesar_borde_z()
    test_generar_componentes_estructura()
    test_reflector_autorecíproco()
    test_generacion_determinista()
    test_invertir_permutacion()
    test_enigma_simetria()
    test_enigma_no_mapea_a_si_misma()
    print("\nTodos los tests de Tasks 1, 2 y 3 pasaron.")
