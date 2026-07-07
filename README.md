# Evaluación Transversal - Redes Programables
**Integrantes:** Vicente Comigual y Gabriel Lazcano

## Objetivo del Proyecto
Este repositorio contiene la evidencia práctica de la automatización y gestión de infraestructura de red mediante Python, Ansible y llamadas API (RESTCONF/NETCONF) orientadas a un router Cisco CSR1000v.

## Prerrequisitos e Instalación
Para ejecutar estos scripts, se requiere Python 3 y las librerías listadas en el archivo de requerimientos.
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Renombrar el archivo `.env.example` a `.env` y colocar las credenciales reales de su entorno.

## Módulos y Ejecución
* **Ítem 3 (Geolocalización):** Ejecutar `python3 ruta_graphhopper.py`. Consume la API de GraphHopper.
* **Ítem 4 (Gestión SQLite/Flask):** Ejecutar `python3 claves_grupo.py`. Despliega una API REST en el puerto 5000 utilizando `hashlib` (SHA-256) para encriptar contraseñas de forma segura.
* **Ítem 5 (NETCONF):** Ejecutar `python3 netconf_check.py`. Requiere el puerto 830 habilitado. Extrae capabilities y el running-config en XML.
* **Ítem 6 (RESTCONF):** Se adjunta la colección `coleccion_restconf.json` para Postman, que demuestra la consulta de interfaces y creación de una Loopback.
* **Ítem 7 (Ansible):** Ejecutar `ansible-playbook -i hosts playbook_servicio.yaml`. **Nota de Idempotencia:** Se utilizó el módulo `ios_config`, el cual es idempotente porque verifica si la configuración SNMP ya existe antes de aplicarla, permitiendo múltiples ejecuciones sin romper la red.
* **Ítem 8 (Netmiko):** Ejecutar `python3 config_netmiko.py`. Emula conexión SSH en el puerto 22 para inyectar configuraciones por CLI.
* **Ítem 9 (SD-WAN):** Se adjunta la colección `coleccion_sdwan.json` de Postman interactuando con el Sandbox de Cisco.
