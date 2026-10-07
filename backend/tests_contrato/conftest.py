# Tests de contrato de la API: comparan cada respuesta con la referencia
# grabada desde la version Flask antes de migrar a FastAPI (referencias/).
# Si un cambio de la API es intencionado, se regraban con CONTRATO_GRABAR=1.
# Van fuera de tests/ porque aquel conftest sustituye modulos por mocks.
import os
import re
import json
import tempfile
from datetime import date, datetime, timedelta, timezone

# El entorno se fija antes de importar la app: load_dotenv no pisa
# variables que ya existen, asi nunca se toca la base de Aiven
_dir_tmp = tempfile.mkdtemp(prefix="contrato_")
RUTA_DB = os.path.join(_dir_tmp, "contrato.db").replace("\\", "/")
# CONTRATO_DB_URI permite pasar los mismos tests contra MySQL (docker)
os.environ["DB_URI"] = os.getenv("CONTRATO_DB_URI") or ("sqlite:///" + RUTA_DB)
os.environ["SECRET_KEY"] = "clave-de-pruebas-del-contrato-0123456789abcdef"
os.environ["RAWG_API_KEY"] = "falsa"
os.environ.pop("FRONTEND_ORIGIN", None)

import jwt as pyjwt
import pytest
from sqlalchemy import create_engine, text

from tests_contrato import rawg_falso

GRABAR = os.getenv("CONTRATO_GRABAR") == "1"
DIR_REFERENCIAS = os.path.join(os.path.dirname(__file__), "referencias")
CLAVE = os.environ["SECRET_KEY"]


def _crear_backend():
    from tests_contrato.backend_fastapi import BackendFastAPI
    return BackendFastAPI()


_backend = None


@pytest.fixture(scope="session")
def backend_sesion():
    global _backend
    if _backend is None:
        _backend = _crear_backend()
    return _backend


@pytest.fixture(autouse=True)
def rawg_simulado(monkeypatch):
    import app.client.clientRAWG as cliente_rawg
    monkeypatch.setattr(cliente_rawg, "_peticion_con_cache", rawg_falso.peticion_falsa)
    # el video del hero baraja la lista: sin barajar, la respuesta es fija
    import app.services.game_services as servicios_juego
    monkeypatch.setattr(servicios_juego.random, "shuffle", lambda lista: None)
    yield


@pytest.fixture
def api(backend_sesion):
    backend_sesion.reiniciar_db()
    return Api(backend_sesion)


class Api:
    def __init__(self, backend):
        self.backend = backend
        self.motor = create_engine(os.environ["DB_URI"])

    def get(self, ruta, **kw):
        return self.backend.peticion("GET", ruta, **kw)

    def post(self, ruta, **kw):
        return self.backend.peticion("POST", ruta, **kw)

    def put(self, ruta, **kw):
        return self.backend.peticion("PUT", ruta, **kw)

    def delete(self, ruta, **kw):
        return self.backend.peticion("DELETE", ruta, **kw)

    def options(self, ruta, **kw):
        return self.backend.peticion("OPTIONS", ruta, **kw)

    # ── ayudas para preparar datos a traves de la propia API ──
    def registrar(self, n=1, **extra):
        datos = {
            "name": f"Nombre{n}", "last_name": f"Apellido{n}", "nickname": f"jugador_{n}",
            "email": f"jugador{n}@gmail.com", "password": "Clave12345",
        }
        datos.update(extra)
        return self.post("/user/register", json=datos)

    def entrar(self, n=1, password="Clave12345"):
        estado, cuerpo, _ = self.post("/user/login", json={"email": f"jugador{n}@gmail.com", "password": password})
        assert estado == 200, cuerpo
        return cuerpo["token"]

    def usuario_con_token(self, n=1):
        self.registrar(n)
        return self.entrar(n)

    def hacer_admin(self, n=1):
        with self.motor.begin() as con:
            con.execute(text("UPDATE users SET role='admin' WHERE email=:e"), {"e": f"jugador{n}@gmail.com"})

    def id_de(self, n=1):
        with self.motor.connect() as con:
            return con.execute(text("SELECT id_user FROM users WHERE email=:e"), {"e": f"jugador{n}@gmail.com"}).scalar()


def token_caducado(id_usuario=1):
    ahora = datetime.now(timezone.utc)
    carga = {"sub": str(id_usuario), "type": "access", "fresh": False, "jti": "x",
             "iat": ahora - timedelta(hours=3), "nbf": ahora - timedelta(hours=3), "exp": ahora - timedelta(hours=1)}
    return pyjwt.encode(carga, CLAVE, algorithm="HS256")


# ── normalizacion y comparacion con la referencia ──
_HOY = date.today()
_HOY_ISO = _HOY.isoformat()
_HOY_RFC = _HOY.strftime("%a, %d %b %Y 00:00:00 GMT")
_JWT = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")


def normalizar(valor):
    # La fecha de hoy y los tokens cambian en cada ejecucion: se sustituyen
    # por marcadores que conservan su FORMATO (rfc1123 frente a iso)
    if isinstance(valor, dict):
        return {k: normalizar(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [normalizar(v) for v in valor]
    if isinstance(valor, str):
        if valor == _HOY_ISO:
            return "<hoy-iso>"
        if valor == _HOY_RFC:
            return "<hoy-rfc1123>"
        if _JWT.match(valor) and len(valor) > 60:
            return "<jwt>"
    return valor


def verificar(nombre, estado, cuerpo):
    obtenido = {"status": estado, "cuerpo": normalizar(cuerpo)}
    ruta = os.path.join(DIR_REFERENCIAS, nombre + ".json")
    if GRABAR:
        os.makedirs(DIR_REFERENCIAS, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(obtenido, f, ensure_ascii=False, indent=2, sort_keys=True)
        return
    assert os.path.exists(ruta), f"Falta la referencia {nombre}: graba con CONTRATO_GRABAR=1 contra Flask"
    with open(ruta, encoding="utf-8") as f:
        esperado = json.load(f)
    assert obtenido == esperado, f"El contrato de {nombre} ha cambiado"
