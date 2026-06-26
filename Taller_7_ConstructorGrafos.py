

def generarConexion(NodoA, NodoB, peso):   
    return [NodoA, NodoB, peso]

def generarGrafo():
    grafo = []
    while True:
        opcion = input("Ingresa Conexion (C), Terminar conexiones (T): ")
        if opcion == "T":
            break
        elif opcion == "C":
            nodoA = input("Ingresa Nodo 1: ")
            nodoB = input("Ingresa Nodo 2: ")
            peso = float(input("Ingresa peso: "))
            grafo.append(generarConexion(nodoA, nodoB, peso))
    return grafo

def imprimirGrafo(grafo):
    print("Grafo:")
    for conexion in grafo:
        print(f"{conexion[0]} --({conexion[2]})--> {conexion[1]}")

def listaIncidencia(grafo):
    nodos = set()
    for conexion in grafo:
        nodos.add(conexion[0])
        nodos.add(conexion[1])
    
    nodos = sorted(nodos)
    incidencia = {nodo: [] for nodo in nodos}
    
    for conexion in grafo:
        incidencia[conexion[0]].append((conexion[1], conexion[2]))
        incidencia[conexion[1]].append((conexion[0], conexion[2]))
    
    return incidencia

def listaAdyacencia(grafo):
    nodos = set()
    for conexion in grafo:
        nodos.add(conexion[0])
        nodos.add(conexion[1])
    
    nodos = sorted(nodos)
    adyacencia = {nodo: [] for nodo in nodos}
    
    for conexion in grafo:
        adyacencia[conexion[0]].append(conexion[1])
        adyacencia[conexion[1]].append(conexion[0])
    
    return adyacencia

def matrizIncidencia(grafo):
    nodos = set()
    for conexion in grafo:
        nodos.add(conexion[0])
        nodos.add(conexion[1])
    
    nodos = sorted(nodos)
    matriz = [[0 for _ in range(len(grafo))] for _ in range(len(nodos))]
    
    for j, conexion in enumerate(grafo):
        nodoA_index = nodos.index(conexion[0])
        nodoB_index = nodos.index(conexion[1])
        matriz[nodoA_index][j] = conexion[2]
        matriz[nodoB_index][j] = conexion[2]
    
    return matriz

def matrizAdyacencia(grafo):
    nodos = set()
    for conexion in grafo:
        nodos.add(conexion[0])
        nodos.add(conexion[1])
    
    nodos = sorted(nodos)
    matriz = [[0 for _ in range(len(nodos))] for _ in range(len(nodos))]
    
    for conexion in grafo:
        nodoA_index = nodos.index(conexion[0])
        nodoB_index = nodos.index(conexion[1])
        matriz[nodoA_index][nodoB_index] = conexion[2]
        matriz[nodoB_index][nodoA_index] = conexion[2]
    
    return matriz

def main():
    grafo = generarGrafo()
    imprimirGrafo(grafo)
    incidencia = listaIncidencia(grafo)
    adyacencia = listaAdyacencia(grafo)
    print("\nLista de Incidencia:")
    for nodo, conexiones in incidencia.items():
        print(f"{nodo}: {conexiones}")
    print("\nLista de Adyacencia:")
    for nodo, nodos_adyacentes in adyacencia.items():
        print(f"{nodo}: {nodos_adyacentes}")
    matriz = matrizIncidencia(grafo)
    print("\nMatriz de Incidencia:")
    for fila in matriz:
        print(fila)
    matriz_adyacencia = matrizAdyacencia(grafo)
    print("\nMatriz de Adyacencia:")
    for fila in matriz_adyacencia:
        print(fila)
if __name__ == "__main__":
    main()