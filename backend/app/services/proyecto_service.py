"""Servicio de Proyectos — lógica de negocio."""
import uuid
from sqlalchemy.orm import Session
from app.models.proyecto import Proyecto
from app.models.plantilla import Plantilla
from app.schemas.proyecto import ProyectoCreate, RespuestaCreate


# ---------------------------------------------------------------------------
# Operaciones principales
# ---------------------------------------------------------------------------

def crear_proyecto(
    db: Session,
    usuario_id: uuid.UUID,
    datos: ProyectoCreate,
) -> Proyecto:
    """Crea un nuevo proyecto asociado a una plantilla."""
    # Verificar que la plantilla existe
    plantilla = db.query(Plantilla).filter(
        Plantilla.id == datos.plantilla_id
    ).first()
    if not plantilla:
        raise ValueError(f"Plantilla {datos.plantilla_id} no encontrada.")

    proyecto = Proyecto(
        usuario_id=usuario_id,
        plantilla_id=datos.plantilla_id,
        titulo=datos.titulo,
        estado="borrador",
        respuestas_json={},
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


def guardar_respuesta(
    db: Session,
    usuario_id: uuid.UUID,
    proyecto_id: uuid.UUID,
    datos: RespuestaCreate,
) -> Proyecto:
    """Guarda la respuesta del usuario para una sección del proyecto."""
    proyecto = obtener_proyecto(db, proyecto_id, usuario_id)
    if not proyecto:
        raise ValueError(f"Proyecto {proyecto_id} no encontrado.")

    # Actualizar el JSON de respuestas
    respuestas = dict(proyecto.respuestas_json)
    respuestas[datos.seccion_id] = datos.respuesta
    proyecto.respuestas_json = respuestas

    # Cambiar estado a en_progreso si tenía respuestas
    if proyecto.estado == "borrador":
        proyecto.estado = "en_progreso"

    db.commit()
    db.refresh(proyecto)
    return proyecto


def listar_proyectos(
    db: Session,
    usuario_id: uuid.UUID,
) -> list[Proyecto]:
    """Lista todos los proyectos del usuario."""
    return (
        db.query(Proyecto)
        .filter(Proyecto.usuario_id == usuario_id)
        .order_by(Proyecto.fecha_creacion.desc())
        .all()
    )


def obtener_proyecto(
    db: Session,
    proyecto_id: uuid.UUID,
    usuario_id: uuid.UUID,
) -> Proyecto | None:
    """Obtiene un proyecto verificando que pertenece al usuario."""
    return (
        db.query(Proyecto)
        .filter(
            Proyecto.id == proyecto_id,
            Proyecto.usuario_id == usuario_id,
        )
        .first()
    )


def proyecto_a_response(proyecto: Proyecto) -> dict:
    """Convierte un Proyecto ORM a dict listo para la respuesta."""
    return {
        "id": proyecto.id,
        "usuario_id": proyecto.usuario_id,
        "plantilla_id": proyecto.plantilla_id,
        "titulo": proyecto.titulo,
        "estado": proyecto.estado,
        "respuestas": proyecto.respuestas_json,
        "fecha_creacion": proyecto.fecha_creacion,
        "fecha_actualiz": proyecto.fecha_actualiz,
    }