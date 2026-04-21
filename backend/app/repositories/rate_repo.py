from app.database.db import db
from app.models.Rate import Rate

def get_rate_by_id(id_rate):
    return Rate.query.filter_by(id_rate=id_rate).first()

def get_rate_by_user_and_game(id_user, id_game):
    return Rate.query.filter_by(id_user=id_user, id_game_api=id_game).first()

def get_rates_by_game(id_game):
    return Rate.query.filter_by(id_game_api=id_game).all()

def get_rates_by_user(id_user):
    return Rate.query.filter_by(id_user=id_user).all()

def create_rate(id_user, id_game, rating, status):
    rate = Rate(id_user=id_user, id_game_api=id_game, rating=rating, status=status)
    db.session.add(rate)
    db.session.commit()
    return rate

def update_rate(id_user, id_game, rating=None, status=None):
    rate = get_rate_by_user_and_game(id_user=id_user, id_game=id_game)
    if not rate:
        return None
    if rating:
        rate.rating = rating
    if status:
        rate.status = status
    db.session.commit()
    return rate

def delete_rate(id_user, id_game):
    rate = get_rate_by_user_and_game(id_user=id_user, id_game=id_game)
    if not rate:
        return False
    db.session.delete(rate)
    db.session.commit()
    return True