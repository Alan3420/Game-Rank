from app.models.Rate import Rate
from app.database.db import db

def get_all_rates() -> list[Rate]:

    return Rate.query.all()

def get_rate_by_id(rate_id) -> Rate:

    return Rate.query.get(rate_id)

def create_rate(id_user, id_video_game, rating) -> Rate:

    new_rate = Rate(id_user=id_user, id_video_game=id_video_game, rating=rating)
    db.session.add(new_rate)
    db.session.commit()

    return new_rate


def update_rate(rate_id, rating) -> Rate | None:

    rate = get_rate_by_id(rate_id)
    if rate:
        rate.rating = rating
        db.session.commit()
        return rate
    return None

def delete_rate(rate_id) -> bool:

    rate = get_rate_by_id(rate_id)

    if rate:
        db.session.delete(rate)
        db.session.commit()
        return True
    return False
