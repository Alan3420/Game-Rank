from app.repositories.favorite_repo import obtener_top_favoritos
from app.repositories.rate_repo import obtener_top_valorados
from app.repositories.comment_repo import obtener_top_comentados
from app.repositories.user_game_status_repo import obtener_top_coleccion
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import formatear_resumen_juego
from concurrent.futures import ThreadPoolExecutor


# Servicio que calcula las tendencias de la comunidad: los juegos con
# mas favoritos, mejor valorados, mas comentados y mas anadidos a
# colecciones. Cada lista se devuelve con los datos del juego (nombre,
# imagen, etc.) listos para pintar en cards.


# Numero maximo de juegos por seccion. 8 es un buen compromiso entre
# variedad y peso de la respuesta (cada juego implica una llamada a RAWG).
LIMITE_POR_SECCION = 8


def _enriquecer_juego(id_juego, valor_estadistico, etiqueta_estadistica):
    # Pide a RAWG los datos del juego y los devuelve junto con el valor
    # numerico de la estadistica (y su etiqueta en espanol, aunque el
    # frontend la ignora y construye la suya en ingles a partir del valor).
    try:
        datos = get_game_by_id_api(id_juego)
        resultado = formatear_resumen_juego(datos)
        resultado["stat_value"] = valor_estadistico
        resultado["stat_label"] = etiqueta_estadistica
        return resultado
    except Exception:
        return None


def _enriquecer_lista(tareas):
    # Recibe una lista de tuplas (id_juego, valor, etiqueta) y llama a
    # RAWG por cada juego en paralelo con hilos. Mantenemos el orden
    # original (los mas populares primero) gracias a executor.map.
    if not tareas:
        return []

    def procesar(tarea):
        id_juego, valor, etiqueta = tarea
        return _enriquecer_juego(id_juego, valor, etiqueta)

    with ThreadPoolExecutor(max_workers=len(tareas)) as executor:
        resultados = list(executor.map(procesar, tareas))

    # Filtramos los que fallaron (None) para no devolver huecos al frontend.
    juegos_validos = []
    for juego in resultados:
        if juego is not None:
            juegos_validos.append(juego)
    return juegos_validos


def obtener_tendencias():
    # Pedimos los cuatro rankings a los repos. Cada uno hace su propia
    # query de agregacion contra la BD; aqui solo orquestamos.
    top_favoritos  = obtener_top_favoritos(LIMITE_POR_SECCION)
    top_valorados  = obtener_top_valorados(LIMITE_POR_SECCION)
    top_comentados = obtener_top_comentados(LIMITE_POR_SECCION)
    top_coleccion  = obtener_top_coleccion(LIMITE_POR_SECCION)

    # Para cada lista construimos las "tareas" (id_juego, valor, etiqueta)
    # que el helper usara para hacer las llamadas a RAWG en paralelo.
    # Las etiquetas van en espanol pero el frontend las regenera en ingles.
    tareas_favs = []
    for fila in top_favoritos:
        id_juego = fila[0]
        total = fila[1]
        etiqueta_singular = 'favorito' if total == 1 else 'favoritos'
        etiqueta = f"{total} {etiqueta_singular}"
        tareas_favs.append((id_juego, float(total), etiqueta))

    tareas_valoradas = []
    for fila in top_valorados:
        id_juego = fila[0]
        promedio = 0.0
        if fila[1]:
            promedio = float(fila[1])
        etiqueta = f"{round(promedio, 1)} / 5 ★"
        tareas_valoradas.append((id_juego, promedio, etiqueta))

    tareas_comentados = []
    for fila in top_comentados:
        id_juego = fila[0]
        total = fila[1]
        etiqueta_singular = 'reseña' if total == 1 else 'reseñas'
        etiqueta = f"{total} {etiqueta_singular}"
        tareas_comentados.append((id_juego, float(total), etiqueta))

    tareas_coleccion = []
    for fila in top_coleccion:
        id_juego = fila[0]
        total = fila[1]
        etiqueta_singular = 'usuario' if total == 1 else 'usuarios'
        etiqueta = f"{total} {etiqueta_singular}"
        tareas_coleccion.append((id_juego, float(total), etiqueta))

    return {
        "mas_favoritos":   _enriquecer_lista(tareas_favs),
        "mejor_valorados": _enriquecer_lista(tareas_valoradas),
        "mas_comentados":  _enriquecer_lista(tareas_comentados),
        "mas_coleccion":   _enriquecer_lista(tareas_coleccion),
    }
