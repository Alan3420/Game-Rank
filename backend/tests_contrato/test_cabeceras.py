ORIGEN_OK = "https://gamerk.netlify.app"


def test_cabeceras_de_seguridad(api):
    _, _, cabeceras = api.get("/content/hero-video")
    assert cabeceras.get("x-content-type-options") == "nosniff"
    assert cabeceras.get("x-frame-options") == "DENY"
    assert cabeceras.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert cabeceras.get("permissions-policy") == "geolocation=(), microphone=(), camera=()"


def test_cors_origen_permitido(api):
    estado, _, cabeceras = api.options("/user/login", cabeceras={
        "Origin": ORIGEN_OK,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type,authorization",
    })
    assert estado in (200, 204)
    assert cabeceras.get("access-control-allow-origin") == ORIGEN_OK


def test_cors_origen_no_permitido(api):
    _, _, cabeceras = api.get("/content/hero-video", cabeceras={"Origin": "https://malicioso.example"})
    assert "access-control-allow-origin" not in cabeceras
