from app.models.Favorite import Favorite
from app.models.Rate import Rate
from app.models.Comment import Comment
from app.models.UserGameStatus import UserGameStatus
from app.database.db import db
from sqlalchemy import func
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import game_format_resume
from concurrent.futures import ThreadPoolExecutor

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


def _enriquecer_lista(tareas):
    """
    Recibe una lista de tuplas (game_id, stat_value, stat_label).
    Llama a la API de RAWG para cada juego en paralelo usando hilos,
    en vez de esperar uno por uno. Los resultados mantienen el orden original.
    """
    if not tareas:
        return []

    def procesar(tarea):
        game_id, stat_value, stat_label = tarea
        return _enriquecer(game_id, stat_value, stat_label)

    with ThreadPoolExecutor(max_workers=len(tareas)) as executor:
        resultados = list(executor.map(procesar, tareas))

    return [juego for juego in resultados if juego is not None]


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
        func.count(Rate.id_user) >= 1
    ).order_by(func.avg(Rate.rating).desc()).limit(LIMIT).all()

    top_comments = db.session.query(
        Comment.id_videogame,
        func.count(Comment.id_comment).label("total")
    ).group_by(Comment.id_videogame).order_by(func.count(Comment.id_comment).desc()).limit(LIMIT).all()

    top_coleccion = db.session.query(
        UserGameStatus.id_game_api,
        func.count(UserGameStatus.id_status).label("total")
    ).group_by(UserGameStatus.id_game_api).order_by(func.count(UserGameStatus.id_status).desc()).limit(LIMIT).all()

    # Construir listas de tareas con el label ya calculado antes de llamar a la API
    tareas_favs = []
    for row in top_favs:
        game_id = row[0]
        total   = row[1]
        label   = f"{total} {'favorito' if total == 1 else 'favoritos'}"
        tareas_favs.append((game_id, float(total), label))

    tareas_rated = []
    for row in top_rated:
        game_id  = row[0]
        promedio = float(row[1]) if row[1] else 0.0
        label    = f"{round(promedio, 1)} / 5 ★"
        tareas_rated.append((game_id, promedio, label))

    tareas_comments = []
    for row in top_comments:
        game_id = row[0]
        total   = row[1]
        label   = f"{total} {'reseña' if total == 1 else 'reseñas'}"
        tareas_comments.append((game_id, float(total), label))

    tareas_coleccion = []
    for row in top_coleccion:
        game_id = row[0]
        total   = row[1]
        label   = f"{total} {'usuario' if total == 1 else 'usuarios'}"
        tareas_coleccion.append((game_id, float(total), label))

    return {
        "mas_favoritos":   _enriquecer_lista(tareas_favs),
        "mejor_valorados": _enriquecer_lista(tareas_rated),
        "mas_comentados":  _enriquecer_lista(tareas_comments),
        "mas_coleccion":   _enriquecer_lista(tareas_coleccion),
    }
