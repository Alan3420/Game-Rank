from app.models.Video_game import Video_game
from app.database.db import db
import requests
import os

RAWG_API_KEY = os.getenv('RAWG_API_KEY')
BASE_URL = "https://api.rawg.io/api"


def get_all_video_games() -> list[Video_game]:
    response = requests.get(f"{BASE_URL}/games", params={"key": RAWG_API_KEY})
    return response.json()

def get_game_by_id_api(game_id) -> dict:
    response = requests.get(f"{BASE_URL}/games/{game_id}", params={"key": RAWG_API_KEY})
    return response.json()

def get_game_by_id_bd(game_id) -> Video_game | None:
    video_game = Video_game.query.filter_by(id_game_api=game_id).first()

    if not video_game:
        return None
    
    return video_game

def get_game_by_name(game_name) -> dict:
    response = requests.get(f"{BASE_URL}/games", params={"key": RAWG_API_KEY, "search": game_name})
        
    return response.json()

def create_video_game(id_game_api, name, date_release, platforms, development_company, id_comment) -> Video_game:
    
    new_video_game = Video_game(id_game_api=id_game_api, name=name, date_release=date_release, platforms=platforms, development_company=development_company, id_comment=id_comment)
    db.session.add(new_video_game)
    db.session.commit()

    return new_video_game

def update_video_game(game_id, name=None, date_release=None, platforms=None, development_company=None, id_comment=None) -> Video_game:
    
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

        if id_comment:
            video_game.id_comment = id_comment

        db.session.commit()

    return video_game

def delete_video_game(game_id) -> bool:
    
    video_game = get_game_by_id_bd(game_id)
    if video_game:
        db.session.delete(video_game)
        db.session.commit()
        return True

    return False





