import os
from groq import Groq
from ddgs import DDGS

client = Groq(api_key="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")

def buscar_web(pregunta, max_results=5):
    with DDGS() as ddgs:
        resultados = list(ddgs.text(pregunta, max_results=max_results))
    return "\n".join([r["body"] for r in resultados])

def agente_investigador(tema):
    print("🔍 Agente Investigador trabajando...")
    info1 = buscar_web(f"¿Qué es {tema}?")
    info2 = buscar_web(f"{tema} últimas tendencias 2025")
    info3 = buscar_web(f"{tema} aplicaciones prácticas ejemplos")
    resumen = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": "Eres un investigador. Resume y organiza la información en puntos clave."},
            {"role": "user", "content": f"Información 1:\n{info1}\n\nInformación 2:\n{info2}\n\nInformación 3:\n{info3}\n\nOrganiza todo sobre: {tema}"}
        ]
    )
    return resumen.choices[0].message.content

def agente_redactor(tema, investigacion):
    print("✍️ Agente Redactor trabajando...")
    informe = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": """Eres un redactor profesional. Genera un informe completo con:
- Introducción
- Puntos principales
- Aplicaciones prácticas
- Conclusión"""},
            {"role": "user", "content": f"Tema: {tema}\n\nInvestigación:\n{investigacion}"}
        ]
    )
    return informe.choices[0].message.content

def agente_corrector(informe):
    print("✅ Agente Corrector revisando...")
    correccion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": """Eres un editor profesional. Revisa y mejora:
- Ortografía y gramática
- Claridad y coherencia
- Estructura y fluidez
- Agrega ejemplos donde falten
Devuelve el informe completo corregido."""},
            {"role": "user", "content": f"Corrige y mejora este informe:\n\n{informe}"}
        ]
    )
    return correccion.choices[0].message.content

def guardar_informe(tema, informe):
    nombre = f"informe_{tema.replace(' ', '_')}.txt"
    with open(nombre, "w", encoding="utf-8") as f:
        f.write(informe)
    print(f"📄 Informe guardado como: {nombre}")

# Ejecutar
print("=== SISTEMA MULTI-AGENTE ===\n")
tema = input("¿Sobre qué tema quieres un informe? ")

investigacion = agente_investigador(tema)
print("\n✅ Investigación completada\n")

informe = agente_redactor(tema, investigacion)
print("\n✅ Redacción completada\n")

informe_corregido = agente_corrector(informe)
print("\n=== INFORME FINAL CORREGIDO ===")
print(informe_corregido)

guardar_informe(tema, informe_corregido)