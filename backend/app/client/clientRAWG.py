import requests
import os

RAWG_API_KEY = os.getenv('RAWG_API_KEY')
BASE_URL = "https://api.rawg.io/api"

def get_all_video_games(page=1, per_page=10):
    response = requests.get(
        f"{BASE_URL}/games/lists/popular",
        params={
            "key": RAWG_API_KEY,
            "page": page,
            "page_size": per_page
        }
    )
    return response.json()

def get_game_by_id_api(game_id) -> dict:
    response = requests.get(f"{BASE_URL}/games/{game_id}", params={"key": RAWG_API_KEY})
    return response.json()

def get_game_screenshots(game_id):
    response = requests.get(f"{BASE_URL}/games/{game_id}/screenshots", params={"key": RAWG_API_KEY})
    if response.status_code != 200:
        return []
    return response.json().get("results", [])

def get_game_by_name(game_name) -> dict:
    response = requests.get(f"{BASE_URL}/games", params={"key": RAWG_API_KEY, "search": game_name})
        
    return response.json()


def get_game_movies(game_id):
    response = requests.get(f"{BASE_URL}/games/{game_id}/movies", params={"key": RAWG_API_KEY})
    
    if response.status_code != 200:
        return []
    
    return response.json().get("results", [])

def get_future_releases( init_date, final_date, page=1, per_page=10,):
    response = requests.get(f"{BASE_URL}/games?dates={init_date},{final_date}&ordering=released&key={RAWG_API_KEY}", params={"page": page, "page_size": per_page})

    if response.status_code != 200:
        return []
    
    return response.json().get("results")
