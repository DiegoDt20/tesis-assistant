"""Rutas de autenticación — registro y login."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from app.database.session import get_db
from app.models.usuario import Usuario
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    correo: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: str
    nombre: str


# ---------------------------------------------------------------------------
# POST /auth/register — crear cuenta nueva
# ---------------------------------------------------------------------------

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(datos: RegisterRequest, db: Session = Depends(get_db)):
    """Crea una cuenta nueva y devuelve el token de acceso."""
    # Verificar que el correo no esté en uso
    existente = db.query(Usuario).filter(
        Usuario.correo == datos.correo
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta con ese correo.",
        )

    # Crear el usuario
    usuario = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        password_hash=hash_password(datos.password),
        rol="estudiante",
        activo=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Generar token
    token = create_access_token({"sub": str(usuario.id)})

    return TokenResponse(
        access_token=token,
        usuario_id=str(usuario.id),
        nombre=usuario.nombre,
    )


# ---------------------------------------------------------------------------
# POST /auth/login — iniciar sesión
# ---------------------------------------------------------------------------

@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    """Inicia sesión y devuelve el token de acceso."""
    # Buscar el usuario
    usuario = db.query(Usuario).filter(
        Usuario.correo == datos.correo,
        Usuario.activo == True,
    ).first()

    if not usuario or not verify_password(datos.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    # Generar token
    token = create_access_token({"sub": str(usuario.id)})

    return TokenResponse(
        access_token=token,
        usuario_id=str(usuario.id),
        nombre=usuario.nombre,
    )


# ---------------------------------------------------------------------------
# GET /auth/me — obtener usuario actual
# ---------------------------------------------------------------------------

@router.get("/me")
def me(db: Session = Depends(get_db)):
    """Endpoint de prueba — implementar con auth completa."""
    return {"mensaje": "Auth funcionando"}