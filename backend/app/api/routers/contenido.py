from fastapi import APIRouter, Depends, Request

from app.api.limites import limiter
from app.api.respuestas import entero_de_query, responder, texto_de_query
from app.api.seguridad import id_usuario_actual
from app.services.game_services import (
    obtener_detalle_del_videojuego,
    obtener_juegos_del_catalogo,
    obtener_proximos_lanzamientos,
    obtener_video_aleatorio,
    obtener_juegos_filtrados,
    obtener_saga,
    obtener_adicciones_del_juego,
    obtener_logros_del_juego
)

router = APIRouter(prefix="/content", tags=["Juegos (RAWG)"])


@router.get("/overview/{game_id}")
def detalle_de_juego(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder(obtener_detalle_del_videojuego(id_juego=game_id), 200)
    except Exception:
        return responder({"message": "Error al obtener los detalles del juego"}, 500)


@router.get("/release")
def proximos_lanzamientos(request: Request, id_usuario: str = Depends(id_usuario_actual)):
    try:
        pagina = entero_de_query(request, "page", 1)
        por_pagina = min(entero_de_query(request, "per_page", 10), 40)
        return responder(obtener_proximos_lanzamientos(pagina=pagina, por_pagina=por_pagina), 200)
    except Exception:
        return responder({"message": "Error al obtener los juegos"}, 500)


@router.get("/catalog")
@limiter.limit("60 per minute")
def juegos_del_catalogo(request: Request, id_usuario: str = Depends(id_usuario_actual)):
    try:
        pagina = entero_de_query(request, "page", 1)
        por_pagina = min(entero_de_query(request, "per_page", 20), 40)
        return responder(obtener_juegos_del_catalogo(pagina=pagina, por_pagina=por_pagina), 200)
    except Exception:
        return responder({"message": "Error al obtener el catálogo"}, 500)


@router.get("/filtered")
@limiter.limit("30 per minute")
def juegos_filtrados(request: Request, id_usuario: str = Depends(id_usuario_actual)):
    try:
        resultado = obtener_juegos_filtrados(
            pagina=entero_de_query(request, "page", 1),
            por_pagina=min(entero_de_query(request, "per_page", 20), 40),
            ordering=texto_de_query(request, "ordering"),
            genres=texto_de_query(request, "genres"),
            platforms=texto_de_query(request, "platforms"),
            dates=texto_de_query(request, "dates"),
            search=texto_de_query(request, "search")
        )
        return responder(resultado, 200)
    except Exception:
        return responder({"message": "Error al obtener los juegos filtrados"}, 500)


@router.get("/overview/{game_id}/adicciones")
def adicciones_del_juego(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder(obtener_adicciones_del_juego(id_juego=game_id), 200)
    except Exception:
        return responder({"message": "Error al obtener adicciones"}, 500)


@router.get("/overview/{game_id}/saga")
def saga_del_juego(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder(obtener_saga(id_juego=game_id), 200)
    except Exception:
        return responder({"message": "Error al obtener saga del juego"}, 500)


@router.get("/overview/{game_id}/logros")
def logros_del_juego(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder(obtener_logros_del_juego(id_juego=game_id), 200)
    except Exception:
        return responder({"message": "Error al obtener logros"}, 500)


@router.get("/hero-video")
@limiter.limit("30 per minute")
def video_destacado(request: Request):
    # sin token: el video se muestra en la Home antes de iniciar sesion
    try:
        video = obtener_video_aleatorio()

        if not video:
            return responder({"message": "No hay videos disponibles"}, 404)

        return responder(video, 200)

    except Exception:
        return responder({"message": "Error al obtener video"}, 500)
