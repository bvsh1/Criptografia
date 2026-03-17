import sys
from scapy.all import rdpcap, ICMP, Raw

def descifrar_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            # Se resta el desplazamiento en lugar de sumarlo
            resultado += chr((ord(char) - ascii_offset - desplazamiento) % 26 + ascii_offset)
        else:
            resultado += char
    return resultado

def evaluar_probabilidad(texto):
    # Quitamos conectores de una letra (" a ", " y ") para evitar falsos positivos
    # y nos enfocamos en palabras de 2 o más letras comunes o del contexto.
    palabras_clave = [" el ", " la ", " en ", " de ", "criptografia", "seguridad", "redes"]
    
    # Contamos cuántas coincidencias hay en el texto
    coincidencias = sum(1 for palabra in palabras_clave if palabra in texto.lower())
    
    # Exigimos que encuentre al menos una palabra larga muy específica, o varias cortas
    if any(p in texto.lower() for p in ["criptografia", "seguridad", "redes"]) or coincidencias >= 2:
        return True
    return False

def extraer_texto(archivo_pcap):
    paquetes = rdpcap(archivo_pcap)
    texto = ""
    for pkt in paquetes:
        # Filtrar paquetes ICMP tipo 8 (Echo Request) que tengan capa Raw (Payload)
        if pkt.haslayer(ICMP) and pkt[ICMP].type == 8 and pkt.haslayer(Raw):
            try:
                # Extraemos el primer byte del payload
                char = pkt[Raw].load[0:1].decode('utf-8')
                texto += char
            except Exception:
                pass
    return texto

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 readv2.py <archivo.pcapng>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    texto_interceptado = extraer_texto(pcap_file)
    
    for i in range(1, 26):
        texto_claro = descifrar_cesar(texto_interceptado, i)
        if evaluar_probabilidad(texto_claro):
            # Imprimir en verde si el texto contiene palabras en español
            print(f"\033[92m{i:2d} {texto_claro}\033[0m")
        else:
            print(f"{i:2d} {texto_claro}")