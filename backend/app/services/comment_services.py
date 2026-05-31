from app.repositories import comment_repo


def crear_comentario(id_usuario, id_juego, descripcion, rating) -> object | str:
    if not descripcion or len(descripcion) < 1 or len(descripcion) > 255:
        return "La descripción debe tener entre 1 y 255 caracteres"

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return "El rating debe ser un número entero entre 1 y 5"

    # uun usuario solo puede tener un comentario por juego
    comentarios_del_juego = comment_repo.obtener_comentarios_por_juego(id_juego=id_juego)
    for comentario in comentarios_del_juego:
        if comentario.id_user == id_usuario:
            return "Ya has comentado este juego"

    nuevo_comentario = comment_repo.crear_comentario(
        id_usuario=id_usuario,
        id_juego=id_juego,
        descripcion=descripcion,
        rating=rating
    )
    return nuevo_comentario


def actualizar_comentario(id_comentario, descripcion, id_usuario, rating=None, es_admin=False) -> object | str:
    if descripcion and (len(descripcion) < 1 or len(descripcion) > 255):
        return "La descripción debe tener entre 1 y 255 caracteres"

    if rating is not None and (not isinstance(rating, int) or rating < 1 or rating > 5):
        return "El rating debe ser un número entero entre 1 y 5"

    comentario = comment_repo.actualizar_comentario(
        id_comentario=id_comentario,
        descripcion=descripcion,
        id_usuario=id_usuario,
        rating=rating,
        es_admin=es_admin
    )

    if not comentario:
        return "Comentario no encontrado"

    return comentario


def eliminar_comentario(id_comentario, id_usuario, es_admin=False) -> bool | str:
    resultado = comment_repo.eliminar_comentario(
        id_comentario=int(id_comentario),
        id_usuario=id_usuario,
        es_admin=es_admin
    )

    if not resultado:
        return "Comentario no encontrado"

    return resultado


def obtener_comentarios_del_juego(id_juego, limite=10, desplazamiento=0) -> dict:
    comentarios, total = comment_repo.obtener_comentarios_por_juego_paginados(
        id_juego=id_juego,
        limite=limite,
        desplazamiento=desplazamiento
    )

    resultado = []
    for comentario in comentarios:
        resultado.append(comentario.to_dict())

    return {
        "comments": resultado,
        "total": total,
        "has_more": (desplazamiento + len(resultado)) < total
    }


def obtener_promedio_del_juego(id_juego) -> float:
    return comment_repo.obtener_promedio_por_juego(id_juego=id_juego)


def obtener_todos_los_comentarios() -> list:
    comentarios = comment_repo.obtener_todos_los_comentarios()

    resultado = []
    for comentario in comentarios:
        datos = comentario.to_dict()
        if comentario.users_rl:
            datos['user_last_name'] = comentario.users_rl.last_name
        else:
            datos['user_last_name'] = ''
        resultado.append(datos)

    return resultado


def obtener_comentarios_del_usuario(id_usuario) -> list:
    comentarios = comment_repo.obtener_comentarios_por_usuario(id_usuario=id_usuario)

    resultado = []
    for comentario in comentarios:
        resultado.append(comentario.to_dict())

    return resultado
