from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def ajustar_parametro(parametro_ingresado, tamano_requerido):
    """
    Ajusta una clave o IV al tamaño exacto requerido por el algoritmo.
    Si es menor, completa con bytes aleatorios. Si es mayor, recorta.
    """
    # Convertir a bytes si viene como string
    if isinstance(parametro_ingresado, str):
        param_bytes = parametro_ingresado.encode('utf-8')
    else:
        param_bytes = parametro_ingresado

    if len(param_bytes) < tamano_requerido:
        # Completar con bytes adicionales aleatorios
        faltantes = tamano_requerido - len(param_bytes)
        bytes_aleatorios = get_random_bytes(faltantes)
        print(f"[*] Faltan {faltantes} bytes. Agregando bytes aleatorios (hex): {bytes_aleatorios.hex()}")
        param_final = param_bytes + bytes_aleatorios
    elif len(param_bytes) > tamano_requerido:
        # Truncar a la longitud necesaria
        param_final = param_bytes[:tamano_requerido]
    else:
        param_final = param_bytes

    return param_final

def procesar_algoritmo(nombre, modulo_cifrado, texto, clave_str, iv_str, tamano_clave, tamano_iv):
    print(f"\n{'='*40}")
    print(f"=== PROCESANDO {nombre} ===")
    
    # 1. Ajuste de Clave e IV
    clave_final = ajustar_parametro(clave_str, tamano_clave)
    iv_final = ajustar_parametro(iv_str, tamano_iv)

    # Imprimir la clave final utilizada después de los ajustes
    print(f"Clave final utilizada (hex) : {clave_final.hex()}")
    print(f"IV final utilizado (hex)    : {iv_final.hex()}")

    bloque = modulo_cifrado.block_size

    try:
        # 2. Proceso de Cifrado (Modo CBC)
        # Se requiere "Padding" porque el modo CBC exige que el texto sea múltiplo del tamaño del bloque
        cipher_encrypt = modulo_cifrado.new(clave_final, modulo_cifrado.MODE_CBC, iv_final)
        texto_bytes = texto.encode('utf-8')
        texto_pad = pad(texto_bytes, bloque)
        texto_cifrado = cipher_encrypt.encrypt(texto_pad)
        
        print(f"Texto cifrado (hex)         : {texto_cifrado.hex()}")

        # 3. Proceso de Descifrado
        # Se debe instanciar un nuevo objeto para descifrar usando la misma clave e IV
        cipher_decrypt = modulo_cifrado.new(clave_final, modulo_cifrado.MODE_CBC, iv_final)
        texto_descifrado_pad = cipher_decrypt.decrypt(texto_cifrado)
        texto_descifrado = unpad(texto_descifrado_pad, bloque).decode('utf-8')
        
        print(f"Texto descifrado            : {texto_descifrado}")

        return texto_cifrado.hex()

    except Exception as e:
        print(f"Error al procesar {nombre}: {e}")
        return None


def main():
    print("--- Laboratorio Criptografía: DES, 3DES y AES-256 ---")
    
    # Solicitar datos al usuario
    clave_ingresada = input("Ingrese la Key base: ")
    iv_ingresado = input("Ingrese el Vector de Inicialización (IV) base: ")
    texto = input("Ingrese el texto a cifrar: ")

    resultados = {}

    # Procesar DES (Clave: 8 bytes, IV: 8 bytes)
    resultados["1"] = procesar_algoritmo("DES", DES, texto, clave_ingresada, iv_ingresado, 8, 8)

    # Procesar 3DES (Clave: 24 bytes, IV: 8 bytes)
    resultados["2"] = procesar_algoritmo("3DES", DES3, texto, clave_ingresada, iv_ingresado, 24, 8)

    # Procesar AES-256 (Clave: 32 bytes, IV: 16 bytes)
    resultados["3"] = procesar_algoritmo("AES-256", AES, texto, clave_ingresada, iv_ingresado, 32, 16)

    print(f"\n{'='*40}")
    print("=== VERIFICACIÓN DE HASH ===")
    while True:
        print("\nElija una opción para verificar (o 'q' para salir):")
        print("1. DES")
        print("2. 3DES")
        print("3. AES-256")
        opcion = input("Opción: ").strip()

        if opcion.lower() == 'q':
            break

        if opcion in resultados and resultados[opcion]:
            hash_ingresado = input("Ingrese el hash (hex) para comparar: ").strip()
            if hash_ingresado.lower() == resultados[opcion].lower():
                print("[✔] ¡El hash coincide con la encriptación!")
            else:
                print("[✘] El hash NO coincide.")
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()