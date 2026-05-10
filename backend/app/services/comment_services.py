from app.repositories.comment_repo import get_comment_by_id, get_comments_by_game,get_comments_by_user, create_comment, update_comment, delete_comment
from app.repositories.rate_repo import get_rates_by_game

def crear_comentario(id_user, id_game, description) -> object | str:
    try:
        if not description or len(description) < 1 or len(description) > 255:
            return "La descripción debe tener entre 1 y 255 caracteres"

        existing = [c for c in get_comments_by_game(id_game=id_game) if c.id_user == id_user]
        if existing:
            return "Ya has comentado este juego"
        comment = create_comment(id_user=id_user, id_game=id_game, description=description)
        return comment
    except Exception as e:
        raise Exception(f"Error al crear el comentario: {str(e)}")

def actualizar_comentario(comment_id, description) -> object | str:
    try:
        if description and (len(description) < 1 or len(description) > 255):
            return "La descripción debe tener entre 1 y 255 caracteres"

        comment = update_comment(comment_id=comment_id, description=description)
        if not comment:
            return "Comentario no encontrado"

        return comment
    except Exception as e:
        raise Exception(f"Error al actualizar el comentario: {str(e)}")

def eliminar_comentario(comment_id, user_id, es_admin=False) -> bool | str:
    try:
        resultado = delete_comment(comment_id=int(comment_id), user_id=user_id, es_admin=es_admin)

        if not resultado:
            return "Comentario no encontrado"

        return resultado
    except Exception as e:
        raise Exception(f"Error al eliminar el comentario: {str(e)}")
    
def get_comentarios_juego(id_game) -> list:
    try:
        comments = get_comments_by_game(id_game=id_game)
        rates = get_rates_by_game(id_game=id_game)
        rating_by_user = {r.id_user: r.rating for r in rates}

        resultado = []
        for comment in comments:
            data = comment.to_dict()
            data["rating"] = rating_by_user.get(comment.id_user)
            resultado.append(data)

        return resultado
    except Exception as e:
        raise Exception(f"Error al obtener comentarios: {str(e)}")

def get_comentarios_usuario(id_user) -> list:

    try:
        comments = get_comments_by_user(id_user=id_user)
        resultado = []

        for comment in comments:
            resultado.append(comment.to_dict())


        return resultado
    except Exception as e:
        raise Exception(f"Error al obtener comentarios: {str(e)}")
    


