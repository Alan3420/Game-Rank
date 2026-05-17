import requests
import os
import time
from collections import OrderedDict

RAWG_API_KEY = os.getenv('RAWG_API_KEY')
BASE_URL = "https://api.rawg.io/api"


class CacheWithTTL:
    def __init__(self, max_size=150, ttl=3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.timestamps = {}

    def get(self, key):
        if key not in self.cache:
            return None

        if time.time() - self.timestamps[key] > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return None

        return self.cache[key]

    def set(self, key, value):
        if key in self.cache:
            del self.cache[key]

        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]

        self.cache[key] = value
        self.timestamps[key] = time.time()


cache = CacheWithTTL(max_size=150, ttl=3600)


def _request_with_cache(endpoint, params=None):
    cache_key = f"{endpoint}_{str(params)}"

    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params={**(params or {}), "key": RAWG_API_KEY},
        timeout=5
    )

    if response.status_code != 200:
        return None

    result = response.json()
    cache.set(cache_key, result)
    return result


def get_all_games(page=1, per_page=20):
    result = _request_with_cache("/games", {"page": page, "page_size": per_page, "exclude_additions": "true"})
    return result or {}

def get_game_by_id_api(game_id) -> dict:
    result = _request_with_cache(f"/games/{game_id}")
    return result or {}

def get_game_screenshots(game_id):
    result = _request_with_cache(f"/games/{game_id}/screenshots")
    return result.get("results", []) if result else []

def get_game_by_name(game_name) -> dict:
    result = _request_with_cache("/games", {"search": game_name, "exclude_additions": "true"})
    return result or {}


def get_game_movies(game_id):
    result = _request_with_cache(f"/games/{game_id}/movies")
    return result.get("results", []) if result else []

def get_future_releases(init_date, final_date, page=1, per_page=10):
    result = _request_with_cache("/games", {
        "dates": f"{init_date},{final_date}",
        "ordering": "released",
        "page": page,
        "page_size": per_page,
        "exclude_additions": "true"
    })
    return result.get("results", []) if result else []

def get_games_by_ordering(ordering="-added", per_page=40):
    result = _request_with_cache("/games", {
        "ordering": ordering,
        "page_size": per_page,
        "dates": "2018-01-01,2026-12-31",
        "exclude_additions": "true"
    })
    return result.get("results", []) if result else []

def obtener_equipo_desarrollo(game_id, page_size=8):
    result = _request_with_cache(f"/games/{game_id}/development-team", {"page_size": page_size})
    return result.get("results", []) if result else []


def obtener_adicciones_juego(game_id, page_size=6):
    result = _request_with_cache(f"/games/{game_id}/additions", {"page_size": page_size})
    return result.get("results", []) if result else []


def obtener_saga_del_juego(game_id, page_size=8):
    result = _request_with_cache(f"/games/{game_id}/game-series", {"page_size": page_size})
    return result.get("results", []) if result else []


def obtener_logros_juego(game_id, page_size=12):
    result = _request_with_cache(f"/games/{game_id}/achievements", {"page_size": page_size})
    return result.get("results", []) if result else []


def get_stores_catalog():
    result = _request_with_cache("/stores", {"page_size": 50})
    if not result:
        return {}
    return {s["id"]: s for s in result.get("results", [])}


def get_game_stores(game_id):
    result = _request_with_cache(f"/games/{game_id}/stores")
    return result.get("results", []) if result else []


def get_games_filtered(page=1, per_page=20, ordering=None, genres=None, platforms=None, dates=None, search=None):
    params = {"page": page, "page_size": per_page, "exclude_additions": "true"}
    if ordering:
        params["ordering"] = ordering
    if genres:
        params["genres"] = genres
    if platforms:
        params["platforms"] = platforms
    if dates:
        params["dates"] = dates
    if search:
        params["search"] = search
    result = _request_with_cache("/games", params)
    return result or {}
