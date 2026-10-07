from fastapi import APIRouter, Depends

from app.api.esquemas import DatosFavorito
from app.api.respuestas import responder
from app.api.seguridad import id_usuario_actual
from app.services.favorite_services import (
    agregar_favorito,
    eliminar_favorito,
    obtener_favoritos_del_usuario,
    es_favorito,
    actualizar_status,
    obtener_estado_del_juego,
    quitar_status,
    listar_favoritos_con_status,
    listar_favoritos_completos
)

router = APIRouter(prefix="/favorite", tags=["Favoritos y estados"])


@router.post("/add")
def agregar(datos: DatosFavorito, id_usuario: str = Depends(id_usuario_actual)):
    try:
        if not datos.id_game:
            return responder({"message": "id_game es obligatorio"}, 400)

        resultado = agregar_favorito(id_usuario=id_usuario, id_juego=datos.id_game, status=datos.status)

        if type(resultado) == str:
            return responder({"message": resultado}, 409)

        return responder({
            "message": "Juego añadido a favoritos",
            "favorite": resultado.to_dict()
        }, 201)

    except Exception:
        return responder({"message": "Error al añadir favorito"}, 500)


@router.delete("/remove")
def quitar(datos: DatosFavorito, id_usuario: str = Depends(id_usuario_actual)):
    try:
        if not datos.id_game:
            return responder({"message": "id_game es obligatorio"}, 400)

        resultado = eliminar_favorito(id_usuario=id_usuario, id_juego=datos.id_game)

        if type(resultado) == str:
            return responder({"message": resultado}, 404)

        return responder({"message": "Juego eliminado de favoritos"}, 200)

    except Exception:
        return responder({"message": "Error al eliminar favorito"}, 500)


@router.put("/status")
def actualizar_estado(datos: DatosFavorito, id_usuario: str = Depends(id_usuario_actual)):
    try:
        if not datos.id_game or not datos.status:
            return responder({"message": "id_game y status son obligatorios"}, 400)

        resultado = actualizar_status(
            id_usuario=int(id_usuario),
            id_juego=datos.id_game,
            nuevo_status=datos.status
        )

        if type(resultado) == str:
            return responder({"message": resultado}, 400)

        return responder({
            "message": "Status actualizado",
            "favorite": resultado.to_dict()
        }, 200)

    except Exception:
        return responder({"message": "Error al actualizar el status"}, 500)


@router.get("/status/{game_id}")
def obtener_estado(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        favorito = obtener_estado_del_juego(id_usuario=int(id_usuario), id_juego=game_id)

        if not favorito:
            return responder({"status": None}, 200)

        return responder({"status": favorito.to_dict()}, 200)

    except Exception:
        return responder({"message": "Error al obtener el status"}, 500)


@router.delete("/status/{game_id}")
def eliminar_estado(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        resultado = quitar_status(id_usuario=int(id_usuario), id_juego=game_id)

        if type(resultado) == str:
            return responder({"message": resultado}, 404)

        return responder({"message": "Status eliminado"}, 200)

    except Exception:
        return responder({"message": "Error al eliminar el status"}, 500)


@router.get("/listFav")
def listar_favoritos(id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder({"favorites": obtener_favoritos_del_usuario(id_usuario=id_usuario)}, 200)
    except Exception:
        return responder({"message": "Error al obtener favoritos"}, 500)


@router.get("/list")
def listar_con_status(id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder({"statuses": listar_favoritos_con_status(id_usuario=int(id_usuario))}, 200)
    except Exception:
        return responder({"message": "Error al listar estados"}, 500)


@router.get("/list/full")
def listar_completos(id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder({"statuses": listar_favoritos_completos(id_usuario=int(id_usuario))}, 200)
    except Exception:
        return responder({"message": "Error al listar favoritos completos"}, 500)


@router.get("/check/{game_id}")
def comprobar(game_id: int, id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder({"is_favorite": es_favorito(id_usuario=id_usuario, id_juego=game_id)}, 200)
    except Exception:
        return responder({"message": "Error al comprobar favorito"}, 500)
