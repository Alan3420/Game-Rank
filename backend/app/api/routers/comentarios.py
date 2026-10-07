from fastapi import APIRouter, Depends, Request

from app.api.esquemas import DatosEdicionComentario, DatosNuevoComentario
from app.api.limites import limiter
from app.api.respuestas import entero_de_query, responder
from app.api.seguridad import admin_requerido, id_usuario_actual
from app.repositories.user_repo import obtener_usuario_por_id
from app.services import user_service
from app.services.comment_services import (
    crear_comentario,
    actualizar_comentario,
    eliminar_comentario,
    obtener_comentarios_del_juego,
    obtener_comentarios_del_usuario,
    obtener_todos_los_comentarios,
    obtener_promedio_del_juego
)

router = APIRouter(prefix="/comment", tags=["Reseñas"])


def _es_admin(id_usuario):
    usuario = obtener_usuario_por_id(id_usuario)
    return bool(usuario and usuario.role == 'admin')


@router.post("/create")
@limiter.limit("5 per minute")
def crear(request: Request, datos: DatosNuevoComentario, id_usuario: str = Depends(id_usuario_actual)):
    try:
        descripcion = datos.description

        if not datos.id_game or not descripcion or datos.rating is None:
            return responder({"message": "id_game, description y rating son obligatorios"}, 400)

        if len(descripcion) > 255:
            return responder({"message": "El comentario no puede superar los 255 caracteres"}, 400)

        resultado = crear_comentario(
            id_usuario=id_usuario,
            id_juego=datos.id_game,
            descripcion=descripcion,
            rating=datos.rating
        )

        if type(resultado) == str:
            return responder({"message": resultado}, 409)

        return responder({"message": "Comentario creado", "comment": resultado.to_dict()}, 201)

    except Exception:
        return responder({"message": "Error al crear el comentario"}, 500)


@router.put("/update/{comment_id}")
@limiter.limit("10 per minute")
def actualizar(request: Request, comment_id: int, datos: DatosEdicionComentario,
               id_usuario: str = Depends(id_usuario_actual)):
    try:
        descripcion = datos.description

        if not descripcion:
            return responder({"message": "description es obligatoria"}, 400)

        if len(descripcion) > 255:
            return responder({"message": "El comentario no puede superar los 255 caracteres"}, 400)

        resultado = actualizar_comentario(
            id_comentario=comment_id,
            descripcion=descripcion,
            id_usuario=id_usuario,
            rating=datos.rating,
            es_admin=_es_admin(id_usuario)
        )

        if type(resultado) == str:
            return responder({"message": resultado}, 404)

        return responder({"message": "Comentario actualizado", "comment": resultado.to_dict()}, 200)

    except Exception:
        return responder({"message": "Error al actualizar el comentario"}, 500)


@router.delete("/delete/{comment_id}")
def eliminar(comment_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        resultado = eliminar_comentario(
            id_comentario=comment_id,
            id_usuario=id_usuario,
            es_admin=_es_admin(id_usuario)
        )

        # este endpoint responde con "msg" (no "message") desde la version Flask
        if resultado is True:
            return responder({"msg": "Comentario eliminado"}, 200)

        return responder({"msg": resultado}, 403)

    except Exception:
        return responder({"message": "Error interno del servidor"}, 500)


@router.get("/game/{game_id}")
def obtener_por_juego(request: Request, game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        # topes para que nadie pida 5000 comentarios de golpe
        limite = min(entero_de_query(request, "limit", 10), 40)
        desplazamiento = max(entero_de_query(request, "offset", 0), 0)

        datos = obtener_comentarios_del_juego(id_juego=game_id, limite=limite, desplazamiento=desplazamiento)
        return responder(datos, 200)

    except Exception:
        return responder({"message": "Error al obtener comentarios"}, 500)


@router.get("/avg/{game_id}")
def obtener_promedio(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder({"game_id": game_id, "avg_rating": obtener_promedio_del_juego(id_juego=game_id)}, 200)
    except Exception:
        return responder({"message": "Error al obtener la media"}, 500)


@router.get("/all")
@limiter.limit("30 per minute")
def obtener_todos_admin(request: Request, id_usuario: str = Depends(admin_requerido)):
    try:
        return responder({"comments": obtener_todos_los_comentarios()}, 200)
    except Exception:
        return responder({"message": "Error al obtener comentarios"}, 500)


@router.get("/user")
def obtener_por_usuario(id_usuario: str = Depends(id_usuario_actual)):
    try:
        comentarios = obtener_comentarios_del_usuario(id_usuario=id_usuario)
        usuario = user_service.obtener_usuario_por_id(id_usuario=id_usuario)

        return responder({
            "comments": comentarios,
            "user": usuario.to_dict() if usuario else None
        }, 200)

    except Exception:
        return responder({"message": "Error al obtener comentarios"}, 500)
