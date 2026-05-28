from app.database.db import db
from app.models.UserGameStatus import UserGameStatus
from sqlalchemy import func


# Capa de acceso a datos para la tabla "user_game_status".
# Guarda en que estado tiene cada usuario sus juegos (pendiente, jugando,
# pausado, completado). Es lo que pinta la pestana "My Collection" del perfil.


def obtener_estado(id_usuario, id_juego):
    return UserGameStatus.query.filter_by(id_user=id_usuario, id_game_api=id_juego).first()


def listar_estados_por_usuario(id_usuario):
    return UserGameStatus.query.filter_by(id_user=id_usuario).all()


def crear_estado(id_usuario, id_juego, estado):
    nuevo_registro = UserGameStatus(
        id_user=id_usuario,
        id_game_api=id_juego,
        status=estado
    )
    db.session.add(nuevo_registro)
    db.session.commit()
    return nuevo_registro


def actualizar_estado(id_usuario, id_juego, nuevo_estado):
    registro = obtener_estado(id_usuario=id_usuario, id_juego=id_juego)

    if not registro:
        return None

    registro.status = nuevo_estado
    db.session.commit()
    return registro


def eliminar_estado(id_usuario, id_juego) -> bool:
    registro = obtener_estado(id_usuario=id_usuario, id_juego=id_juego)

    if not registro:
        return False

    db.session.delete(registro)
    db.session.commit()
    return True


def obtener_top_coleccion(limite):
    # Ranking de juegos mas anadidos a colecciones (sin importar el estado).
    # Devuelve (id_game_api, total).
    total = func.count(UserGameStatus.id_status).label("total")
    return (db.session.query(UserGameStatus.id_game_api, total)
            .group_by(UserGameStatus.id_game_api)
            .order_by(total.desc())
            .limit(limite)
            .all())


def obtener_conteo_estados_por_usuario(id_usuario):
    # Cuantas filas tiene el usuario por cada estado (pendiente, jugando,
    # pausado, completado). Devuelve (estado, total).
    return (db.session.query(UserGameStatus.status, func.count(UserGameStatus.id_status))
            .filter(UserGameStatus.id_user == id_usuario)
            .group_by(UserGameStatus.status)
            .all())
