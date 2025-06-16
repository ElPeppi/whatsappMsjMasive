import requests
import csv
import time
import os

# --- CONFIGURACIÓN ---
# Tu token de acceso de la API de Meta. ¡Mantenlo seguro!
# Es una buena práctica usar variables de entorno para no escribirlo aquí.
ACCESS_TOKEN = 'EAASuEjYQq6UBO5ORkV36kdMF43phJWD6if2bfIIPxz57S67BDL9YIMQaiXvGV1JgAxysOk3W49znvmlvsp9KTdvZAOusKcWtlS4wlfyve69mzqECIDkCsZBbVsGXPMWm2FZCvP2xS9SdiVSNCxZBLOZBejiXDRfO24KR81S8cmvTh5QLyLfQsOXWA0XG1c2VmZCAZDZD'

# El ID de tu número de teléfono de WhatsApp Business
PHONE_NUMBER_ID = '733407986512052'

# El nombre del archivo CSV que creaste
CSV_FILENAME = 'contactos.csv'

# El nombre EXACTO de la plantilla que creaste en Meta
TEMPLATE_NAME = 'derechotransitovigencia2025'

# La URL de la API de Graph
API_URL = f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages'

# Cabeceras de la petición (Headers)
HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def enviar_mensaje_whatsapp(nombre_destinatario, numero_destinatario):
    """
    Envía un mensaje de WhatsApp usando una plantilla a un destinatario.
    """
    # El cuerpo de la petición cambia para incluir los parámetros de la plantilla
    data_payload = {
        "messaging_product": "whatsapp",
        "to": numero_destinatario,
        "type": "template",
        "template": {
            "name": TEMPLATE_NAME,
            "language": {
                "code": "es_CO"  # Asumiendo que tu plantilla está en español
            }
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data_payload)
        response.raise_for_status()  # Esto generará un error si la petición falla (status code 4xx o 5xx)
        
        print(f"Éxito: Mensaje enviado a {nombre_destinatario} ({numero_destinatario}).")
        print(f"Respuesta de la API: {response.json()}")
        return True

    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP al enviar a {nombre_destinatario}: {err}")
        print(f"Respuesta de la API: {err.response.text}")
        return False
    except Exception as err:
        print(f"Ocurrió otro error al enviar a {nombre_destinatario}: {err}")
        return False

# --- LÓGICA PRINCIPAL ---
def procesar_csv_y_enviar():
    print("Iniciando proceso de envío masivo...")
    try:
        with open(CSV_FILENAME, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Obtenemos el nombre y el celular de cada fila, quitando espacios extra
                nombre_completo = row.get('nombre completo', '').strip()
                celular = row.get('celular', '').strip()

                if nombre_completo and celular:
                    enviar_mensaje_whatsapp(nombre_completo, celular)
                    
                    # Pausa de 2 segundos entre cada mensaje para no saturar la API
                    print("...esperando 2 segundos...")
                    time.sleep(2)
                else:
                    print(f"Advertencia: Fila omitida por datos incompletos: {row}")
        
        print("¡Proceso de envío masivo completado!")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{CSV_FILENAME}'. Asegúrate de que esté en la misma carpeta que el script.")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante el proceso: {e}")

# Ejecutar la función principal
if __name__ == "__main__":
    procesar_csv_y_enviar()