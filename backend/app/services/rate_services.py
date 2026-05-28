from app.repositories import rate_repo


def crear_calificacion(id_usuario, id_juego, valor) -> object | str:
    # El 0 sirve para que el usuario pueda "limpiar" su nota desde el form
    if not isinstance(valor, int) or valor < 0 or valor > 5:
        return "La valoración debe ser un número entero entre 0 y 5"

    if rate_repo.obtener_calificacion_por_usuario_y_juego(id_usuario=id_usuario, id_juego=id_juego):
        return "Ya has valorado este juego"

    return rate_repo.crear_calificacion(id_usuario=id_usuario, id_juego=id_juego, valor=valor)


def actualizar_calificacion(id_usuario, id_juego, valor=None) -> object | str:
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
