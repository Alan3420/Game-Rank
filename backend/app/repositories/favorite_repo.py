from app.models.Favorite import Favorite
from app.database.db import db
from sqlalchemy import func


# Capa de acceso a datos para la tabla "favorites".
# La tabla tiene PK compuesta (user_id + id_game_api) para evitar duplicados
# a nivel de BD; aun asi comprobamos en el servicio antes de insertar para
# devolver un error legible al frontend en vez de un IntegrityError.


def obtener_favorito(id_usuario, id_juego):
    return Favorite.query.filter_by(user_id=id_usuario, id_game_api=id_juego).first()


def obtener_favoritos_por_usuario(id_usuario):
    return Favorite.query.filter_by(user_id=id_usuario).all()


def crear_favorito(id_usuario, id_juego):
    nuevo_favorito = Favorite(user_id=id_usuario, id_game_api=id_juego)
    db.session.add(nuevo_favorito)
    db.session.commit()
    return nuevo_favorito


def eliminar_favorito(id_usuario, id_juego):
    # Primero comprobamos que exista. Si no, devolvemos False para que
    # el servicio sepa que no habia nada que borrar y avise al frontend.
    favorito = obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)

    if not favorito:
        return False

    db.session.delete(favorito)
    db.session.commit()
    return True


def obtener_top_favoritos(limite):
    # Ranking de juegos con mas favoritos. Devuelve (id_game_api, total).
    total = func.count(Favorite.fav_id).label("total")
    return (db.session.query(Favorite.id_game_api, total)
            .group_by(Favorite.id_game_api)
            .order_by(total.desc())
            .limit(limite)
            .all())


def contar_favoritos_por_usuario(id_usuario):
    total = db.session.query(func.count(Favorite.fav_id))\
                      .filter(Favorite.user_id == id_usuario)\
                      .scalar()
    return total or 0
