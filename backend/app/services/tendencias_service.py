from app.repositories.favorite_repo import obtener_top_favoritos, obtener_top_coleccion
from app.repositories.comment_repo import obtener_top_valorados, obtener_top_comentados
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import formatear_resumen_juego
from concurrent.futures import ThreadPoolExecutor


LIMITE_POR_SECCION = 8


def _enriquecer_juego(id_juego, valor_estadistico, etiqueta_estadistica):
    try:
        datos = get_game_by_id_api(id_juego)
        resultado = formatear_resumen_juego(datos)
        resultado["stat_value"] = valor_estadistico
        resultado["stat_label"] = etiqueta_estadistica
        return resultado
    except Exception:
        return None


def _enriquecer_lista(tareas):
    # lanzamos las llamadas a RAWG en hilos para no esperar una detras de otra,
    # executor.map respeta el orden de la lista asi que el ranking se conserva
    if not tareas:
        return []

    def procesar(tarea):
        id_juego, valor, etiqueta = tarea
        return _enriquecer_juego(id_juego, valor, etiqueta)

    with ThreadPoolExecutor(max_workers=len(tareas)) as executor:
        resultados = list(executor.map(procesar, tareas))

    juegos_validos = []
    for juego in resultados:
        if juego is not None:
            juegos_validos.append(juego)
    return juegos_validos


def obtener_tendencias():
    top_favoritos  = obtener_top_favoritos(LIMITE_POR_SECCION)
    top_valorados  = obtener_top_valorados(LIMITE_POR_SECCION)
    top_comentados = obtener_top_comentados(LIMITE_POR_SECCION)
    top_coleccion  = obtener_top_coleccion(LIMITE_POR_SECCION)

    tareas_favs = []
    for fila in top_favoritos:
        id_juego = fila[0]
        total = fila[1]
        if total == 1:
            etiqueta_singular = 'favorito'
        else:
            etiqueta_singular = 'favoritos'
        etiqueta = f"{total} {etiqueta_singular}"
        tareas_favs.append((id_juego, float(total), etiqueta))

    tareas_valoradas = []
    for fila in top_valorados:
        id_juego = fila[0]
        promedio = 0.0
        if fila[1]:
            promedio = float(fila[1])
        etiqueta = f"{round(promedio, 1)} / 5"
        tareas_valoradas.append((id_juego, promedio, etiqueta))

    tareas_comentados = []
    for fila in top_comentados:
        id_juego = fila[0]
        total = fila[1]
        if total == 1:
            etiqueta_singular = 'reseña'
        else:
            etiqueta_singular = 'reseñas'
        etiqueta = f"{total} {etiqueta_singular}"
        tareas_comentados.append((id_juego, float(total), etiqueta))

    tareas_coleccion = []
    for fila in top_coleccion:
        id_juego = fila[0]
        total = fila[1]
        if total == 1:
            etiqueta_singular = 'usuario'
        else:
            etiqueta_singular = 'usuarios'
        etiqueta = f"{total} {etiqueta_singular}"
        tareas_coleccion.append((id_juego, float(total), etiqueta))

    return {
        "mas_favoritos":   _enriquecer_lista(tareas_favs),
        "mejor_valorados": _enriquecer_lista(tareas_valoradas),
        "mas_comentados":  _enriquecer_lista(tareas_comentados),
        "mas_coleccion":   _enriquecer_lista(tareas_coleccion),
    }
