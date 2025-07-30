import openai
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("asst_b3utMhxT6go7pIXB4s55uFpW")
backend_url = os.getenv("https://script.google.com/macros/s/AKfycbzGf9eb4pchk9c9k-5i-DBMxNXw8-Vo-iJq3QGJpKWwUs_fDiUwCF4NAY2EUXGjeYM_/exec")

# Función para iniciar una conversación
def iniciar_conversacion():
    thread = openai.beta.threads.create()
    return thread.id

# Enviar un mensaje al assistant
def enviar_mensaje(thread_id, mensaje):
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=mensaje
    )
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    return run

# Esperar la respuesta del assistant
def esperar_respuesta(thread_id, run_id):
    import time
    while True:
        run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == "completed":
            break
        print("Esperando respuesta del assistant...")
        time.sleep(2)

    mensajes = openai.beta.threads.messages.list(thread_id=thread_id)
    for msg in mensajes.data[::-1]:
        if msg.role == "assistant":
            print("🧠 Assistant:", msg.content[0].text.value)
            return msg.content[0].text.value

# Simulación de llamado al backend
def llamar_backend(payload):
    response = requests.post(backend_url, json=payload)
    if response.status_code == 200:
        print("✅ Presentación actualizada correctamente")
    else:
        print("❌ Error:", response.status_code, response.text)

# MAIN
if __name__ == "__main__":
    thread_id = iniciar_conversacion()
    mensaje_usuario = input("¿Qué proyecto quieres actualizar?: ")
    run = enviar_mensaje(thread_id, mensaje_usuario)
    respuesta = esperar_respuesta(thread_id, run.id)

    # Acá simulas un payload
    payload = {
        "proyecto": "Pollo Granjero CR",
        "avance": "Implementación de pagos completada",
        "imagenGanttUrl": "https://drive.google.com/uc?id=GANTT_ID",
        "imagenAvanceUrl": "https://drive.google.com/uc?id=AVANCE_ID"
    }

    llamar_backend(payload)
