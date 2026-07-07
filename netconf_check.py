from ncclient import manager
import os
from dotenv import load_dotenv

# Cargar variables seguras desde el archivo oculto .env
load_dotenv()

ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USER = os.getenv("ROUTER_USER")
ROUTER_PASS = os.getenv("ROUTER_PASS")
ROUTER_PORT = 830

def main():
    print("="*60)
    print(" Conexión NETCONF - CSR1000v")
    print(" Integrantes: Vicente Comigual y Gabriel Lazcano")
    print("="*60)
    
    if not ROUTER_IP or not ROUTER_USER or not ROUTER_PASS:
        print("[!] Error: Faltan credenciales en el archivo .env")
        return

    try:
        print(f"[*] Conectando a {ROUTER_IP} por NETCONF...")
        
        # Conexión usando las variables seguras y librería ncclient
        with manager.connect(host=ROUTER_IP, port=ROUTER_PORT, username=ROUTER_USER, password=ROUTER_PASS, hostkey_verify=False) as m:
            print("[*] Conexión NETCONF establecida exitosamente.\n")
            
            # Consulta 1: Capabilities del router
            print("--- Capabilities del dispositivo (Muestra parcial) ---")
            for cap in list(m.server_capabilities)[:5]: 
                print(cap)
            print("...\n")
            
            # Consulta 2: Obtener running-config y guardarlo en formato XML
            print("[*] Obteniendo configuración (running-config)...")
            config = m.get_config(source='running')
            
            # Guardamos la salida en el archivo requerido
            with open("salida.xml", "w") as f:
                f.write(config.xml)
                
            print("[*] Configuración guardada exitosamente en el archivo 'salida.xml'.")
            
    except Exception as e:
        print(f"[!] Error al conectar por NETCONF: {e}")

if __name__ == "__main__":
    main()