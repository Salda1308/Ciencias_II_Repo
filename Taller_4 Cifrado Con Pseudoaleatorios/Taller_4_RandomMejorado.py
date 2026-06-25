

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


N = 100000000
conteo = [0] * 101  

for _ in range(N):
    conteo[generar()] += 1

print(f"\nResultados tras {N} iteraciones")
print(f"{'Número':>8} {'Conteo':>8} {'Probabilidad':>14}")
print("-" * 34)
for num, cnt in enumerate(conteo):
    prob = cnt / N
    print(f"{num:>8} {cnt:>8} {prob:>14.4f}")

print("-" * 34)
print(f"{'Total':>8} {N:>8} {'1.0000':>14}")
