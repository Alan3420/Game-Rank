from datetime import datetime
from app.models.TierList import TierList
from app.models.TierListItem import TierListItem
from app.database.db import db


def crear_tierlist(id_user, title) -> TierList:
    tierlist = TierList(id_user=id_user, title=title)
    db.session.add(tierlist)
    db.session.commit()
    return tierlist


def obtener_tierlist_por_id(id_tierlist) -> TierList | None:
    return TierList.query.filter_by(id_tierlist=id_tierlist).first()


def obtener_tierlists_por_usuario(id_user) -> list[TierList]:
    return TierList.query.filter_by(id_user=id_user).all()


def actualizar_titulo_tierlist(id_tierlist, nuevo_titulo) -> TierList | None:
    tierlist = obtener_tierlist_por_id(id_tierlist=id_tierlist)
    if not tierlist:
        return None
    tierlist.title = nuevo_titulo
    tierlist.date_modified = datetime.today()
    db.session.commit()
    return tierlist


def eliminar_tierlist(id_tierlist) -> bool:
    tierlist = obtener_tierlist_por_id(id_tierlist=id_tierlist)
    if not tierlist:
        return False
    db.session.delete(tierlist)
    db.session.commit()
    return True


def obtener_items_tierlist(id_tierlist) -> list[TierListItem]:
    return TierListItem.query.filter_by(id_tierlist=id_tierlist).all()


def obtener_item_por_id(id_item) -> TierListItem | None:
    return TierListItem.query.filter_by(id_item=id_item).first()


def obtener_item_por_juego(id_tierlist, id_game_api) -> TierListItem | None:
    return TierListItem.query.filter_by(
        id_tierlist=id_tierlist, id_game_api=id_game_api
    ).first()


def contar_items_en_rank(id_tierlist, rank) -> int:
    return TierListItem.query.filter_by(
        id_tierlist=id_tierlist, rank=rank
    ).count()


def crear_item_tierlist(id_tierlist, id_game_api, rank) -> TierListItem:
    item = TierListItem(
        id_tierlist=id_tierlist,
        id_game_api=id_game_api,
        rank=rank
    )
    db.session.add(item)
    db.session.commit()
    return item


def actualizar_item_tierlist(id_item, rank=None) -> TierListItem | None:
    item = obtener_item_por_id(id_item=id_item)
    if not item:
        return None
    if rank is not None:
        item.rank = rank
    db.session.commit()
    return item


def eliminar_item_tierlist(id_item) -> bool:
    item = obtener_item_por_id(id_item=id_item)
    if not item:
        return False
    db.session.delete(item)
    db.session.commit()
    return True