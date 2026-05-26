import re


# Capa "adaptador" entre la respuesta de RAWG y el formato que espera el
# frontend. La API de RAWG devuelve muchos datos que no usamos (y muchos
# anidados); aqui nos quedamos solo con lo que pinta cada componente.


# Lista de tags y palabras clave que marcan contenido NSFW. Los usamos
# para filtrar juegos adultos del catalogo, ya que la app no tiene control
# parental ni verificacion de edad.
TAGS_NSFW = {
    "adult", "nsfw", "hentai", "eroge", "nudity",
    "sexual-content", "adults-only", "pornographic",
    "erotic", "xxx", "18-plus", "porn"
}

PALABRAS_NSFW = {
    "porn", "hentai", "xxx", "nsfw", "eroge",
    "rule34", "r34", "futanari", "yiff", "ahegao",
    "lewd", "ecchi", "naked", "nude", "nudes",
    "boobs", "tits", "pussy", "cum"
}


def nombre_es_nsfw(nombre) -> bool:
    # Tokeniza el nombre con \b\w+\b y comprueba palabra a palabra.
    # Asi evitamos falsos positivos por substrings (p. ej. "scuba" no
    # deberia activar "cuba" si lo metieramos en la lista).
    if not nombre:
        return False

    tokens = re.findall(r"\b\w+\b", nombre.lower())
    for token in tokens:
        if token in PALABRAS_NSFW:
            return True
    return False


def es_contenido_adulto(datos_juego) -> bool:
    # Tres criterios: ESRB rating "Adults Only" (id=5), nombre con palabras
    # NSFW, o tags NSFW si no hay ESRB. Si alguno se cumple, lo filtramos.
    if not datos_juego:
        return False

    esrb = datos_juego.get("esrb_rating")
    if esrb and esrb.get("id") == 5:
        return True

    if nombre_es_nsfw(datos_juego.get("name", "")):
        return True

    if not esrb:
        tags = datos_juego.get("tags") or []
        for tag in tags:
            slug = ""
            if tag.get("slug"):
                slug = tag.get("slug").lower()
            if slug in TAGS_NSFW:
                return True

    return False


def formatear_plataformas(datos) -> dict | list[dict]:
    # Acepta una plataforma suelta o una lista. Si llega lista devolvemos
    # una lista de diccionarios planos con id y name. Reducimos el JSON
    # anidado original a lo minimo.
    if not datos:
        return None

    if type(datos) != list:
        return {
            "id": datos["platform"].get("id"),
            "name": datos["platform"].get("name"),
        }

    resultado = []
    for plataforma in datos:
        resultado.append({
            "id": plataforma["platform"].get("id"),
            "name": plataforma["platform"].get("name"),
        })
    return resultado


def formatear_desarrolladoras(datos) -> dict | list[dict]:
    # Igual que plataformas: dejamos solo id, nombre y la imagen de fondo
    # que usamos como logo en el sidebar del detalle.
    if not datos:
        return None

    if type(datos) != list:
        return {
            "id": datos.get("id"),
            "name": datos.get("name"),
            "image": datos.get("image_background")
        }

    resultado = []
    for desarrolladora in datos:
        resultado.append({
            "id": desarrolladora.get("id"),
            "name": desarrolladora.get("name"),
            "image": desarrolladora.get("image_background")
        })
    return resultado


def formatear_capturas(datos) -> list:
    # Capturas de pantalla del juego para la galeria del detalle.
    if not datos:
        return []

    resultado = []
    for captura in datos:
        resultado.append({
            "id": captura.get("id"),
            "image": captura.get("image")
        })
    return resultado


def formatear_trailers(datos):
    # Por cada trailer guardamos el "preview" (imagen fija que se muestra
    # antes de reproducir) y la URL de mayor calidad disponible.
    if not datos:
        return None

    if type(datos) != list:
        return {
            "id": datos.get("id"),
            "name": datos.get("name"),
            "preview": datos.get("preview"),
            "trailer_url": datos.get("data", {}).get("max")
        }

    resultado = []
    for trailer in datos:
        resultado.append({
            "id": trailer.get("id"),
            "name": trailer.get("name"),
            "preview": trailer.get("preview"),
            "trailer_url": trailer.get("data", {}).get("max")
        })
    return resultado


def formatear_equipo(datos) -> list:
    # Equipo creativo del juego (directores, guionistas, etc.). Sus roles
    # vienen como lista de "positions" y los capitalizamos para la UI.
    if not datos:
        return []

    resultado = []
    for miembro in datos:
        roles = []
        for posicion in miembro.get("positions", []):
            nombre_rol = posicion.get("name", "").capitalize()
            roles.append(nombre_rol)

        resultado.append({
            "id": miembro.get("id"),
            "name": miembro.get("name"),
            "image": miembro.get("image"),
            "roles": roles
        })
    return resultado


