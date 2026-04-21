from app.repositories.favorite_repo import get_favorite, get_favorites_by_user, create_favorite, delete_favorite

def añadir_favorito(id_user, id_game) -> object | str:
    try:
        existe = get_favorite(user_id=id_user, id_game=id_game)

        if existe:
            return "El juego ya está en favoritos"
        favorite = create_favorite(user_id=id_user, id_game=id_game)

        return favorite
    except Exception as e:
        raise Exception(f"Error al añadir favorito: {str(e)}")
    

def eliminar_favorito(id_user, id_game) -> bool | str:
    
    try:
        existe = get_favorite(user_id=id_user, id_game=id_game)

        if not existe:
            return "El juego no está en favoritos"
        
        resultado = delete_favorite(user_id=id_user, id_game=id_game)

        return resultado
    except Exception as e:
        raise Exception(f"Error al eliminar favorito: {str(e)}")

def get_favoritos_usuario(id_user) -> list:
    
    try:
        favorites = get_favorites_by_user(user_id=id_user)
        resultado = []

        for fav in favorites:
            resultado.append(fav.to_dict())

        return resultado
    
    except Exception as e:
        raise Exception(f"Error al obtener favoritos: {str(e)}")
    

def es_favorito(id_user, id_game) -> bool:

    try:
        favorite = get_favorite(user_id=id_user, id_game=id_game)

        if favorite:
            return True
        
        return False
    
    except Exception as e:
        raise Exception(f"Error al comprobar favorito: {str(e)}")

