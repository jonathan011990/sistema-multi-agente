import os
import json
from groq import Groq
from ddgs import DDGS

client = Groq(api_key="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")

ARCHIVO_MEMORIA = "memoria.json"

def cargar_memoria():
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_memoria(historial):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def buscar_web(pregunta):
    with DDGS() as ddgs:
        resultados = list(ddgs.text(pregunta, max_results=5))
    return "\n".join([r["body"] for r in resultados])

# Cargar historial previo
historial = cargar_memoria()
print("=== AGENTE CON MEMORIA ===")
print("Escribe 'salir' para terminar\n")

while True:
    pregunta = input("Tú: ")
    if pregunta.lower() == "salir":
        break

    print("Buscando en internet...")
    info = buscar_web(pregunta)

    historial.append({
        "role": "user",
        "content": f"Información encontrada:\n{info}\n\nPregunta: {pregunta}"
    })

    respuesta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Eres un asistente experto que recuerda conversaciones anteriores."}
        ] + historial
    )

    respuesta_texto = respuesta.choices[0].message.content

    historial.append({
        "role": "assistant",
        "content": respuesta_texto
    })

    guardar_memoria(historial)

    print(f"\nAgente: {respuesta_texto}\n")