from app.models.Favorite import Favorite
from app.models.Rate import Rate
from app.models.Comment import Comment
from app.models.UserGameStatus import UserGameStatus
from app.database.db import db
from sqlalchemy import func
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import game_format_resume

LIMIT = 8


def _enriquecer(game_id, stat_value, stat_label):
    try:
        data = get_game_by_id_api(game_id)
        resultado = game_format_resume(data)
        resultado["stat_value"] = stat_value
        resultado["stat_label"] = stat_label
        return resultado
    except Exception:
        return None


def obtener_tendencias():
    top_favs = db.session.query(
        Favorite.id_game_api,
        func.count(Favorite.fav_id).label("total")
    ).group_by(Favorite.id_game_api).order_by(func.count(Favorite.fav_id).desc()).limit(LIMIT).all()

    top_rated = db.session.query(
        Rate.id_game_api,
        func.round(func.avg(Rate.rating), 1).label("avg_rating"),
        func.count(Rate.id_rate).label("votes")
    ).group_by(Rate.id_game_api).having(
        func.count(Rate.id_rate) >= 1
    ).order_by(func.avg(Rate.rating).desc()).limit(LIMIT).all()

    top_comments = db.session.query(
        Comment.id_videogame,
        func.count(Comment.id_comment).label("total")
    ).group_by(Comment.id_videogame).order_by(func.count(Comment.id_comment).desc()).limit(LIMIT).all()

    top_coleccion = db.session.query(
        UserGameStatus.id_game_api,
        func.count(UserGameStatus.id_status).label("total")
    ).group_by(UserGameStatus.id_game_api).order_by(func.count(UserGameStatus.id_status).desc()).limit(LIMIT).all()

    def build(items, label_fn):
        resultado = []
        for row in items:
            game_id = row[0]
            raw_val = row[1]
            juego = _enriquecer(game_id, float(raw_val) if raw_val else 0, label_fn(raw_val))
            if juego:
                resultado.append(juego)
        return resultado

    return {
        "mas_favoritos":  build(top_favs,     lambda v: f"{v} {'favorito' if v == 1 else 'favoritos'}"),
        "mejor_valorados": build(top_rated,   lambda v: f"{round(float(v), 1)} / 5 ★"),
        "mas_comentados": build(top_comments, lambda v: f"{v} {'reseña' if v == 1 else 'reseñas'}"),
        "mas_coleccion":  build(top_coleccion,lambda v: f"{v} {'usuario' if v == 1 else 'usuarios'}"),
    }
