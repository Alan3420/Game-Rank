from app.models.Comment import Comment
from app.database.db import db

def get_all_comments() -> list[Comment]:

    return Comment.query.all()

def get_comment_by_id(comment_id) -> Comment:

    return Comment.query.get(comment_id)

def create_comment(description, id_user) -> Comment:

    comment = Comment(description=description, id_user=id_user)
    db.session.add(comment)
    db.session.commit()

    return comment

def update_comment(comment_id, description) -> Comment:

    comment = get_comment_by_id(comment_id)

    if comment:
        comment.description = description
        db.session.commit()

    return comment

def delete_comment(comment_id) -> bool:

    comment = get_comment_by_id(comment_id)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return True

    return False