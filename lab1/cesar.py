import sys

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            # Determinar si es mayúscula o minúscula para el offset ASCII
            ascii_offset = 65 if char.isupper() else 97
            # Aplicar desplazamiento cíclico
            nuevo_char = chr((ord(char) - ascii_offset + desplazamiento) % 26 + ascii_offset)
            resultado += nuevo_char
        else:
            # Mantener espacios y otros caracteres especiales
            resultado += char
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py <texto> <desplazamiento>")
        sys.exit(1)

    texto = sys.argv[1]
    desplazamiento = int(sys.argv[2])
    print(cifrado_cesar(texto, desplazamiento))