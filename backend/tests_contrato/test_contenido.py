from tests_contrato.conftest import verificar


def test_contenido_de_juegos(api):
    t = api.usuario_con_token(1)
    verificar("cont_detalle", *api.get("/content/overview/101", token=t)[:2])
    verificar("cont_adicciones", *api.get("/content/overview/101/adicciones", token=t)[:2])
    verificar("cont_saga", *api.get("/content/overview/101/saga", token=t)[:2])
    verificar("cont_logros", *api.get("/content/overview/101/logros", token=t)[:2])


def test_listados(api):
    t = api.usuario_con_token(1)
    verificar("cont_catalogo", *api.get("/content/catalog", token=t, params={"page": 2, "per_page": 5})[:2])
    verificar("cont_catalogo_pagina_no_numerica", *api.get("/content/catalog", token=t, params={"page": "abc"})[:2])
    verificar("cont_lanzamientos", *api.get("/content/release", token=t, params={"page": 1, "per_page": 5})[:2])
    verificar("cont_filtrados", *api.get("/content/filtered", token=t, params={"page": 1, "per_page": 20, "ordering": "-added", "genres": "4,5", "search": "alpha"})[:2])


def test_video_publico(api):
    verificar("cont_hero_video", *api.get("/content/hero-video")[:2])


def test_contenido_sin_token(api):
    verificar("cont_catalogo_sin_token", *api.get("/content/catalog")[:2])


def test_tendencias(api):
    t1 = api.usuario_con_token(1)
    t2 = api.usuario_con_token(2)
    t3 = api.usuario_con_token(3)
    for t in (t1, t2, t3):
        api.post("/favorite/add", json={"id_game": 101, "status": "completado"}, token=t)
        api.post("/comment/create", json={"id_game": 101, "description": "Top", "rating": 5}, token=t)
    api.post("/favorite/add", json={"id_game": 102, "status": "jugando"}, token=t1)
    api.post("/comment/create", json={"id_game": 102, "description": "Bien", "rating": 3}, token=t1)
    verificar("tendencias", *api.get("/tendencias/", token=t1)[:2])
