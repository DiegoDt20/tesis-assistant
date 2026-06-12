"""Servicio de Generación — usa OpenAI para redactar secciones académicas."""
import os
from openai import OpenAI
from app.models.proyecto import Proyecto
from app.models.plantilla import Plantilla


# ---------------------------------------------------------------------------
# Cliente OpenAI (se inicializa con la key del .env)
# ---------------------------------------------------------------------------

def get_cliente() -> OpenAI:
    """Crea el cliente OpenAI usando la API key del config."""
    from app.core.config import get_settings
    settings = get_settings()
    api_key = settings.openai_api_key
    if not api_key:
        raise ValueError("OPENAI_API_KEY no está configurada en el .env")
    return OpenAI(api_key=api_key)

# ---------------------------------------------------------------------------
# Constructor de prompts
# ---------------------------------------------------------------------------

def construir_prompt(
    seccion_id: str,
    seccion_titulo: str,
    respuestas: dict,
    titulo_proyecto: str,
) -> str:
    """
    Construye el prompt para generar el contenido de una sección.
    Incluye el título del proyecto y todas las respuestas disponibles
    para dar contexto a la IA.
    """
    # Formatear las respuestas como contexto
    contexto = "\n".join([
        f"- {k}: {v}"
        for k, v in respuestas.items()
        if v.strip()
    ])

    return f"""Eres un asistente académico experto en redacción de proyectos de investigación.

Proyecto: {titulo_proyecto}

Información proporcionada por el investigador:
{contexto if contexto else "Sin información adicional aún."}

Tarea: Redacta el contenido de la sección "{seccion_titulo}" para este proyecto de investigación.

Instrucciones:
- Usa un lenguaje académico formal
- El texto debe tener entre 150 y 300 palabras
- Basa el contenido en la información proporcionada
- Si falta información, usa estructura académica estándar
- No incluyas el título de la sección en tu respuesta
- Responde directamente con el texto de la sección

Redacta la sección ahora:"""


# ---------------------------------------------------------------------------
# Función principal de generación
# ---------------------------------------------------------------------------

def generar_seccion(
    proyecto: Proyecto,
    plantilla: Plantilla,
    seccion_id: str,
) -> str:
    """
    Genera el contenido de una sección usando OpenAI.
    
    Busca la sección en la plantilla, construye el prompt con las
    respuestas del proyecto y llama a la API de OpenAI.
    """
    # Buscar el título de la sección en la plantilla
    seccion_titulo = seccion_id  # fallback
    for sec in plantilla.secciones_json:
        if sec.get("id") == seccion_id:
            seccion_titulo = sec.get("titulo", seccion_id)
            break

    # Construir el prompt
    prompt = construir_prompt(
        seccion_id=seccion_id,
        seccion_titulo=seccion_titulo,
        respuestas=proyecto.respuestas_json,
        titulo_proyecto=proyecto.titulo,
    )

    # Llamar a OpenAI
    cliente = get_cliente()
    respuesta = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres un experto en redacción académica universitaria."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500,
        temperature=0.7,
    )

    return respuesta.choices[0].message.content.strip()


def generar_todas_las_secciones(
    proyecto: Proyecto,
    plantilla: Plantilla,
) -> dict[str, str]:
    """
    Genera el contenido de todas las secciones de la plantilla.
    Devuelve un dict con seccion_id → contenido generado.
    """
    contenidos = {}
    for seccion in plantilla.secciones_json:
        seccion_id = seccion.get("id", "")
        if seccion_id:
            contenidos[seccion_id] = generar_seccion(
                proyecto, plantilla, seccion_id
            )
    return contenidos