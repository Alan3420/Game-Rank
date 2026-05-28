from app.repositories import comment_repo
from app.repositories import rate_repo


def crear_comentario(id_usuario, id_juego, descripcion) -> object | str:
    if not descripcion or len(descripcion) < 1 or len(descripcion) > 255:
        return "La descripción debe tener entre 1 y 255 caracteres"

    # Regla de negocio: un usuario solo puede tener un comentario por juego
    comentarios_del_juego = comment_repo.obtener_comentarios_por_juego(id_juego=id_juego)
    for comentario in comentarios_del_juego:
        if comentario.id_user == id_usuario:
            return "Ya has comentado este juego"

    nuevo_comentario = comment_repo.crear_comentario(
        id_usuario=id_usuario,
        id_juego=id_juego,
        descripcion=descripcion
    )
    return nuevo_comentario


def actualizar_comentario(id_comentario, descripcion, id_usuario, es_admin=False) -> object | str:
    if descripcion and (len(descripcion) < 1 or len(descripcion) > 255):
        return "La descripción debe tener entre 1 y 255 caracteres"

    comentario = comment_repo.actualizar_comentario(
        id_comentario=id_comentario,
        descripcion=descripcion,
        id_usuario=id_usuario,
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

    # Adjuntamos al comentario la nota que el mismo usuario le dio al juego
    # asi el front lo pinta junto al texto sin pedir otra cosa
    calificaciones = rate_repo.obtener_calificaciones_por_juego(id_juego=id_juego)
    calificacion_por_usuario = {}
    for calificacion in calificaciones:
        calificacion_por_usuario[calificacion.id_user] = calificacion.rating

    resultado = []
    for comentario in comentarios:
        datos = comentario.to_dict()
        datos["rating"] = calificacion_por_usuario.get(comentario.id_user)
        resultado.append(datos)

    return {
        "comments": resultado,
        "total": total,
        "has_more": (desplazamiento + len(resultado)) < total
    }


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
