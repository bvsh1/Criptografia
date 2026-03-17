def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            ascii_base = ord('A') if caracter.isupper() else ord('a')
            resultado += chr((ord(caracter) - ascii_base + desplazamiento) % 26 + ascii_base)
        else:
            resultado += caracter
    return resultado

# 1. Pedimos la entrada en una sola línea
entrada = input('Ingresa el texto y el desplazamiento: ')

try:
    # 2. Separamos la entrada de derecha a izquierda por el último espacio
    # Esto divide el string en dos partes: el texto (con todo y espacios) y el número
    partes = entrada.rsplit(' ', 1)
    
    # 3. Limpiamos y asignamos las variables
    # strip('"\'') elimina las comillas dobles o simples que envuelven al texto
    texto_ingresado = partes[0].strip('"\'') 
    desplazamiento_ingresado = int(partes[1])
    
    # 4. Ejecutamos la función
    texto_final = cifrado_cesar(texto_ingresado, desplazamiento_ingresado)
    print(texto_final)

except (IndexError, ValueError):
    print("Error de formato. Asegúrate de seguir la estructura: \"texto\" número")