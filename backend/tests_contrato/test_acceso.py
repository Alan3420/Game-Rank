from tests_contrato.conftest import verificar, token_caducado


def test_registro_correcto(api):
    estado, cuerpo, _ = api.registrar(1)
    verificar("acceso_registro_ok", estado, cuerpo)


def test_registro_email_repetido(api):
    api.registrar(1)
    estado, cuerpo, _ = api.registrar(2, email="jugador1@gmail.com")
    verificar("acceso_registro_email_repetido", estado, cuerpo)


def test_registro_nickname_repetido(api):
    api.registrar(1)
    estado, cuerpo, _ = api.registrar(2, nickname="jugador_1")
    verificar("acceso_registro_nickname_repetido", estado, cuerpo)


def test_login_correcto(api):
    api.registrar(1)
    estado, cuerpo, _ = api.post("/user/login", json={"email": "jugador1@gmail.com", "password": "Clave12345"})
    verificar("acceso_login_ok", estado, cuerpo)


def test_login_incorrecto(api):
    api.registrar(1)
    estado, cuerpo, _ = api.post("/user/login", json={"email": "jugador1@gmail.com", "password": "Mala99999"})
    verificar("acceso_login_incorrecto", estado, cuerpo)


def test_me_con_token(api):
    token = api.usuario_con_token(1)
    estado, cuerpo, _ = api.get("/user/me", token=token)
    verificar("acceso_me_ok", estado, cuerpo)


def test_me_sin_token(api):
    estado, cuerpo, _ = api.get("/user/me")
    verificar("acceso_me_sin_token", estado, cuerpo)


def test_me_token_invalido(api):
    estado, cuerpo, _ = api.get("/user/me", token="esto.no.es-un-token")
    verificar("acceso_me_token_invalido", estado, cuerpo)


def test_me_token_caducado(api):
    api.registrar(1)
    estado, cuerpo, _ = api.get("/user/me", token=token_caducado(api.id_de(1)))
    verificar("acceso_me_token_caducado", estado, cuerpo)


def test_me_usuario_borrado(api):
    token = api.usuario_con_token(1)
    api.delete("/settings/account", token=token)
    estado, cuerpo, _ = api.get("/user/me", token=token)
    verificar("acceso_me_usuario_borrado", estado, cuerpo)
