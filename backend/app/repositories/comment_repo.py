from app.models.Comment import Comment
from app.database.db import db

def get_all_comments() -> list[Comment]:

    return Comment.query.all()

def get_comment_by_id(comment_id) -> Comment:

    return Comment.query.filter_by(id_comment = comment_id).first()

def get_comments_by_game(id_game):
    return Comment.query.filter_by(id_videogame=id_game).all()

def get_comments_by_user(id_user):
    return Comment.query.filter_by(id_user=id_user).all()

def create_comment(description, id_user, id_game):
    comment = Comment(description=description, id_user=id_user, id_videogame=id_game)
    db.session.add(comment)
    db.session.commit()
    return comment

def update_comment(comment_id, description) -> Comment:

    comment = get_comment_by_id(comment_id)

    if comment:
        comment.description = description
        db.session.commit()

    return comment

def delete_comment(comment_id, user_id) -> bool:
    try:
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