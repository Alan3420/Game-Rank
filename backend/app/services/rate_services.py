from app.repositories import rate_repo


# Servicio de calificaciones (1-5 estrellas) de los usuarios sobre juegos.
# Solo se permite una calificacion por usuario y juego. La restriccion la
# garantiza la PK compuesta de la tabla rates ademas de esta validacion.


def crear_calificacion(id_usuario, id_juego, valor) -> object | str:
    # Validacion del valor. Aceptamos 0 a 5 para que tambien se pueda
    # "limpiar" una calificacion poniendola a 0 desde el formulario.
    if not isinstance(valor, int) or valor < 0 or valor > 5:
        return "La valoración debe ser un número entero entre 0 y 5"

    if rate_repo.obtener_calificacion_por_usuario_y_juego(id_usuario=id_usuario, id_juego=id_juego):
        return "Ya has valorado este juego"

    return rate_repo.crear_calificacion(id_usuario=id_usuario, id_juego=id_juego, valor=valor)


def actualizar_calificacion(id_usuario, id_juego, valor=None) -> object | str:
    # Mismo rango de validacion que en crear. El valor es opcional para
    # poder usar este metodo solo para "tocar" el registro en el futuro.
    if valor is not None:
        if not isinstance(valor, int) or valor < 0 or valor > 5:
            return "La valoración debe ser un número entero entre 0 y 5"

    calificacion = rate_repo.actualizar_calificacion(id_usuario=id_usuario, id_juego=id_juego, valor=valor)

    if not calificacion:
        return "Valoración no encontrada"

    return calificacion


def eliminar_calificacion(id_usuario, id_juego) -> bool | str:
    resultado = rate_repo.eliminar_calificacion(id_usuario=id_usuario, id_juego=id_juego)

    if not resultado:
        return "Valoración no encontrada"

    return resultado


def obtener_promedio_del_juego(id_juego) -> float:
    # Devuelve la media de todas las calificaciones que tiene el juego.
    # Si no hay ninguna devolvemos 0.0 para que el frontend pinte un "—".
    calificaciones = rate_repo.obtener_calificaciones_por_juego(id_juego=id_juego)

    if not calificaciones:
        return 0.0

    suma_total = 0
    for c in calificaciones:
        suma_total = suma_total + c.rating

    promedio = suma_total / len(calificaciones)
    return round(promedio, 2)


def obtener_calificaciones_del_juego(id_juego) -> list:
    calificaciones = rate_repo.obtener_calificaciones_por_juego(id_juego=id_juego)

    resultado = []
    for c in calificaciones:
        resultado.append(c.to_dict())
    return resultado


def obtener_calificaciones_del_usuario(id_usuario) -> list:
    calificaciones = rate_repo.obtener_calificaciones_por_usuario(id_usuario=id_usuario)

    resultado = []
    for c in calificaciones:
        resultado.append(c.to_dict())
    return resultado
