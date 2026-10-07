from tests_contrato.conftest import verificar


def _comentar(api, token, juego=101, texto="Muy bueno", rating=4):
    return api.post("/comment/create", json={"id_game": juego, "description": texto, "rating": rating}, token=token)


def test_crear_y_leer_comentarios(api):
    t1 = api.usuario_con_token(1)
    t2 = api.usuario_con_token(2)

    verificar("com_crear_ok", *_comentar(api, t1)[:2])
    verificar("com_crear_repetido", *_comentar(api, t1)[:2])
    verificar("com_crear_incompleto", *api.post("/comment/create", json={"id_game": 101}, token=t1)[:2])
    verificar("com_crear_largo", *_comentar(api, t2, texto="x" * 256)[:2])
    verificar("com_crear_rating_malo", *_comentar(api, t2, rating=9)[:2])
    _comentar(api, t2, texto="Regular", rating=2)

    verificar("com_juego", *api.get("/comment/game/101", token=t1)[:2])
    verificar("com_juego_paginado", *api.get("/comment/game/101", token=t1, params={"limit": 1, "offset": 1})[:2])
    verificar("com_juego_vacio", *api.get("/comment/game/999", token=t1)[:2])
    verificar("com_media", *api.get("/comment/avg/101", token=t1)[:2])
    verificar("com_media_vacia", *api.get("/comment/avg/999", token=t1)[:2])
    verificar("com_usuario", *api.get("/comment/user", token=t1)[:2])


def test_editar_y_borrar_comentarios(api):
    t1 = api.usuario_con_token(1)
    t2 = api.usuario_con_token(2)
    _comentar(api, t1)
    id_com = api.get("/comment/user", token=t1)[1]["comments"][0]["id_comment"]

    verificar("com_editar_ok", *api.put(f"/comment/update/{id_com}", json={"description": "Editado", "rating": 5}, token=t1)[:2])
    verificar("com_editar_sin_texto", *api.put(f"/comment/update/{id_com}", json={"rating": 5}, token=t1)[:2])
    verificar("com_editar_ajeno", *api.put(f"/comment/update/{id_com}", json={"description": "No", "rating": 1}, token=t2)[:2])
    verificar("com_editar_no_existe", *api.put("/comment/update/9999", json={"description": "No", "rating": 1}, token=t1)[:2])

    verificar("com_borrar_ajeno", *api.delete(f"/comment/delete/{id_com}", token=t2)[:2])
    verificar("com_borrar_ok", *api.delete(f"/comment/delete/{id_com}", token=t1)[:2])
    verificar("com_borrar_no_existe", *api.delete(f"/comment/delete/{id_com}", token=t1)[:2])


def test_admin_comentarios(api):
    t1 = api.usuario_con_token(1)
    t2 = api.usuario_con_token(2)
    _comentar(api, t2)
    verificar("com_todos_no_admin", *api.get("/comment/all", token=t1)[:2])
    api.hacer_admin(1)
    verificar("com_todos_admin", *api.get("/comment/all", token=t1)[:2])
    id_com = api.get("/comment/user", token=t2)[1]["comments"][0]["id_comment"]
    verificar("com_admin_edita_ajeno", *api.put(f"/comment/update/{id_com}", json={"description": "Moderado", "rating": 3}, token=t1)[:2])
    verificar("com_admin_borra_ajeno", *api.delete(f"/comment/delete/{id_com}", token=t1)[:2])
