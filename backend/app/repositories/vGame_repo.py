from app.models.Video_game import Video_game
from app.database.db import db


def get_all_video_games() -> list[Video_game]:
    
    return Video_game.query.all()

def get_video_game_by_id(game_id) -> Video_game:
    
    return Video_game.query.get(game_id)

def create_video_game(id_game_api, name, date_release, platforms, development_company, id_comment) -> Video_game:
    
    new_video_game = Video_game(id_game_api=id_game_api, name=name, date_release=date_release, platforms=platforms, development_company=development_company, id_comment=id_comment)
    db.session.add(new_video_game)
    db.session.commit()

    return new_video_game

def update_video_game(game_id, name=None, date_release=None, platforms=None, development_company=None, id_comment=None) -> Video_game:
    
    video_game = get_video_game_by_id(game_id)
    if video_game:
        if name:
            video_game.name = name

        if date_release:
            video_game.date_release = date_release

        if platforms:
            video_game.platforms = platforms

        if development_company:
            video_game.development_company = development_company

        if id_comment:
            video_game.id_comment = id_comment

        db.session.commit()

    return video_game

def delete_video_game(game_id) -> bool:
    
    video_game = get_video_game_by_id(game_id)
    if video_game:
        db.session.delete(video_game)
        db.session.commit()
        return True

    return False





