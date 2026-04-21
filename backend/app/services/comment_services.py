from app.repositories.comment_repo import get_comment_by_id, get_comments_by_game,get_comments_by_user, create_comment, update_comment, delete_comment

def crear_comentario(id_user, id_game, description) -> object | str:
    try:
        comment = create_comment(id_user=id_user, id_game=id_game, description=description)
        return comment
    except Exception as e:
        raise Exception(f"Error al crear el comentario: {str(e)}")

def actualizar_comentario(comment_id, description) -> object | str:
    try:
        comment = update_comment(comment_id=comment_id, description=description)
        if not comment:
            return "Comentario no encontrado"
        
        return comment
    except Exception as e:
        raise Exception(f"Error al actualizar el comentario: {str(e)}")

def eliminar_comentario(comment_id) -> bool | str:
    try:
        resultado = delete_comment(comment_id=comment_id)
        if not resultado:
            return "Comentario no encontrado"
        return resultado
    except Exception as e:
        raise Exception(f"Error al eliminar el comentario: {str(e)}")
    
def get_comentarios_juego(id_game) -> list:
    try:
        comments = get_comments_by_game(id_game=id_game)
        resultado = []

        for comment in comments:
            resultado.append(comment.to_dict())

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
    


