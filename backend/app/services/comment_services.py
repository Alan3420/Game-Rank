from app.repositories import comment_repo
from app.repositories import rate_repo


# Servicio que orquesta las operaciones de comentarios.
# Una regla importante: un usuario solo puede tener UN comentario por juego.
# La regla se aplica en crear_comentario(), no a nivel de constraint de BD.


def crear_comentario(id_usuario, id_juego, descripcion) -> object | str:
    if not descripcion or len(descripcion) < 1 or len(descripcion) > 255:
        return "La descripción debe tener entre 1 y 255 caracteres"

    # Buscamos si el usuario ya tiene un comentario en este juego. No usamos
    # una constraint UNIQUE en la BD porque queremos un mensaje legible
    # y porque la regla podria relajarse en el futuro.
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

    # El repo ya filtra por id_user salvo que es_admin sea True.
    # Si el comentario no existe (o el usuario no es el autor y no es admin)
    # devuelve None y nosotros traducimos a mensaje legible.
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
    # Devolvemos los comentarios paginados + el total + un flag "has_more"
    # para que el frontend sepa si debe mostrar el boton "Load more".
    comentarios, total = comment_repo.obtener_comentarios_por_juego_paginados(
        id_juego=id_juego,
        limite=limite,
        desplazamiento=desplazamiento
    )

    # Enganchamos a cada comentario la nota que ese usuario dio al juego,
    # para pintarla junto al texto sin tener que hacer otra llamada desde
    # el frontend.
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
    # Solo el admin. Anadimos el apellido del autor para que en el panel
    # se vea "Nombre Apellido" sin tener que hacer otra peticion.
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
