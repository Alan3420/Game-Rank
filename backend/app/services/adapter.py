import re

NSFW_TAG_SLUGS = {
    "adult", "nsfw", "hentai", "eroge", "nudity",
    "sexual-content", "adults-only", "pornographic",
    "erotic", "xxx", "18-plus", "porn"
}

NSFW_NAME_KEYWORDS = {
    "porn", "hentai", "xxx", "nsfw", "eroge",
    "rule34", "r34", "futanari", "yiff", "ahegao",
    "lewd", "ecchi", "naked", "nude", "nudes",
    "boobs", "tits", "pussy", "cum"
}


def has_nsfw_name(name) -> bool:
    if not name:
        return False
    tokens = re.findall(r"\b\w+\b", name.lower())
    for token in tokens:
        if token in NSFW_NAME_KEYWORDS:
            return True
    return False


def is_adult_content(game_data) -> bool:
    if not game_data:
        return False

    esrb = game_data.get("esrb_rating")
    if esrb and esrb.get("id") == 5:
        return True

    if has_nsfw_name(game_data.get("name", "")):
        return True

    if not esrb:
        tags = game_data.get("tags") or []
        for tag in tags:
            slug = (tag.get("slug") or "").lower()
            if slug in NSFW_TAG_SLUGS:
                return True

    return False


def platform_format(data) -> dict | list[dict]:
    if not data:
        return None
    
    if type(data) != list:
        return {
            "id": data["platform"].get("id"),
            "name": data["platform"].get("name"),
        }
    else:
        lista_platform_dict = []

        for platform in data:
            platform_dict = {
                "id": platform["platform"].get("id"),
                "name": platform["platform"].get("name"),
            }
            lista_platform_dict.append(platform_dict)
        
        return lista_platform_dict


def developer_format(data) -> dict | list[dict]:
    if not data:
        return None
    if type(data) != list:
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "image": data.get("image_background")
        }
    else:
        lista_developer_dict = []

        for developer in data:
            
            developer_dict = {
                "id": developer.get("id"),
                "name": developer.get("name"),
                "image": developer.get("image_background")
            }
            lista_developer_dict.append(developer_dict)
        
        return lista_developer_dict

def screenshots_format(data) -> list:
    if not data:
        return []
    
    lista_screenshots = []

    for screenshot in data:
        screenshot_dict = {
            "id": screenshot.get("id"),
            "image": screenshot.get("image")
        }
        lista_screenshots.append(screenshot_dict)
    
    return lista_screenshots

def trailer_format(data):
    if not data:
        return None
    
    if type(data) != list:
        return{
            "id": data.get("id"),
            "name": data.get("name"),
            "preview": data.get("preview"),
            "trailer_url": data.get("data",{}).get("max")
        }
    
    else:
        trailer_list_dict = []

        for trailer in data:
            trailer_list = {
                "id": trailer.get("id"),
                "name": trailer.get("name"),
                "preview": trailer.get("preview"),
                "trailer_url": trailer.get("data",{}).get("max")
            }
            trailer_list_dict.append(trailer_list)
        
        return trailer_list_dict

def equipo_format(data) -> list:
    if not data:
        return []
    result = []
    for member in data:
        roles = [p.get("name", "").capitalize() for p in member.get("positions", [])]
        result.append({
            "id": member.get("id"),
            "name": member.get("name"),
            "image": member.get("image"),
            "roles": roles
        })
    return result


def stores_format(data) -> list:
    if not data:
        return []
    result = []
    for item in data:
        store_info = item.get("store", {})
        result.append({
            "id": item.get("id"),
            "name": store_info.get("name"),
            "slug": store_info.get("slug"),
            "url": item.get("url")
        })
    return result


def logros_format(data) -> list:
    if not data:
        return []
    result = []
    for logro in data:
        percent = logro.get("percent")
        try:
            percent = float(percent) if percent is not None else None
        except (ValueError, TypeError):
            percent = None
        result.append({
            "id": logro.get("id"),
            "name": logro.get("name"),
            "description": logro.get("description"),
            "image": logro.get("image"),
            "percent": percent
        })
    return result


def game_format_resume(data) -> dict:
    if type(data) != list:
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "release_date": data.get("released"),
            "imge_url": data.get("background_image"),
            "rating": data.get("rating"),
            "metacritic": data.get("metacritic"),
        }
    else:
        lista_game_dict = []

        for game in data:
            if is_adult_content(game):
                continue

            game_dict = {
                "id": game.get("id"),
                "name": game.get("name"),
                "release_date": game.get("released"),
                "imge_url": game.get("background_image"),
                "rating": game.get("rating"),
                "metacritic": game.get("metacritic"),
            }
            lista_game_dict.append(game_dict)

        return lista_game_dict

def genre_format(data) -> list[dict]:
    if not data:
        return []

    lista_genre_dict = []

    for genre in data:
        genre_dict = {
            "id": genre.get("id"),
            "name": genre.get("name"),
        }
        lista_genre_dict.append(genre_dict)

    return lista_genre_dict


def game_format_details(data) -> dict | list[dict]:

    if type(data) != list:
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "release_date": data.get("released"),
            "description": data.get("description"),
            "imge_url": data.get("background_image"),
            "rating": data.get("rating"),
            "metacritic": data.get("metacritic"),
            "genres":      genre_format(data=data.get("genres", [])),
            "screenshots": screenshots_format(data=data.get("short_screenshots", [])),
            "movies":      trailer_format(data=data.get("movies", [])),
            "platforms":   platform_format(data=data.get("platforms")),
            "developers":  developer_format(data=data.get("developers")),
            "stores":      stores_format(data=data.get("stores", [])),
            "team":        equipo_format(data=data.get("team", [])),
        }
    else:
        lista_game_dict = []

        for game in data:
            game_dict = {
                "id": game.get("id"),
                "name": game.get("name"),
                "release_date": game.get("released"),
                "description": game.get("description"),
                "imge_url": game.get("background_image"),
                "rating": game.get("rating"),
                "metacritic": game.get("metacritic"),
                "genres":      genre_format(data=game.get("genres", [])),
                "screenshots": screenshots_format(data=game.get("short_screenshots", [])),
                "movies":      trailer_format(data=game.get("movies", [])),
                "platforms":   platform_format(data=game.get("platforms")),
                "developers":  developer_format(data=game.get("developers")),
                "stores":      stores_format(data=game.get("stores", [])),
                "team":        equipo_format(data=game.get("team", [])),
            }
            lista_game_dict.append(game_dict)

        return lista_game_dict