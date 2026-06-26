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

def necesita_busqueda(pregunta, historial):
    """El modelo decide si necesita buscar en internet"""
    mensajes = [
        {"role": "system", "content": """Decides si una pregunta necesita búsqueda en internet.
Responde SOLO con 'SI' o 'NO'.
- SI: preguntas sobre hechos actuales, noticias, datos específicos
- NO: preguntas de seguimiento, opiniones, explicaciones de algo ya conversado"""},
        {"role": "user", "content": f"Historial reciente: {str(historial[-3:])}\nPregunta: {pregunta}"}
    ]
    respuesta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=mensajes,
        max_tokens=5
    )
    return "SI" in respuesta.choices[0].message.content.upper()

historial = cargar_memoria()
print("=== AGENTE INTELIGENTE CON MEMORIA ===")
print("Escribe 'salir' para terminar\n")

while True:
    pregunta = input("Tú: ")
    if pregunta.lower() == "salir":
        break

    # El agente decide si buscar
    if necesita_busqueda(pregunta, historial):
        print("🔍 Buscando en internet...")
        info = f"Información encontrada:\n{buscar_web(pregunta)}\n\nPregunta: {pregunta}"
    else:
        print("🧠 Usando memoria...")
        info = pregunta

    historial.append({"role": "user", "content": info})

    respuesta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Eres un asistente experto que recuerda toda la conversación."}
        ] + historial
    )

    respuesta_texto = respuesta.choices[0].message.content
    historial.append({"role": "assistant", "content": respuesta_texto})
    guardar_memoria(historial)

    print(f"\nAgente: {respuesta_texto}\n")