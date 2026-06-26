import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from enigma import extraer_digitos, cesar_cifrar, cesar_descifrar

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

if __name__ == "__main__":
    test_extraer_digitos()
    test_cesar_cifrar_descifrar()
    test_cesar_borde_z()
    print("\nTodos los tests de Task 1 pasaron.")
