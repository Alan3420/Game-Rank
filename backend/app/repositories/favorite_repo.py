from app.models.Favorite import Favorite
from app.database.db import db


def get_all_favorites() -> list[Favorite]:

    return Favorite.query.all()


def get_favorite_by_id(favorite_id) -> Favorite:

    return Favorite.query.filter_by(fav_id=favorite_id).first()


def get_favorite(user_id, id_game):
    return Favorite.query.filter_by(user_id=user_id, id_game_api=id_game).first()


def get_favorites_by_user_id(user_id) -> list[Favorite]:

    return Favorite.query.filter_by(fav_id=user_id).first()

def get_favorites_by_user(user_id):
    return Favorite.query.filter_by(user_id=user_id).all()


def get_favorite_by_userID_or_gameID(user_id=None, id_video_game=None) -> Favorite | None:

    if user_id and id_video_game:
        return Favorite.query.filter_by(user_id=user_id, id_game_api=id_video_game).first()
    elif user_id:
        return Favorite.query.filter_by(user_id=user_id).first()
    elif id_video_game:
        return Favorite.query.filter_by(id_game_api=id_video_game).first()
    else:
        return None

    
    
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

    
def delete_favorite_by_userID_or_gameID(user_id=None, id_video_game=None) -> bool:
    if user_id and id_video_game:
        favorite = Favorite.query.filter_by(user_id=user_id, id_game_api=id_video_game).first()
    elif user_id:
        favorite = Favorite.query.filter_by(user_id=user_id).first()
    elif id_video_game:
        favorite = Favorite.query.filter_by(id_game_api=id_video_game).first()
    else:
        return False

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return True
    return False

