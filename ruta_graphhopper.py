import requests
import os
from dotenv import load_dotenv

# 1. Cargar variables de entorno desde el archivo .env
load_dotenv()
# Extraemos la llave de GraphHopper de forma segura
api_key = os.getenv("GRAPHHOPPER_API_KEY")

def main():
    if not api_key:
        print("Error: API key ausente. Verifique su archivo .env.")
        return

    while True:
        origen = input("Ingrese Ciudad Origen (o 'q' para salir): ")
        if origen.lower() == 'q':
            print("Saliendo del programa...")
            break
        
        destino = input("Ingrese Ciudad Destino (o 'q' para salir): ")
        if destino.lower() == 'q':
            print("Saliendo del programa...")
            break

        try:
            # 2. Geocoding: Obtener latitud y longitud de Origen
            url_origen = f"https://graphhopper.com/api/1/geocode?q={origen}&key={api_key}"
            res_origen = requests.get(url_origen, timeout=10)
            
            if res_origen.status_code != 200 or not res_origen.json().get('hits'):
                print(f"Error HTTP {res_origen.status_code}: Origen inválido o no encontrado.")
                continue
                
            lat_origen = res_origen.json()['hits'][0]['point']['lat']
            lng_origen = res_origen.json()['hits'][0]['point']['lng']

            # 3. Geocoding: Obtener latitud y longitud de Destino
            url_destino = f"https://graphhopper.com/api/1/geocode?q={destino}&key={api_key}"
            res_destino = requests.get(url_destino, timeout=10)
            
            if res_destino.status_code != 200 or not res_destino.json().get('hits'):
                print(f"Error HTTP {res_destino.status_code}: Destino inválido o no encontrado.")
                continue

            lat_destino = res_destino.json()['hits'][0]['point']['lat']
            lng_destino = res_destino.json()['hits'][0]['point']['lng']

            # 4. Routing: Calcular la Ruta entre ambas coordenadas
            # Se usa locale=es para que las instrucciones salgan en español
            url_ruta = f"https://graphhopper.com/api/1/route?point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&vehicle=car&locale=es&key={api_key}"
            res_ruta = requests.get(url_ruta, timeout=10)

            if res_ruta.status_code == 200:
                datos_ruta = res_ruta.json()
                
                # 5. Extraer datos y realizar cálculos
                if 'paths' in datos_ruta and len(datos_ruta['paths']) > 0:
                    ruta = datos_ruta['paths'][0]
                    distancia_m = ruta['distance']
                    duracion_ms = ruta['time'] # GraphHopper usa milisegundos
                    instrucciones = ruta.get('instructions', [])

                    distancia_km = distancia_m / 1000
                    duracion_s = duracion_ms / 1000
                    horas = int(duracion_s // 3600)
                    minutos = int((duracion_s % 3600) // 60)
                    segundos = int(duracion_s % 60)
                    litros = distancia_km / 12.0  

                    print("\n" + "="*60)
                    print(f"Viaje desde {origen.title()} hasta {destino.title()}")
                    print(f"Distancia: {distancia_km:.2f} kilómetros")
                    print(f"Duración del viaje: {horas:02d} horas, {minutos:02d} minutos y {segundos:02d} segundos")
                    print(f"Combustible requerido: {litros:.2f} litros")
                    print("="*60 + "\n")
                    
                    print("--- Narrativa del viaje ---")
                    for paso in instrucciones:
                        texto = paso.get('text', '')
                        dist_paso_km = paso.get('distance', 0) / 1000
                        print(f"{texto} ({dist_paso_km:.2f} km)")
                    print("="*60 + "\n")
                else:
                    print("Error: No se pudo trazar una ruta válida entre estas ciudades.")
            else:
                 print(f"Error HTTP en ruta: {res_ruta.status_code}")

        # 6. Control de errores de red
        except requests.exceptions.RequestException as e:
            print(f"Error de red o conexión: {e}\n")
        except Exception as e:
            print(f"Error inesperado: {e}\n")

if __name__ == "__main__":
    main()