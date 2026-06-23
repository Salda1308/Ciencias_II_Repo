from math import ceil

def nodo(hoja=True):
    return {'hoja': hoja, 'claves': [], 'hijos': []}

def dividir_nodo(n, m):
    mid = ceil(m / 2) - 1
    central = n['claves'][mid]
    der = nodo(n['hoja'])
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

def extremo(n, lado):
    while not n['hoja']: n = n['hijos'][lado]
    return n['claves'][lado]

def fusionar(n, i):
    h, s = n['hijos'][i], n['hijos'][i+1]
    h['claves'] += [n['claves'].pop(i)] + s['claves']
    h['hijos'] += s['hijos']
    n['hijos'].pop(i+1)

def rotar(n, i, d):
    h, s = n['hijos'][i], n['hijos'][i+d]
    if d == -1:
        h['claves'].insert(0, n['claves'][i-1]); n['claves'][i-1] = s['claves'].pop()
        if not s['hoja']: h['hijos'].insert(0, s['hijos'].pop())
    else:
        h['claves'].append(n['claves'][i]); n['claves'][i] = s['claves'].pop(0)
        if not s['hoja']: h['hijos'].append(s['hijos'].pop(0))

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
    i = next((j for j, c in enumerate(n['claves']) if c >= k), len(n['claves']))
    if i < len(n['claves']) and n['claves'][i] == k:
        if n['hoja']:
            n['claves'].pop(i)
        elif len(n['hijos'][i]['claves']) > min_c:
            p = extremo(n['hijos'][i], -1)
            n['claves'][i] = p; eliminar_en(n['hijos'][i], p, m)
        else:
            fusionar(n, i); eliminar_en(n['hijos'][i], k, m)
    else:
        if n['hoja']: return
        if len(n['hijos'][i]['claves']) <= min_c:
            rellenar(n, i, m)
            i = min(i, len(n['claves']))
        eliminar_en(n['hijos'][i], k, m)

def eliminar(arbol, k):
    eliminar_en(arbol['raiz'], k, arbol['m'])
    if not arbol['raiz']['claves'] and not arbol['raiz']['hoja']:
        arbol['raiz'] = arbol['raiz']['hijos'][0]

def mostrar(raiz):
    nivel = [raiz]
    num = 0
    while nivel:
        print(f"Nivel {num}: " + "   ".join(str(nd['claves']) for nd in nivel))
        nivel = [h for nd in nivel for h in nd['hijos']]
        num += 1

m = int(input("M = maximo de hijos: "))
arbol = {'m': m, 'raiz': nodo()}

while True:
    opc = input("\n[i] Insertar  [e] Eliminar  [s] Salir > ").strip().lower()
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
    else:
        print("Opcion invalida.")
