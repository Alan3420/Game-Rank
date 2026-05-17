from app.database.db import db
from app.models.Rate import Rate

def get_rate_by_user_and_game(id_user, id_game):
    return Rate.query.filter_by(id_user=id_user, id_game_api=id_game).first()

def get_rates_by_game(id_game):
    return Rate.query.filter_by(id_game_api=id_game).all()

def get_rates_by_user(id_user):
    return Rate.query.filter_by(id_user=id_user).all()

def create_rate(id_user, id_game, rating):
    rate = Rate(id_user=id_user, id_game_api=id_game, rating=rating)
    db.session.add(rate)
    db.session.commit()
    return rate

def update_rate(id_user, id_game, rating=None):
    rate = get_rate_by_user_and_game(id_user=id_user, id_game=id_game)
    if not rate:
        return None
    if rating:
        rate.rating = rating
    db.session.commit()
    return rate

def delete_rate(id_user, id_game):
    rate = get_rate_by_user_and_game(id_user=id_user, id_game=id_game)
    if not rate:
        return False
    db.session.delete(rate)
    db.session.commit()
    return True