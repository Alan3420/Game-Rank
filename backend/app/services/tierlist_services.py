from app.repositories.tierlist_repo import crear_tierlist, obtener_tierlist_por_id, obtener_tierlists_por_usuario, actualizar_titulo_tierlist, eliminar_tierlist, obtener_items_tierlist, obtener_item_por_id, obtener_item_por_juego, contar_items_en_rank, crear_item_tierlist, actualizar_item_tierlist, eliminar_item_tierlist


RANKS_VALIDOS = {"S", "A", "B", "C", "D"}
MAX_POR_RANK = 5


def crear_nueva_tierlist(id_user, title) -> object | str:
    try:
        if not title or not title.strip():
            return "El titulo es obligatorio"
        return crear_tierlist(id_user=id_user, title=title.strip())
    except Exception as e:
        raise Exception(f"Error al crear la tierlist: {str(e)}")


def obtener_tierlist_completa(id_tierlist, id_user) -> dict | str:
    try:
        tierlist = obtener_tierlist_por_id(id_tierlist=id_tierlist)
        if not tierlist or tierlist.id_user != id_user:
            return "Tierlist no encontrada"

        items = obtener_items_tierlist(id_tierlist=id_tierlist)
        return {**tierlist.to_dict(), "items": [i.to_dict() for i in items]}
    except Exception as e:
        raise Exception(f"Error al obtener la tierlist: {str(e)}")


def listar_tierlists_usuario(id_user) -> list:
    try:
        tierlists = obtener_tierlists_por_usuario(id_user=id_user)
        return [t.to_dict() for t in tierlists]
    except Exception as e:
        raise Exception(f"Error al listar las tierlists: {str(e)}")


def renombrar_tierlist(id_tierlist, id_user, nuevo_titulo) -> object | str:
    try:
        if not nuevo_titulo or not nuevo_titulo.strip():
            return "El titulo es obligatorio"

        tierlist = obtener_tierlist_por_id(id_tierlist=id_tierlist)
        if not tierlist or tierlist.id_user != id_user:
            return "Tierlist no encontrada"

        return actualizar_titulo_tierlist(id_tierlist=id_tierlist, nuevo_titulo=nuevo_titulo.strip())
    except Exception as e:
        raise Exception(f"Error al renombrar la tierlist: {str(e)}")


def borrar_tierlist(id_tierlist, id_user) -> bool | str:
    try:
        tierlist = obtener_tierlist_por_id(id_tierlist=id_tierlist)
        if not tierlist or tierlist.id_user != id_user:
            return "Tierlist no encontrada"
        return eliminar_tierlist(id_tierlist=id_tierlist)
    except Exception as e:
        raise Exception(f"Error al eliminar la tierlist: {str(e)}")


def agregar_juego_a_tierlist(id_tierlist, id_user, id_game_api, rank) -> object | str:
    try:
        tierlist = obtener_tierlist_por_id(id_tierlist=id_tierlist)
        if not tierlist or tierlist.id_user != id_user:
            return "Tierlist no encontrada"

        if rank not in RANKS_VALIDOS:
            return "El rank debe ser S, A, B, C o D"

        if obtener_item_por_juego(id_tierlist=id_tierlist, id_game_api=id_game_api):
            return "Este juego ya esta en la tierlist"

        if contar_items_en_rank(id_tierlist=id_tierlist, rank=rank) >= MAX_POR_RANK:
            return f"El rank {rank} ya esta lleno"

        return crear_item_tierlist(id_tierlist=id_tierlist, id_game_api=id_game_api, rank=rank)
    except Exception as e:
        raise Exception(f"Error al agregar el juego: {str(e)}")


def mover_juego_en_tierlist(id_item, id_user, nuevo_rank) -> object | str:
    try:
        item = obtener_item_por_id(id_item=id_item)
        if not item:
            return "Entrada no encontrada"

        tierlist = obtener_tierlist_por_id(id_tierlist=item.id_tierlist)
        if tierlist.id_user != id_user:
            return "No tienes permiso para modificar esta tierlist"

        if nuevo_rank not in RANKS_VALIDOS:
            return "El rank debe ser S, A, B, C o D"

        if item.rank != nuevo_rank and contar_items_en_rank(id_tierlist=item.id_tierlist, rank=nuevo_rank) >= MAX_POR_RANK:
            return f"El rank {nuevo_rank} ya esta lleno"

        return actualizar_item_tierlist(id_item=id_item, rank=nuevo_rank)
    except Exception as e:
        raise Exception(f"Error al mover el juego: {str(e)}")


def quitar_juego_de_tierlist(id_item, id_user) -> bool | str:
    try:
        item = obtener_item_por_id(id_item=id_item)
        if not item:
            return "Entrada no encontrada"

        tierlist = obtener_tierlist_por_id(id_tierlist=item.id_tierlist)
        if tierlist.id_user != id_user:
            return "No tienes permiso para modificar esta tierlist"

        return eliminar_item_tierlist(id_item=id_item)
    except Exception as e:
        raise Exception(f"Error al quitar el juego: {str(e)}")