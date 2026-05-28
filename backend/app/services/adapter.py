import re


# Listas para filtrar juegos adultos del catalogo, la app no tiene control
# parental ni verificacion de edad asi que toca cortarlo por aqui
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
    # Vamos palabra a palabra con \b\w+\b para no tener falsos positivos
    # del tipo "scuba" activando "cuba"
    if not nombre:
        return False

    tokens = re.findall(r"\b\w+\b", nombre.lower())
    for token in tokens:
        if token in PALABRAS_NSFW:
            return True
    return False


def es_contenido_adulto(datos_juego) -> bool:
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
    if not datos:
        return []

    resultado = []
    for logro in datos:
        porcentaje = logro.get("percent")

        # A veces el percent viene como string desde RAWG, lo pasamos a float
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
