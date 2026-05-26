from app.database.db import db
from app.models.Rate import Rate


# Capa de acceso a datos para la tabla "rates" (calificaciones de juegos
# por usuario). La tabla tiene PK compuesta (id_user + id_game_api), asi
# que un usuario solo puede tener una calificacion por juego.


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

    # Solo cambiamos la nota si nos pasaron una. Asi este metodo sirve
    # tambien para "tocar" el registro sin modificar el valor (por si en
    # el futuro se anaden campos editables).
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
