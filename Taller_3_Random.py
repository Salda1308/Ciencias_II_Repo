

M1 = 1_000_000_007  
M2 = 998_244_353      
A  = 6_271            
B  = 3_571           

semilla = int(input("Ingresa una semilla: "))

p = semilla % M1 or 1               
q = (semilla * 1_000_003 + 1) % M2  
def generar():
    global p, q
    
    p = (A * p + q) % M1
   
    q = (B * q + p * p) % M2
    
    return (p + q) % 101


print("\nPresiona Enter para generar un número entre 0 y 100.")
print("'q' para salir.\n")

generados = 0
aparecidos = set()

while True:
    entrada = input("> ")
    if entrada.strip().lower() == "q":
        break
    numero = generar()
    generados += 1
    aparecidos.add(numero)
    print(f"  Número: {numero}  (distintos hasta ahora: {len(aparecidos)}/{generados})")
