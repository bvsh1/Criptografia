import sys
from scapy.all import rdpcap, ICMP, Raw

def descifrar_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            resultado += chr((ord(char) - ascii_offset - desplazamiento) % 26 + ascii_offset)
        else:
            resultado += char
    return resultado

def evaluar_probabilidad(texto):
    # Diccionario amplio: conectores comunes del español + términos técnicos
    diccionario_espanol = {
        # Artículos y conectores comunes
        "el", "la", "los", "las", "un", "una", "unos", "unas",
        "y", "o", "pero", "si", "no", "ni",
        "en", "de", "a", "con", "por", "para", "sin", "sobre", "hasta",
        "que", "como", "cuando", "donde", "quien", "del", "al",
        "es", "son", "fue", "ser", "estar", "este", "esta", "eso",
        # Términos de informática y redes
        "red", "redes", "seguridad", "criptografia", "sistema", "sistemas",
        "datos", "informacion", "mensaje", "texto", "cifrado", "descifrado",
        "usuario", "clave", "ataque", "protocolo", "paquete", "internet", "mitm"
    }
    
    # Separamos el texto en palabras individuales
    palabras_texto = texto.lower().split()
    puntuacion = 0
    
    for palabra in palabras_texto:
        if palabra in diccionario_espanol:
            # Damos más peso a las palabras largas (3 o más letras). 
            # Las letras cortas suman menos para no gatillar falsos positivos solas.
            if len(palabra) >= 3:
                puntuacion += 2
            else:
                puntuacion += 1
                
    # Requerimos una puntuación mínima de 3 para considerarlo válido. 
    # Ej: "en" (1 punto) + "redes" (2 puntos) = 3 puntos. 
    # La frase "criptografia y seguridad en redes" suma 8 puntos en total.
    return puntuacion >= 3

def extraer_texto(archivo_pcap):
    paquetes = rdpcap(archivo_pcap)
    texto = ""
    for pkt in paquetes:
        if pkt.haslayer(ICMP) and pkt[ICMP].type == 8 and pkt.haslayer(Raw):
            try:
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
            print(f"\033[92m{i:2d} {texto_claro}\033[0m")
        else:
            print(f"{i:2d} {texto_claro}")