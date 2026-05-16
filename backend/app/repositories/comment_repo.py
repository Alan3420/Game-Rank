from app.models.Comment import Comment
from app.database.db import db
from datetime import date
from sqlalchemy import desc

def get_all_comments() -> list[Comment]:
    return Comment.query.order_by(desc(Comment.date_of_comment), desc(Comment.id_comment)).all()

def get_comment_by_id(comment_id) -> Comment:

    return Comment.query.filter_by(id_comment = comment_id).first()

def get_comments_by_game(id_game):
    return Comment.query.filter_by(id_videogame=id_game).all()

def get_comments_by_game_paginated(id_game, limit, offset):
    total = Comment.query.filter_by(id_videogame=id_game).count()
    comments = (Comment.query
                .filter_by(id_videogame=id_game)
                .order_by(desc(Comment.date_of_comment), desc(Comment.id_comment))
                .limit(limit)
                .offset(offset)
                .all())
    return comments, total

def get_comments_by_user(id_user):
    return Comment.query.filter_by(id_user=id_user).all()

def create_comment(description, id_user, id_game):
    comment = Comment(description=description, id_user=id_user, id_videogame=id_game)
    db.session.add(comment)
    db.session.commit()
    return comment

def update_comment(comment_id, description, user_id, es_admin=False) -> Comment:
    if es_admin:
        comment = Comment.query.filter_by(id_comment=comment_id).first()
    else:
        comment = Comment.query.filter_by(
            id_comment=comment_id,
            id_user=user_id
        ).first()

    if comment:
        comment.description = description
        comment.date_of_update = date.today()
        db.session.commit()

    return comment

def delete_comment(comment_id, user_id, es_admin=False) -> bool:
    try:
        if es_admin:
            comment = Comment.query.filter_by(id_comment=comment_id).first()
        else:
            comment = Comment.query.filter_by(
                id_comment=comment_id,
                id_user=user_id
            ).first()

        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True

        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error en delete_comment: {e}")
        raise e