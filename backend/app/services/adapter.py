
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
    

    
def game_format(data) -> dict | list[dict]:
    
    if type(data) != list:
        print(data)
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "release_date": data.get("released"),
            "description": data.get("description"),
            "imge_url": data.get("background_image"),
            "rating": data.get("rating"),
            "platforms":   platform_format(data=data.get("platforms")),
            "developers":   developer_format(data=data.get("developers")),
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
                "platforms":    platform_format(data=game.get("platforms")),
                "developers":   developer_format(data=game.get("developers")),
            }
            lista_game_dict.append(game_dict)
        
        return lista_game_dict