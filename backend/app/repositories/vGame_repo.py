from app.models.Video_game import Video_game
from app.database.db import db
from sqlalchemy.exc import IntegrityError


# Capa de acceso a datos para la tabla "videoGame".
# En esta tabla solo guardamos los juegos que algun usuario ha tocado
# (los que ha marcado como favorito, calificado o agregado a su coleccion).
# El resto de juegos viven solo en la API de RAWG y se piden bajo demanda.


def obtener_juego_por_id_bd(id_juego) -> Video_game | None:
    return Video_game.query.filter_by(id_game_api=id_juego).first()


def crear_videojuego(id_juego_api, nombre=None, fecha_lanzamiento=None,
                     plataformas=None, compania_desarrollo=None) -> Video_game:
    nuevo_videojuego = Video_game(
        id_game_api=id_juego_api,
        name=nombre,
        date_release=fecha_lanzamiento,
        platforms=plataformas,
        development_company=compania_desarrollo
    )
    db.session.add(nuevo_videojuego)

    try:
        db.session.commit()
        return nuevo_videojuego

    except IntegrityError:
        # Puede ocurrir cuando dos requests intentan crear el mismo juego
        # casi a la vez (race condition). En ese caso hacemos rollback y
        # devolvemos el registro que ya creo la otra request.
        db.session.rollback()
        return obtener_juego_por_id_bd(id_juego_api)
