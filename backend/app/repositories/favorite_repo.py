from app.models.Favorite import Favorite
from app.database.db import db


def get_favorite(user_id, id_game):
    return Favorite.query.filter_by(user_id=user_id, id_game_api=id_game).first()


def get_favorites_by_user(user_id):
    return Favorite.query.filter_by(user_id=user_id).all()


def create_favorite(user_id, id_game):
    favorite = Favorite(user_id=user_id, id_game_api=id_game)
    db.session.add(favorite)
    db.session.commit()
    return favorite

def delete_favorite(user_id, id_game):
    
    favorite = get_favorite(user_id=user_id, id_game=id_game)
    if not favorite:
        return False
    db.session.delete(favorite)
    db.session.commit()
    return True

    

