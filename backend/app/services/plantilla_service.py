"""Servicio de Plantillas — lógica de negocio."""
import uuid
from sqlalchemy.orm import Session
from app.models.plantilla import Plantilla
from app.models.estructura import Estructura
from app.schemas.plantilla import PlantillaCreate, PlantillaDesdeDocumento, SeccionSchema


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _estructura_a_seccion(est: Estructura, orden: int) -> dict:
    """Convierte un nodo Estructura del DB en un dict de sección."""
    # Convertir hijos recursivamente
    hijos = [
        _estructura_a_seccion(hijo, i + 1)
        for i, hijo in enumerate(
            sorted(est.hijos or [], key=lambda h: h.orden)
        )
    ]
    return {
        "id": str(est.id),
        "titulo": est.titulo,
        "obligatoria": True,   # por defecto toda sección detectada es obligatoria
        "orden": orden,
        "hijos": hijos,
    }


def _secciones_a_json(secciones: list[SeccionSchema]) -> list[dict]:
    """Convierte lista de SeccionSchema a lista de dicts para guardar en JSONB."""
    result = []
    for s in secciones:
        result.append({
            "id": s.id,
            "titulo": s.titulo,
            "obligatoria": s.obligatoria,
            "orden": s.orden,
            "hijos": _secciones_a_json(s.hijos),
        })
    return result


def _json_a_secciones(data: list[dict]) -> list[SeccionSchema]:
    """Convierte lista de dicts del JSONB a lista de SeccionSchema."""
    result = []
    for item in data:
        result.append(SeccionSchema(
            id=item["id"],
            titulo=item["titulo"],
            obligatoria=item.get("obligatoria", True),
            orden=item["orden"],
            hijos=_json_a_secciones(item.get("hijos", [])),
        ))
    return result


# ---------------------------------------------------------------------------
# Operaciones principales
# ---------------------------------------------------------------------------

def crear_plantilla(
    db: Session,
    usuario_id: uuid.UUID,
    datos: PlantillaCreate,
) -> Plantilla:
    """Crea una plantilla manualmente con las secciones proporcionadas."""
    plantilla = Plantilla(
        usuario_id=usuario_id,
        documento_id=datos.documento_id,
        titulo=datos.titulo,
        secciones_json=_secciones_a_json(datos.secciones),
    )
    db.add(plantilla)
    db.commit()
    db.refresh(plantilla)
    return plantilla


def crear_plantilla_desde_documento(
    db: Session,
    usuario_id: uuid.UUID,
    datos: PlantillaDesdeDocumento,
) -> Plantilla:
    """
    Genera una plantilla automáticamente a partir de las estructuras
    detectadas de un documento ya analizado.
    """
    # Obtener solo las secciones raíz (sin parent) del documento
    secciones_raiz = (
        db.query(Estructura)
        .filter(
            Estructura.documento_id == datos.documento_id,
            Estructura.parent_id == None,
        )
        .order_by(Estructura.orden)
        .all()
    )

    if not secciones_raiz:
        raise ValueError(
            f"El documento {datos.documento_id} no tiene estructuras detectadas."
        )

    # Convertir estructuras a formato JSON de secciones
    secciones_json = [
        _estructura_a_seccion(est, i + 1)
        for i, est in enumerate(secciones_raiz)
    ]

    plantilla = Plantilla(
        usuario_id=usuario_id,
        documento_id=datos.documento_id,
        titulo=datos.titulo,
        secciones_json=secciones_json,
    )
    db.add(plantilla)
    db.commit()
    db.refresh(plantilla)
    return plantilla


def listar_plantillas(db: Session, usuario_id: uuid.UUID) -> list[Plantilla]:
    """Lista todas las plantillas del usuario."""
    return (
        db.query(Plantilla)
        .filter(Plantilla.usuario_id == usuario_id)
        .order_by(Plantilla.fecha_creacion.desc())
        .all()
    )


def obtener_plantilla(
    db: Session,
    plantilla_id: uuid.UUID,
    usuario_id: uuid.UUID,
) -> Plantilla | None:
    """Obtiene una plantilla por ID verificando que pertenece al usuario."""
    return (
        db.query(Plantilla)
        .filter(
            Plantilla.id == plantilla_id,
            Plantilla.usuario_id == usuario_id,
        )
        .first()
    )


def plantilla_a_response(plantilla: Plantilla) -> dict:
    """Convierte una Plantilla ORM a dict listo para la respuesta."""
    return {
        "id": plantilla.id,
        "usuario_id": plantilla.usuario_id,
        "documento_id": plantilla.documento_id,
        "titulo": plantilla.titulo,
        "secciones": _json_a_secciones(plantilla.secciones_json),
        "fecha_creacion": plantilla.fecha_creacion,
    }