from fastapi import APIRouter

from app.core.config import VERSION

# Rutas para comprobar que la API funciona (no son de negocio)
router = APIRouter(tags=["health"])


@router.get("/health", summary="Estado de la API")
def health():
    return {"status": "ok"}


@router.get("/version", summary="Versión de la API")
def version():
    return {"version": VERSION}


@router.get("/ping", summary="Ping")
def ping():
    return {"message": "pong"}
