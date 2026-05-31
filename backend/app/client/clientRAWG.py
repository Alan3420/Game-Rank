import requests
import os
import time
from collections import OrderedDict


CLAVE_API_RAWG = os.getenv('RAWG_API_KEY')
URL_BASE = "https://api.rawg.io/api"


class CacheConTTL:
    def __init__(self, max_size=150, ttl=3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.timestamps = {}

    def get(self, clave):
        if clave not in self.cache:
            return None

        if time.time() - self.timestamps[clave] > self.ttl:
            del self.cache[clave]
            del self.timestamps[clave]
            return None

        return self.cache[clave]

    def set(self, clave, valor):
        if clave in self.cache:
            del self.cache[clave]

        if len(self.cache) >= self.max_size:
            clave_mas_antigua = next(iter(self.cache))
            del self.cache[clave_mas_antigua]
            del self.timestamps[clave_mas_antigua]

        self.cache[clave] = valor
        self.timestamps[clave] = time.time()


cache = CacheConTTL(max_size=150, ttl=3600)


def _peticion_con_cache(endpoint, params=None):
    clave_cache = f"{endpoint}_{str(params)}"

    resultado_cacheado = cache.get(clave_cache)
    if resultado_cacheado is not None:
        return resultado_cacheado

    parametros_finales = {}
    if params:
        for clave in params:
            parametros_finales[clave] = params[clave]
    parametros_finales["key"] = CLAVE_API_RAWG

    respuesta = requests.get(
        f"{URL_BASE}{endpoint}",
        params=parametros_finales,
        timeout=5
    )

    if respuesta.status_code != 200:
        return None

    resultado = respuesta.json()
    cache.set(clave_cache, resultado)
    return resultado


def get_all_games(page=1, per_page=20):
    # exclude_additions para que no salgan DLC sueltos mezclados con juegos
    resultado = _peticion_con_cache("/games", {
        "page": page,
        "page_size": per_page,
        "exclude_additions": "true"
    })
    return resultado or {}


def get_game_by_id_api(game_id) -> dict:
    resultado = _peticion_con_cache(f"/games/{game_id}")
    return resultado or {}


def get_game_screenshots(game_id):
    resultado = _peticion_con_cache(f"/games/{game_id}/screenshots")
    if resultado:
        return resultado.get("results", [])
    return []


def get_game_movies(game_id):
    resultado = _peticion_con_cache(f"/games/{game_id}/movies")
    if resultado:
        return resultado.get("results", [])
    return []


def get_future_releases(init_date, final_date, page=1, per_page=10):
    resultado = _peticion_con_cache("/games", {
        "dates": f"{init_date},{final_date}",
        "ordering": "released",
        "page": page,
        "page_size": per_page,
        "exclude_additions": "true"
    })
    return resultado or {}


def get_games_by_ordering(ordering="-added", per_page=40):
    # Acotamos las fechas porque los juegos muy antiguos no suelen tener trailer
    # y este metodo se usa para el video del hero
    resultado = _peticion_con_cache("/games", {
        "ordering": ordering,
        "page_size": per_page,
        "dates": "2018-01-01,2026-12-31",
        "exclude_additions": "true"
    })
    if resultado:
        return resultado.get("results", [])
    return []


def obtener_equipo_desarrollo(game_id, page_size=8):
    resultado = _peticion_con_cache(f"/games/{game_id}/development-team", {"page_size": page_size})
    if resultado:
        return resultado.get("results", [])
    return []


def obtener_adicciones_juego(game_id, page_size=6):
    resultado = _peticion_con_cache(f"/games/{game_id}/additions", {"page_size": page_size})
    if resultado:
        return resultado.get("results", [])
    return []


def obtener_saga_del_juego(game_id, page_size=8):
    resultado = _peticion_con_cache(f"/games/{game_id}/game-series", {"page_size": page_size})
    if resultado:
        return resultado.get("results", [])
    return []


def obtener_logros_juego(game_id, page_size=12):
    resultado = _peticion_con_cache(f"/games/{game_id}/achievements", {"page_size": page_size})
    if resultado:
        return resultado.get("results", [])
    return []


def get_stores_catalog():
    # Lo guardamos como dict {id: tienda} asi luego cruzamos rapido con
    # las tiendas de un juego concreto
    resultado = _peticion_con_cache("/stores", {"page_size": 50})
    if not resultado:
        return {}

    diccionario_tiendas = {}
    for tienda in resultado.get("results", []):
        diccionario_tiendas[tienda["id"]] = tienda
    return diccionario_tiendas


def get_game_stores(game_id):
    resultado = _peticion_con_cache(f"/games/{game_id}/stores")
    if resultado:
        return resultado.get("results", [])
    return []


def get_games_filtered(page=1, per_page=20, ordering=None, genres=None,
                        platforms=None, dates=None, search=None):
    params = {
        "page": page,
        "page_size": per_page,
        "exclude_additions": "true"
    }

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

    resultado = _peticion_con_cache("/games", params)
    return resultado or {}
