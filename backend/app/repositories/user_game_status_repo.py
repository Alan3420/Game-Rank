from app.database.db import db
from app.models.UserGameStatus import UserGameStatus


def obtener_status(id_user, id_game):
    return UserGameStatus.query.filter_by(id_user=id_user, id_game_api=id_game).first()


def listar_statuses_por_usuario(id_user):
    return UserGameStatus.query.filter_by(id_user=id_user).all()


def crear_status(id_user, id_game, status):
    nuevo_registro = UserGameStatus(id_user=id_user, id_game_api=id_game, status=status)
    db.session.add(nuevo_registro)
    db.session.commit()
    return nuevo_registro


def actualizar_status(id_user, id_game, nuevo_status):
    registro = obtener_status(id_user=id_user, id_game=id_game)
    if not registro:
        return None
    registro.status = nuevo_status
    db.session.commit()
    return registro


def eliminar_status(id_user, id_game) -> bool:
    registro = obtener_status(id_user=id_user, id_game=id_game)
    if not registro:
        return False
    db.session.delete(registro)
    db.session.commit()
    return True