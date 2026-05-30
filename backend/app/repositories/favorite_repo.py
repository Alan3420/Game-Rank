from app.models.Favorite import Favorite
from app.models.AddFavorite import AddFavorite
from app.database.db import db
from sqlalchemy import func


def obtener_favorito(id_usuario, id_juego):
    return (Favorite.query
            .join(AddFavorite, Favorite.fav_id == AddFavorite.fav_id)
            .filter(AddFavorite.id_user == id_usuario, Favorite.id_game_api == id_juego)
            .first())


def obtener_favoritos_por_usuario(id_usuario):
    return (Favorite.query
            .join(AddFavorite, Favorite.fav_id == AddFavorite.fav_id)
            .filter(AddFavorite.id_user == id_usuario)
            .all())


def crear_favorito(id_usuario, id_juego, status=None):
    nuevo = Favorite(id_game_api=id_juego, status=status)
    db.session.add(nuevo)
    db.session.flush()
    add_fav = AddFavorite(fav_id=nuevo.fav_id, id_user=id_usuario)
    db.session.add(add_fav)
    db.session.commit()
    return nuevo


def actualizar_status(id_usuario, id_juego, nuevo_status):
    favorito = obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)

    if not favorito:
        return None

    favorito.status = nuevo_status
    db.session.commit()
    return favorito


def eliminar_favorito(id_usuario, id_juego):
    favorito = obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)

    if not favorito:
        return False

    db.session.delete(favorito)
    db.session.commit()
    return True


def obtener_top_favoritos(limite):
    total = func.count(AddFavorite.fav_id).label("total")
    return (db.session.query(Favorite.id_game_api, total)
            .join(AddFavorite, Favorite.fav_id == AddFavorite.fav_id)
            .group_by(Favorite.id_game_api)
            .order_by(total.desc())
            .limit(limite)
            .all())


def obtener_top_coleccion(limite):
    total = func.count(AddFavorite.fav_id).label("total")
    return (db.session.query(Favorite.id_game_api, total)
            .join(AddFavorite, Favorite.fav_id == AddFavorite.fav_id)
            .filter(Favorite.status.isnot(None))
            .group_by(Favorite.id_game_api)
            .order_by(total.desc())
            .limit(limite)
            .all())


def obtener_conteo_estados_por_usuario(id_usuario):
    return (db.session.query(Favorite.status, func.count(Favorite.fav_id))
            .join(AddFavorite, Favorite.fav_id == AddFavorite.fav_id)
            .filter(AddFavorite.id_user == id_usuario, Favorite.status.isnot(None))
            .group_by(Favorite.status)
            .all())


def contar_favoritos_por_usuario(id_usuario):
    total = (db.session.query(func.count(AddFavorite.fav_id))
             .filter(AddFavorite.id_user == id_usuario)
             .scalar())
    return total or 0
