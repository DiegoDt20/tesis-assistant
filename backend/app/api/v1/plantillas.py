"""Rutas HTTP para Plantillas — Sprint 2."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.plantilla import (
    PlantillaCreate,
    PlantillaDesdeDocumento,
    PlantillaResponse,
)
from app.services.plantilla_service import (
    crear_plantilla,
    crear_plantilla_desde_documento,
    listar_plantillas,
    obtener_plantilla,
    plantilla_a_response,
)

# Usuario demo hasta que implementemos auth completa
DEMO_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

router = APIRouter(prefix="/plantillas", tags=["plantillas"])


# ---------------------------------------------------------------------------
# GET /plantillas — listar todas las plantillas del usuario
# ---------------------------------------------------------------------------

@router.get("/", response_model=list[PlantillaResponse])
def listar(db: Session = Depends(get_db)):
    """Lista todas las plantillas del usuario actual."""
    plantillas = listar_plantillas(db, DEMO_USER_ID)
    return [plantilla_a_response(p) for p in plantillas]


# ---------------------------------------------------------------------------
# POST /plantillas — crear plantilla manualmente
# ---------------------------------------------------------------------------

@router.post("/", response_model=PlantillaResponse, status_code=status.HTTP_201_CREATED)
def crear(datos: PlantillaCreate, db: Session = Depends(get_db)):
    """Crea una nueva plantilla con secciones definidas manualmente."""
    plantilla = crear_plantilla(db, DEMO_USER_ID, datos)
    return plantilla_a_response(plantilla)


# ---------------------------------------------------------------------------
# POST /plantillas/desde-documento — crear plantilla desde documento analizado
# ---------------------------------------------------------------------------

@router.post(
    "/desde-documento",
    response_model=PlantillaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_desde_documento(
    datos: PlantillaDesdeDocumento,
    db: Session = Depends(get_db),
):
    """
    Genera una plantilla automáticamente a partir de las estructuras
    detectadas en un documento ya analizado.
    """
    try:
        plantilla = crear_plantilla_desde_documento(db, DEMO_USER_ID, datos)
        return plantilla_a_response(plantilla)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ---------------------------------------------------------------------------
# GET /plantillas/{id} — obtener una plantilla específica
# ---------------------------------------------------------------------------

@router.get("/{plantilla_id}", response_model=PlantillaResponse)
def obtener(plantilla_id: uuid.UUID, db: Session = Depends(get_db)):
    """Obtiene una plantilla por su ID."""
    plantilla = obtener_plantilla(db, plantilla_id, DEMO_USER_ID)
    if not plantilla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plantilla {plantilla_id} no encontrada.",
        )
    return plantilla_a_response(plantilla)