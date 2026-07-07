from netmiko import ConnectHandler
import os
from dotenv import load_dotenv

# Buenas prácticas: Variables separadas y carga segura desde .env
load_dotenv()

router_csr = {
    'device_type': 'cisco_ios',
    'host': os.getenv("ROUTER_IP", "192.168.100.98"),
    'username': os.getenv("ROUTER_USER", "cisco"),
    'password': os.getenv("ROUTER_PASS", "cisco123!"),
    'port': 22,
    'global_delay_factor': 2
}

def main():
    print("="*60)
    print(" Configuración con Netmiko - CSR1000v")
    print(" Integrantes: Vicente Comigual y Gabriel Lazcano")
    print("="*60)

    try:
        # Conexión SSH
        print("[*] Estableciendo conexión SSH con Netmiko...")
        conexion = ConnectHandler(**router_csr)
        print("[*] ¡Conexión exitosa al router!")

        # Comandos de configuración a enviar
        comandos_config = [
            'interface GigabitEthernet1',
            'description INTERFAZ DE GESTION - COMIGUAL Y LAZCANO',
            'interface Loopback100',
            'description LOOPBACK CREADA CON NETMIKO',
            'ip address 100.100.100.100 255.255.255.255',
            'no shutdown'
        ]

        # Enviar configuraciones
        print("[*] Enviando configuraciones (send_config_set)...")
        salida_config = conexion.send_config_set(comandos_config)
        print("[*] Configuraciones aplicadas correctamente.")

        # Ejecutar comandos show para validación
        print("[*] Validando configuración aplicada...")
        validacion = conexion.send_command('show ip interface brief')
        
        # Guardar la validación en un archivo de texto como pide la rúbrica
        with open("07_netmiko_validacion.txt", "w") as archivo:
            archivo.write("VALIDACION DE INTERFACES - VICENTE Y GABRIEL\n")
            archivo.write("="*50 + "\n")
            archivo.write(validacion)

        print("[*] Validación guardada en '07_netmiko_validacion.txt'.")
        print("\n--- Vista previa de la validación ---")
        print(validacion)

        # Buenas prácticas: Cierre de conexión
        conexion.disconnect()
        print("\n[*] Conexión cerrada de forma segura.")

    except Exception as e:
        print(f"[!] Ocurrió un error en la ejecución: {e}")

if __name__ == "__main__":
    main()