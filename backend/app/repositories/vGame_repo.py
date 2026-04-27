from app.models.Video_game import Video_game
from app.database.db import db


def get_all_video_games_bd() -> list[Video_game]:
    return Video_game.query.all()

def get_video_games_by_name_bd(name) -> list[Video_game]:
    return Video_game.query.filter(Video_game.name.like(f"%{name}%")).all()

def get_game_by_id_bd(game_id) -> Video_game | None:
    video_game = Video_game.query.filter_by(id_game_api=game_id).first()

    if not video_game:
        return None
    
    return video_game


def create_video_game(id_game_api, name, date_release, platforms, development_company) -> Video_game:
    
    new_video_game = Video_game(id_game_api=id_game_api, name=name, date_release=date_release, platforms=platforms, development_company=development_company)
    db.session.add(new_video_game)
    db.session.commit()

    return new_video_game

def update_video_game(game_id, name=None, date_release=None, platforms=None, development_company=None) -> Video_game:
    
    video_game = get_game_by_id_bd(game_id)
    if video_game:
        if name:
            video_game.name = name

        if date_release:
            video_game.date_release = date_release

        if platforms:
            video_game.platforms = platforms

        if development_company:
            video_game.development_company = development_company

        db.session.commit()

    return video_game

def delete_video_game(game_id) -> bool:
    
    video_game = get_game_by_id_bd(game_id)
    if video_game:
        db.session.delete(video_game)
        db.session.commit()
        return True

    return False





