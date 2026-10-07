from tests_contrato.conftest import verificar


def test_flujo_completo_de_favoritos(api):
    token = api.usuario_con_token(1)

    verificar("fav_add_ok", *api.post("/favorite/add", json={"id_game": 101}, token=token)[:2])
    verificar("fav_add_con_estado", *api.post("/favorite/add", json={"id_game": 102, "status": "jugando"}, token=token)[:2])
    verificar("fav_add_repetido", *api.post("/favorite/add", json={"id_game": 101}, token=token)[:2])
    verificar("fav_add_estado_invalido", *api.post("/favorite/add", json={"id_game": 103, "status": "otro"}, token=token)[:2])
    verificar("fav_add_sin_id", *api.post("/favorite/add", json={}, token=token)[:2])

    verificar("fav_check_si", *api.get("/favorite/check/101", token=token)[:2])
    verificar("fav_check_no", *api.get("/favorite/check/999", token=token)[:2])

    verificar("fav_status_put_ok", *api.put("/favorite/status", json={"id_game": 101, "status": "completado"}, token=token)[:2])
    verificar("fav_status_put_incompleto", *api.put("/favorite/status", json={"id_game": 101}, token=token)[:2])
    verificar("fav_status_put_invalido", *api.put("/favorite/status", json={"id_game": 101, "status": "otro"}, token=token)[:2])

    verificar("fav_status_get_ok", *api.get("/favorite/status/101", token=token)[:2])
    verificar("fav_status_get_ninguno", *api.get("/favorite/status/999", token=token)[:2])

    verificar("fav_listfav", *api.get("/favorite/listFav", token=token)[:2])
    verificar("fav_list", *api.get("/favorite/list", token=token)[:2])
    verificar("fav_list_full", *api.get("/favorite/list/full", token=token)[:2])

    verificar("fav_status_delete_ok", *api.delete("/favorite/status/101", token=token)[:2])
    verificar("fav_status_delete_no_existe", *api.delete("/favorite/status/999", token=token)[:2])

    verificar("fav_remove_ok", *api.delete("/favorite/remove", json={"id_game": 101}, token=token)[:2])
    verificar("fav_remove_no_existe", *api.delete("/favorite/remove", json={"id_game": 101}, token=token)[:2])
    verificar("fav_remove_sin_id", *api.delete("/favorite/remove", json={}, token=token)[:2])


def test_favoritos_sin_token(api):
    verificar("fav_list_sin_token", *api.get("/favorite/list")[:2])
