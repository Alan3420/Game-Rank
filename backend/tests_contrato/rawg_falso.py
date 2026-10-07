# RAWG simulado para los tests de contrato: respuestas fijas, sin red.
# Sustituye a app.client.clientRAWG._peticion_con_cache, el unico punto
# por el que el backend habla con RAWG.
import re


def _juego(id_juego, nombre, lanzamiento, metacritic, rating, extra=None):
    juego = {
        "id": id_juego,
        "name": nombre,
        "released": lanzamiento,
        "background_image": f"https://media.example/{id_juego}.jpg",
        "rating": rating,
        "metacritic": metacritic,
        "esrb_rating": {"id": 4, "name": "Mature"},
        "tags": [{"slug": "singleplayer"}],
    }
    if extra:
        juego.update(extra)
    return juego


JUEGOS = [
    _juego(101, "Alpha Quest", "2020-05-01", 90, 4.5),
    _juego(102, "Beta Racer", "2019-11-12", 75, 3.9),
    _juego(103, "Gamma Tactics", "2021-02-20", None, 4.1),
    # contenido adulto: el adaptador lo debe filtrar de los listados
    _juego(104, "Delta Adult", "2018-01-01", 60, 3.0, {"esrb_rating": {"id": 5, "name": "Adults Only"}}),
]


def _detalle(id_juego):
    base = next((j for j in JUEGOS if j["id"] == id_juego), None)
    if base is None:
        base = _juego(id_juego, f"Juego {id_juego}", "2022-03-03", 80, 4.0)
    detalle = dict(base)
    detalle.update({
        "description": f"<p>Descripcion de {detalle['name']}</p>",
        "genres": [{"id": 4, "name": "Action"}, {"id": 5, "name": "RPG"}],
        "platforms": [{"platform": {"id": 4, "name": "PC"}}, {"platform": {"id": 187, "name": "PlayStation 5"}}],
        "developers": [{"id": 9, "name": "Estudio Falso", "image_background": "https://media.example/dev.jpg"}],
    })
    return detalle


def _lista(resultados, siguiente=None):
    return {"count": len(resultados), "next": siguiente, "previous": None, "results": resultados}


def peticion_falsa(endpoint, params=None):
    if endpoint == "/games":
        return _lista(list(JUEGOS), "https://api.example/games?page=2")

    if endpoint == "/stores":
        return _lista([{"id": 1, "name": "Steam", "slug": "steam"}, {"id": 3, "name": "PlayStation Store", "slug": "playstation-store"}])

    m = re.fullmatch(r"/games/(\d+)(/[a-z-]+)?", endpoint)
    if not m:
        return None
    id_juego = int(m.group(1))
    sub = m.group(2)

    if sub is None:
        return _detalle(id_juego)
    if sub == "/screenshots":
        return _lista([{"id": 1, "image": "https://media.example/s1.jpg"}, {"id": 2, "image": "https://media.example/s2.jpg"}])
    if sub == "/movies":
        return _lista([{"id": 7, "name": "Trailer", "preview": "https://media.example/p.jpg",
                        "data": {"max": "https://media.example/t.mp4", "480": "https://media.example/t480.mp4"}}])
    if sub == "/stores":
        return _lista([{"id": 55, "store_id": 1, "url": "https://store.example/55"}])
    if sub == "/development-team":
        return _lista([{"id": 3, "name": "Ana Directora", "image": None, "positions": [{"name": "director"}]}])
    if sub == "/additions":
        return _lista([JUEGOS[1]])
    if sub == "/game-series":
        return _lista([JUEGOS[0], JUEGOS[2]])
    if sub == "/achievements":
        return _lista([{"id": 11, "name": "Primer paso", "description": "Empieza", "image": None, "percent": "62.5"},
                       {"id": 12, "name": "Leyenda", "description": "Termina", "image": None, "percent": "3.1"}])
    return None
