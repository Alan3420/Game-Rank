from app.models.Comment import Comment
from app.database.db import db
from datetime import date
from sqlalchemy import desc, func


def obtener_todos_los_comentarios() -> list[Comment]:
    return Comment.query.order_by(
        desc(Comment.date_of_comment),
        desc(Comment.id_comment)
    ).all()


def obtener_comentario_por_id(id_comentario) -> Comment:
    return Comment.query.filter_by(id_comment=id_comentario).first()


def obtener_comentarios_por_juego(id_juego):
    return Comment.query.filter_by(id_videogame=id_juego).all()


def obtener_comentarios_por_juego_paginados(id_juego, limite, desplazamiento):
    total = Comment.query.filter_by(id_videogame=id_juego).count()

    comentarios = (Comment.query
                   .filter_by(id_videogame=id_juego)
                   .order_by(desc(Comment.date_of_comment), desc(Comment.id_comment))
                   .limit(limite)
                   .offset(desplazamiento)
                   .all())

    return comentarios, total


def obtener_comentarios_por_usuario(id_usuario):
    return Comment.query.filter_by(id_user=id_usuario).all()


def crear_comentario(descripcion, id_usuario, id_juego, rating):
    nuevo_comentario = Comment(
        description=descripcion,
        id_user=id_usuario,
        id_videogame=id_juego,
        rating=rating
    )
    db.session.add(nuevo_comentario)
    db.session.commit()
    return nuevo_comentario


def actualizar_comentario(id_comentario, descripcion, id_usuario, rating=None, es_admin=False) -> Comment:
    # El admin puede editar cualquier comentario, un usuario normal solo el suyo
    if es_admin:
        comentario = Comment.query.filter_by(id_comment=id_comentario).first()
    else:
        comentario = Comment.query.filter_by(
            id_comment=id_comentario,
            id_user=id_usuario
        ).first()

    if comentario:
        comentario.description = descripcion
        comentario.date_of_update = date.today()
        if rating is not None:
            comentario.rating = rating
        db.session.commit()

    return comentario


def eliminar_comentario(id_comentario, id_usuario, es_admin=False) -> bool:
    try:
        if es_admin:
            comentario = Comment.query.filter_by(id_comment=id_comentario).first()
        else:
            comentario = Comment.query.filter_by(
                id_comment=id_comentario,
                id_user=id_usuario
            ).first()

        if comentario:
            db.session.delete(comentario)
            db.session.commit()
            return True

        return False

    except Exception as e:
        db.session.rollback()
        print(f"Error en eliminar_comentario: {e}")
        raise e


def obtener_promedio_por_juego(id_juego) -> float:
    resultado = (db.session.query(func.avg(Comment.rating))
                 .filter(Comment.id_videogame == id_juego)
                 .scalar())
    if resultado is None:
        return 0.0
    return round(float(resultado), 2)


def obtener_top_comentados(limite):
    total = func.count(Comment.id_comment).label("total")
    return (db.session.query(Comment.id_videogame, total)
            .group_by(Comment.id_videogame)
            .order_by(total.desc())
            .limit(limite)
            .all())


def obtener_top_valorados(limite):
    promedio = func.round(func.avg(Comment.rating), 1).label("avg_rating")
    votos = func.count(Comment.id_comment).label("votes")
    return (db.session.query(Comment.id_videogame, promedio, votos)
            .group_by(Comment.id_videogame)
            .having(func.count(Comment.id_comment) >= 1)
            .order_by(func.avg(Comment.rating).desc())
            .limit(limite)
            .all())


def contar_comentarios_por_usuario(id_usuario):
    total = db.session.query(func.count(Comment.id_comment))\
                      .filter(Comment.id_user == id_usuario)\
                      .scalar()
    return total or 0
