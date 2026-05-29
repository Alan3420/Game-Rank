from app.database.db import db
from app.models.Rate import Rate
from sqlalchemy import func


def obtener_calificacion_por_usuario_y_juego(id_usuario, id_juego):
    return Rate.query.filter_by(id_user=id_usuario, id_game_api=id_juego).first()


def obtener_calificaciones_por_juego(id_juego):
    return Rate.query.filter_by(id_game_api=id_juego).all()


def obtener_calificaciones_por_usuario(id_usuario):
    return Rate.query.filter_by(id_user=id_usuario).all()


def crear_calificacion(id_usuario, id_juego, valor):
    nueva_calificacion = Rate(id_user=id_usuario, id_game_api=id_juego, rating=valor)
    db.session.add(nueva_calificacion)
    db.session.commit()
    return nueva_calificacion


def actualizar_calificacion(id_usuario, id_juego, valor=None):
    calificacion = obtener_calificacion_por_usuario_y_juego(
        id_usuario=id_usuario,
        id_juego=id_juego
    )

    if not calificacion:
        return None

    if valor:
        calificacion.rating = valor

    db.session.commit()
    return calificacion


def eliminar_calificacion(id_usuario, id_juego):
    calificacion = obtener_calificacion_por_usuario_y_juego(
        id_usuario=id_usuario,
        id_juego=id_juego
    )

    if not calificacion:
        return False

    db.session.delete(calificacion)
    db.session.commit()
    return True


def obtener_top_valorados(limite):
    promedio = func.round(func.avg(Rate.rating), 1).label("avg_rating")
    votos = func.count(Rate.id_user).label("votes")
    return (db.session.query(Rate.id_game_api, promedio, votos)
            .group_by(Rate.id_game_api)
            .having(func.count(Rate.id_user) >= 1)
            .order_by(func.avg(Rate.rating).desc())
            .limit(limite)
            .all())
