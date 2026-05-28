from app.models.Comment import Comment
from app.database.db import db
from datetime import date
from sqlalchemy import desc, func


# Capa de acceso a datos para la tabla "comments".
# Devuelve modelos sin transformar; los servicios deciden que campos
# exponer al exterior.


def obtener_todos_los_comentarios() -> list[Comment]:
    # Ordenamos primero por fecha y luego por id para que los empates
    # de fecha (mismo dia) salgan en orden de creacion, mas reciente primero.
    return Comment.query.order_by(
        desc(Comment.date_of_comment),
        desc(Comment.id_comment)
    ).all()


def obtener_comentario_por_id(id_comentario) -> Comment:
    return Comment.query.filter_by(id_comment=id_comentario).first()


def obtener_comentarios_por_juego(id_juego):
    return Comment.query.filter_by(id_videogame=id_juego).all()


def obtener_comentarios_por_juego_paginados(id_juego, limite, desplazamiento):
    # Devuelve la pagina de comentarios + el total para que el frontend
    # pueda decidir si mostrar el boton "Load more".
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


def crear_comentario(descripcion, id_usuario, id_juego):
    nuevo_comentario = Comment(
        description=descripcion,
        id_user=id_usuario,
        id_videogame=id_juego
    )
    db.session.add(nuevo_comentario)
    db.session.commit()
    return nuevo_comentario


def actualizar_comentario(id_comentario, descripcion, id_usuario, es_admin=False) -> Comment:
    # Si el que pide la actualizacion es admin, le permitimos editar
    # cualquier comentario. Si no, solo puede editar el suyo (filtramos
    # tambien por id_user para que la query no devuelva nada si intenta
    # tocar uno ajeno).
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
        db.session.commit()

    return comentario


def eliminar_comentario(id_comentario, id_usuario, es_admin=False) -> bool:
    # Misma logica de permisos que actualizar: admin puede borrar cualquiera,
    # el usuario normal solo puede borrar el suyo.
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
        # Hacemos rollback explicito para no dejar la sesion en un estado
        # corrupto que afecte a la siguiente request.
        db.session.rollback()
        print(f"Error en eliminar_comentario: {e}")
        raise e


def obtener_top_comentados(limite):
    # Ranking de juegos con mas resenas. Devuelve (id_videogame, total).
    total = func.count(Comment.id_comment).label("total")
    return (db.session.query(Comment.id_videogame, total)
            .group_by(Comment.id_videogame)
            .order_by(total.desc())
            .limit(limite)
            .all())


def contar_comentarios_por_usuario(id_usuario):
    total = db.session.query(func.count(Comment.id_comment))\
                      .filter(Comment.id_user == id_usuario)\
                      .scalar()
    return total or 0
