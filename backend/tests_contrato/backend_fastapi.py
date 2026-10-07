from fastapi.testclient import TestClient


class BackendFastAPI:
    def __init__(self):
        from app.main import app
        from app.api.limites import limiter
        limiter.enabled = False
        self.cliente = TestClient(app, follow_redirects=False)

    def reiniciar_db(self):
        from app.database.db import db
        db.session.remove()
        db.drop_all()
        db.create_all()

    def peticion(self, metodo, ruta, json=None, token=None, params=None, cabeceras=None):
        headers = dict(cabeceras or {})
        if token:
            headers["Authorization"] = "Bearer " + token
        r = self.cliente.request(metodo, ruta, json=json, headers=headers, params=params)
        try:
            cuerpo = r.json()
        except ValueError:
            cuerpo = None
        return r.status_code, cuerpo, {k.lower(): v for k, v in r.headers.items()}
