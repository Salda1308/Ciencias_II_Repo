from math import ceil

def nodo(hoja=True):
    return {'hoja': hoja, 'claves': [], 'hijos': [], 'siguiente': None}

def dividir_nodo(n, m):
    if n['hoja']:
        mid = m // 2
        central = n['claves'][mid]
        der = nodo(True)
        der['claves'] = n['claves'][mid:]
        der['siguiente'] = n['siguiente']
        n['claves'] = n['claves'][:mid]
        n['siguiente'] = der
        return central, der
    else:
        mid = ceil(m / 2) - 1
        central = n['claves'][mid]
        der = nodo(False)
        der['claves'] = n['claves'][mid+1:]
        der['hijos'] = n['hijos'][mid+1:]
        n['claves'] = n['claves'][:mid]
        n['hijos'] = n['hijos'][:mid+1]
        return central, der

def insertar_en(n, k, m):
    if n['hoja']:
        i = next((j for j, v in enumerate(n['claves']) if v > k), len(n['claves']))
        n['claves'].insert(i, k)
    else:
        i = next((j for j, v in enumerate(n['claves']) if v > k), len(n['claves']))
        res = insertar_en(n['hijos'][i], k, m)
        if res:
            central, der = res
            n['claves'].insert(i, central)
            n['hijos'].insert(i+1, der)
    if len(n['claves']) == m:
        return dividir_nodo(n, m)

def insertar(arbol, k):
    res = insertar_en(arbol['raiz'], k, arbol['m'])
    if res:
        central, der = res
        nueva = nodo(False)
        nueva['claves'] = [central]
        nueva['hijos'] = [arbol['raiz'], der]
        arbol['raiz'] = nueva

def fusionar(n, i):
    h, s = n['hijos'][i], n['hijos'][i+1]
    if h['hoja']:
        h['claves'] += s['claves']
        h['siguiente'] = s['siguiente']
    else:
        h['claves'] += [n['claves'][i]] + s['claves']
        h['hijos'] += s['hijos']
    n['claves'].pop(i)
    n['hijos'].pop(i+1)

def rotar(n, i, d):
    h, s = n['hijos'][i], n['hijos'][i+d]
    if h['hoja']:
        if d == -1:
            h['claves'].insert(0, s['claves'].pop())
            n['claves'][i-1] = h['claves'][0]
        else:
            h['claves'].append(s['claves'].pop(0))
            n['claves'][i] = s['claves'][0]
    else:
        if d == -1:
            h['claves'].insert(0, n['claves'][i-1]); n['claves'][i-1] = s['claves'].pop()
            h['hijos'].insert(0, s['hijos'].pop())
        else:
            h['claves'].append(n['claves'][i]); n['claves'][i] = s['claves'].pop(0)
            h['hijos'].append(s['hijos'].pop(0))

def rellenar(n, i, m):
    min_c = ceil(m / 2) - 1
    if i > 0 and len(n['hijos'][i-1]['claves']) > min_c:
        rotar(n, i, -1)
    elif i < len(n['hijos'])-1 and len(n['hijos'][i+1]['claves']) > min_c:
        rotar(n, i, 1)
    else:
        fusionar(n, i if i < len(n['hijos'])-1 else i-1)

def eliminar_en(n, k, m):
    min_c = ceil(m / 2) - 1
    if n['hoja']:
        if k in n['claves']:
            n['claves'].remove(k)
        return
    i = next((j for j, v in enumerate(n['claves']) if v > k), len(n['claves']))
    if len(n['hijos'][i]['claves']) <= min_c:
        rellenar(n, i, m)
        i = min(i, len(n['claves']))
    eliminar_en(n['hijos'][i], k, m)

def eliminar(arbol, k):
    eliminar_en(arbol['raiz'], k, arbol['m'])
    if not arbol['raiz']['claves'] and not arbol['raiz']['hoja']:
        arbol['raiz'] = arbol['raiz']['hijos'][0]

def buscar_rango(arbol, ini, fin):
    n = arbol['raiz']
    while not n['hoja']:
        i = next((j for j, v in enumerate(n['claves']) if v > ini), len(n['claves']))
        n = n['hijos'][i]
    resultado = []
    while n:
        for k in n['claves']:
            if ini <= k <= fin:
                resultado.append(k)
            elif k > fin:
                return resultado
        n = n['siguiente']
    return resultado

def mostrar(raiz):
    nivel = [raiz]
    num = 0
    while nivel:
        print(f"Nivel {num}: " + "   ".join(str(nd['claves']) for nd in nivel))
        nivel = [h for nd in nivel for h in nd['hijos']]
        num += 1
    n = raiz
    while not n['hoja']: n = n['hijos'][0]
    hojas = []
    while n:
        hojas.append(str(n['claves']))
        n = n['siguiente']
    if len(hojas) > 1:
        print("Hojas: " + " -> ".join(hojas))

m = int(input("M = maximo de hijos: "))
arbol = {'m': m, 'raiz': nodo()}

while True:
    opc = input("\n[i] Insertar  [e] Eliminar  [r] Rango  [s] Salir > ").strip().lower()
    if opc == 's':
        break
    if opc in ('i', 'e'):
        try:
            k = int(input("Clave: "))
            if opc == 'i': insertar(arbol, k)
            else: eliminar(arbol, k)
            mostrar(arbol['raiz'])
        except ValueError:
            print("Numero invalido.")
    elif opc == 'r':
        try:
            ini, fin = int(input("Desde: ")), int(input("Hasta: "))
            print(f"Rango [{ini},{fin}]: {buscar_rango(arbol, ini, fin)}")
        except ValueError:
            print("Numero invalido.")
    else:
        print("Opcion invalida.")
