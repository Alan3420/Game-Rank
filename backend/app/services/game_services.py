from app.repositories.vGame_repo import get_game_by_id, get_all_video_games, create_video_game

def get_video_game_details(game_id):
    game_details = get_game_by_id(game_id=game_id)
    all_games = get_all_video_games()

    print(game_details)
    game_exists = False

    for game in all_games:
        if game.id_game_api ==game_details["id"]:
            print(game.id_game_api)
            game_exists = True

            break

    if not game_exists:
        create_video_game(id_game_api=int(game_details["id"]), 
                              name=str(game_details["name"]), 
                              date_release=game_details["released"], 
                              platforms=str(game_details["platforms"][0]["platform"]["name"]), 
                              development_company=str(game_details["developers"][0]["name"]), 
                              id_comment=None)

    return game_format(game_details)

def game_format(data):
    return {
        "id": data["id"],
        "name": data["name"],
        "release_date": data["released"],
        "description": data["description"],
        "imge_url": data["background_image"],
        "rating": data["rating"],
        "platforms": [platform["platform"]["name"] for platform in data["platforms"]],
        "developers": [developer["name"] for developer in data["developers"]],
    }
        
        
        
        