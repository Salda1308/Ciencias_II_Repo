import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from enigma import extraer_digitos, cesar_cifrar, cesar_descifrar, generar_componentes, generar_reflector
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

if __name__ == "__main__":
    test_extraer_digitos()
    test_cesar_cifrar_descifrar()
    test_cesar_borde_z()
    test_generar_componentes_estructura()
    test_reflector_autorecíproco()
    test_generacion_determinista()
    print("\nTodos los tests de Task 1 y 2 pasaron.")
