from tests_contrato.conftest import verificar


def test_editar_perfil(api):
    t1 = api.usuario_con_token(1)
    api.registrar(2)
    id1, id2 = api.id_de(1), api.id_de(2)

    verificar("cuenta_editar_propio", *api.put("/settings/options", json={"id_user": id1, "name": "Nuevo", "last_name": "Apellido1", "nickname": "nuevo_nick"}, token=t1)[:2])
    verificar("cuenta_editar_nick_ocupado", *api.put("/settings/options", json={"id_user": id1, "name": "Nuevo", "last_name": "Apellido1", "nickname": "jugador_2"}, token=t1)[:2])
    verificar("cuenta_editar_ajeno", *api.put("/settings/options", json={"id_user": id2, "name": "X", "last_name": "Y"}, token=t1)[:2])


def test_contrasena(api):
    t1 = api.usuario_con_token(1)
    verificar("cuenta_pwd_incompleta", *api.put("/settings/change-password", json={"current_password": "Clave12345"}, token=t1)[:2])
    verificar("cuenta_pwd_actual_mala", *api.put("/settings/change-password", json={"current_password": "Mala00000", "new_password": "Nueva12345"}, token=t1)[:2])
    verificar("cuenta_pwd_ok", *api.put("/settings/change-password", json={"current_password": "Clave12345", "new_password": "Nueva12345"}, token=t1)[:2])
    estado, _, _ = api.post("/user/login", json={"email": "jugador1@gmail.com", "password": "Nueva12345"})
    assert estado == 200


def test_estadisticas(api):
    t1 = api.usuario_con_token(1)
    api.post("/favorite/add", json={"id_game": 101, "status": "jugando"}, token=t1)
    api.post("/favorite/add", json={"id_game": 102}, token=t1)
    api.post("/comment/create", json={"id_game": 101, "description": "Bien", "rating": 4}, token=t1)
    verificar("cuenta_stats", *api.get("/settings/stats", token=t1)[:2])


def test_administracion_de_usuarios(api):
    t1 = api.usuario_con_token(1)
    api.registrar(2)
    api.registrar(3)
    id2 = api.id_de(2)

    verificar("admin_lista_no_admin", *api.get("/settings/options", token=t1)[:2])
    api.hacer_admin(1)
    verificar("admin_lista", *api.get("/settings/options", token=t1)[:2])
    verificar("admin_rol_ok", *api.put("/settings/change-role", json={"id_user": id2, "new_role": "admin"}, token=t1)[:2])
    verificar("admin_rol_invalido", *api.put("/settings/change-role", json={"id_user": id2, "new_role": "jefe"}, token=t1)[:2])
    verificar("admin_rol_incompleto", *api.put("/settings/change-role", json={"id_user": id2}, token=t1)[:2])
    verificar("admin_rol_no_existe", *api.put("/settings/change-role", json={"id_user": 9999, "new_role": "user"}, token=t1)[:2])
    verificar("admin_editar_ajeno", *api.put("/settings/options", json={"id_user": id2, "name": "Editado", "last_name": "Por admin"}, token=t1)[:2])
    verificar("admin_borrar_ok", *api.delete("/settings/options", json={"id_user": id2}, token=t1)[:2])
    verificar("admin_borrar_no_existe", *api.delete("/settings/options", json={"id_user": 9999}, token=t1)[:2])


def test_borrar_cuenta_propia(api):
    t1 = api.usuario_con_token(1)
    api.post("/favorite/add", json={"id_game": 101}, token=t1)
    api.post("/comment/create", json={"id_game": 101, "description": "Bien", "rating": 4}, token=t1)
    verificar("cuenta_borrar_ok", *api.delete("/settings/account", token=t1)[:2])
    verificar("cuenta_borrar_otra_vez", *api.delete("/settings/account", token=t1)[:2])
    estado, _, _ = api.post("/user/login", json={"email": "jugador1@gmail.com", "password": "Clave12345"})
    assert estado == 401
