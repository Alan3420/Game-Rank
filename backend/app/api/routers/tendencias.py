from fastapi import APIRouter, Depends, Request

from app.api.limites import limiter
from app.api.respuestas import responder
from app.api.seguridad import id_usuario_actual
from app.services.tendencias_service import obtener_tendencias

router = APIRouter(prefix="/tendencias", tags=["Tendencias"])


@router.get("/")
@limiter.limit("60 per minute")
def tendencias(request: Request, id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder(obtener_tendencias(), 200)
    except Exception:
        return responder({"message": "Error interno del servidor"}, 500)
