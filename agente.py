import os
from groq import Groq
from ddgs import DDGS

client = Groq(api_key="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")

def buscar_web(pregunta):
    with DDGS() as ddgs:
        resultados = list(ddgs.text(pregunta, max_results=3))
    return "\n".join([r["body"] for r in resultados])

pregunta = "¿Cómo se diseña un curso universitario de IA?"
print("Buscando en internet...")
info = buscar_web(pregunta)

respuesta = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "Eres un asistente experto. Usa la información proporcionada para responder."},
        {"role": "user", "content": f"Información encontrada:\n{info}\n\nPregunta: {pregunta}"}
    ]
)

print("\n=== RESPUESTA DEL AGENTE ===")
print(respuesta.choices[0].message.content)