def formatear_tiendas(datos) -> list:
    # Tiendas donde se puede comprar el juego (Steam, Epic, etc.).
    # Devolvemos slug + url para que el frontend pueda pintar el icono
    # de la tienda y construir el enlace de "Where to buy".
    if not datos:
        return []

    resultado = []
    for item in datos:
        info_tienda = item.get("store", {})
        resultado.append({
            "id": item.get("id"),
            "name": info_tienda.get("name"),
            "slug": info_tienda.get("slug"),
            "url": item.get("url")
        })
    return resultado


def formatear_logros(datos) -> list:
    # Logros del juego con su porcentaje de obtencion. Convertimos el
    # percent a float defensivamente (a veces RAWG manda string).
    if not datos:
        return []

    resultado = []
    for logro in datos:
        porcentaje = logro.get("percent")

        # Si viene como string lo convertimos. Si no se puede, lo dejamos
        # como None y el frontend decide si lo pinta o no.
        try:
            if porcentaje is not None:
                porcentaje = float(porcentaje)
            else:
                porcentaje = None
        except (ValueError, TypeError):
            porcentaje = None

        resultado.append({
            "id": logro.get("id"),
            "name": logro.get("name"),
            "description": logro.get("description"),
            "image": logro.get("image"),
            "percent": porcentaje
        })
    return resultado


def formatear_resumen_juego(datos) -> dict:
    # Formato "card" del juego: lo minimo para pintar una tarjeta del
    # catalogo (id, nombre, fecha, imagen, rating y metacritic).
    #
    # Acepta tanto un dict individual (juego suelto) como una lista (catalogo).
    # En el caso de lista, ademas filtra los juegos NSFW para que no salgan
    # nunca en el catalogo publico.
    if type(datos) != list:
        return {
            "id": datos.get("id"),
            "name": datos.get("name"),
            "release_date": datos.get("released"),
            "imge_url": datos.get("background_image"),
            "rating": datos.get("rating"),
            "metacritic": datos.get("metacritic"),
        }

    resultado = []
    for juego in datos:
        if es_contenido_adulto(juego):
            continue

        resultado.append({
            "id": juego.get("id"),
            "name": juego.get("name"),
            "release_date": juego.get("released"),
            "imge_url": juego.get("background_image"),
            "rating": juego.get("rating"),
            "metacritic": juego.get("metacritic"),
        })

    return resultado


def formatear_generos(datos) -> list[dict]:
    if not datos:
        return []

    resultado = []
    for genero in datos:
        resultado.append({
            "id": genero.get("id"),
            "name": genero.get("name"),
        })
    return resultado


def formatear_detalle_juego(datos) -> dict | list[dict]:
    # Formato "detalle completo" del juego: el de la pantalla GameDetail.
    # Incluye todo lo del resumen + descripcion, generos, capturas, trailers,
    # plataformas, desarrolladoras, tiendas y equipo.
    #
    # Como en el resumen, acepta dict individual o lista.
    if type(datos) != list:
        return {
            "id": datos.get("id"),
            "name": datos.get("name"),
            "release_date": datos.get("released"),
            "description": datos.get("description"),
            "imge_url": datos.get("background_image"),
            "rating": datos.get("rating"),
            "metacritic": datos.get("metacritic"),
            "genres":      formatear_generos(datos=datos.get("genres", [])),
            "screenshots": formatear_capturas(datos=datos.get("short_screenshots", [])),
            "movies":      formatear_trailers(datos=datos.get("movies", [])),
            "platforms":   formatear_plataformas(datos=datos.get("platforms")),
            "developers":  formatear_desarrolladoras(datos=datos.get("developers")),
            "stores":      formatear_tiendas(datos=datos.get("stores", [])),
            "team":        formatear_equipo(datos=datos.get("team", [])),
        }

    resultado = []
    for juego in datos:
        resultado.append({
            "id": juego.get("id"),
            "name": juego.get("name"),
            "release_date": juego.get("released"),
            "description": juego.get("description"),
            "imge_url": juego.get("background_image"),
            "rating": juego.get("rating"),
            "metacritic": juego.get("metacritic"),
            "genres":      formatear_generos(datos=juego.get("genres", [])),
            "screenshots": formatear_capturas(datos=juego.get("short_screenshots", [])),
            "movies":      formatear_trailers(datos=juego.get("movies", [])),
            "platforms":   formatear_plataformas(datos=juego.get("platforms")),
            "developers":  formatear_desarrolladoras(datos=juego.get("developers")),
            "stores":      formatear_tiendas(datos=juego.get("stores", [])),
            "team":        formatear_equipo(datos=juego.get("team", [])),
        })

    return resultado


