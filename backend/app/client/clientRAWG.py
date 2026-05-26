import requests
import os
import time
from collections import OrderedDict


# Cliente para la API de RAWG. Hace de "fachada" entre nuestro backend y
# el servicio externo. Toda la app usa estos helpers en lugar de hacer
# requests directos a RAWG, lo que permite cacheo, retries y cambios de
# endpoint sin tener que tocar las capas de arriba.


# Clave de API. Se lee del entorno; si no esta definida la app igual
# arranca pero todas las llamadas a RAWG fallaran con 401.
CLAVE_API_RAWG = os.getenv('RAWG_API_KEY')

# URL base de la API. RAWG mantiene esta URL estable, asi que la dejamos
# como constante en lugar de exponerla por configuracion.
URL_BASE = "https://api.rawg.io/api"


class CacheConTTL:
    """
    Cache LRU sencilla con tiempo de vida (TTL) por clave. Cuando se
    sobrepasa max_size eliminamos la entrada mas antigua; cuando una entrada
    pasa de ttl segundos se considera caducada y se borra al consultarla.

    No usamos functools.lru_cache porque queremos invalidacion por tiempo,
    no solo por LRU.
    """

    def __init__(self, max_size=150, ttl=3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.timestamps = {}

    def get(self, clave):
        if clave not in self.cache:
            return None

        # Si la entrada ha caducado, la limpiamos antes de devolver None
        # para no acumular basura en memoria.
        if time.time() - self.timestamps[clave] > self.ttl:
            del self.cache[clave]
            del self.timestamps[clave]
            return None

        return self.cache[clave]

    def set(self, clave, valor):
        # Si la clave ya estaba, la borramos para reinsertarla al final
        # del OrderedDict y que aparezca como "mas reciente".
        if clave in self.cache:
            del self.cache[clave]

        # Si llegamos al limite, eliminamos la entrada mas vieja
        # (la primera del OrderedDict).
        if len(self.cache) >= self.max_size:
            clave_mas_antigua = next(iter(self.cache))
            del self.cache[clave_mas_antigua]
            del self.timestamps[clave_mas_antigua]

        self.cache[clave] = valor
        self.timestamps[clave] = time.time()


# Instancia global del cache. 150 entradas y 1 hora de TTL es suficiente
# para reducir mucho las llamadas a RAWG sin gastar demasiada memoria.
cache = CacheConTTL(max_size=150, ttl=3600)


def _peticion_con_cache(endpoint, params=None):
    # Construimos la clave del cache concatenando endpoint + params. Es
    # simple pero funciona; si en el futuro queremos algo mas robusto
    # podemos usar hash de un JSON normalizado.
    clave_cache = f"{endpoint}_{str(params)}"

    resultado_cacheado = cache.get(clave_cache)
    if resultado_cacheado is not None:
        return resultado_cacheado

    # Mezclamos los params del caller con nuestra API key. Timeout corto
    # (5s) para que si RAWG tarda mucho no bloqueemos al usuario.
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
    # Catalogo general paginado. exclude_additions evita que aparezcan
    # DLC sueltos como si fueran juegos completos.
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
    # Juegos con fecha de lanzamiento entre init_date y final_date,
    # ordenados por fecha de lanzamiento ascendente (los mas cercanos primero).
    resultado = _peticion_con_cache("/games", {
        "dates": f"{init_date},{final_date}",
        "ordering": "released",
        "page": page,
        "page_size": per_page,
        "exclude_additions": "true"
    })
    if resultado:
        return resultado.get("results", [])
    return []


def get_games_by_ordering(ordering="-added", per_page=40):
    # Util para el "video aleatorio del hero": pedimos los mas anadidos
    # (o mejor valorados, etc.) y luego elegimos uno al azar.
    # Acotamos el rango de fechas para no incluir juegos muy viejos sin trailer.
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
    # Equipo creativo del juego (directores, guionistas, etc.). Por defecto
    # pedimos 8, que es lo que entra bien en el sidebar del detalle.
    resultado = _peticion_con_cache(f"/games/{game_id}/development-team", {"page_size": page_size})
    if resultado:
        return resultado.get("results", [])
    return []


def obtener_adicciones_juego(game_id, page_size=6):
    # DLC, expansiones y contenido adicional del juego.
    resultado = _peticion_con_cache(f"/games/{game_id}/additions", {"page_size": page_size})
    if resultado:
        return resultado.get("results", [])
    return []


def obtener_saga_del_juego(game_id, page_size=8):
    # Otros juegos de la misma saga (por ejemplo, todos los Final Fantasy).
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
    # Catalogo de TODAS las tiendas conocidas por RAWG (Steam, Epic, etc.).
    # Lo cacheamos como dict {id: tienda} para hacer joins rapidos cuando
    # pintamos las tiendas de un juego concreto.
    resultado = _peticion_con_cache("/stores", {"page_size": 50})
    if not resultado:
        return {}

    diccionario_tiendas = {}
    for tienda in resultado.get("results", []):
        diccionario_tiendas[tienda["id"]] = tienda
    return diccionario_tiendas


def get_game_stores(game_id):
    # Tiendas donde se puede comprar UN juego concreto. Devuelve relaciones
    # con store_id; se cruzan con get_stores_catalog para obtener el nombre.
    resultado = _peticion_con_cache(f"/games/{game_id}/stores")
    if resultado:
        return resultado.get("results", [])
    return []


def get_games_filtered(page=1, per_page=20, ordering=None, genres=None,
                        platforms=None, dates=None, search=None):
    # Buscador filtrado. Solo anadimos al payload los filtros que el
    # caller ha pasado; los que vienen como None se omiten para que RAWG
    # use sus defaults.
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
