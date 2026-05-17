from app.models.Video_game import Video_game
from app.database.db import db
from sqlalchemy.exc import IntegrityError


def get_game_by_id_bd(game_id) -> Video_game | None:
    return Video_game.query.filter_by(id_game_api=game_id).first()


def create_video_game(id_game_api, name=None, date_release=None,
                      platforms=None, development_company=None) -> Video_game:
    new_video_game = Video_game(
        id_game_api=id_game_api,
        name=name,
        date_release=date_release,
        platforms=platforms,
        development_company=development_company
    )
    db.session.add(new_video_game)
    try:
        db.session.commit()
        return new_video_game
    except IntegrityError:
        db.session.rollback()
        return get_game_by_id_bd(id_game_api)


