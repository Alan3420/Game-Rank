import os
import threading
from contextvars import ContextVar
from dotenv import load_dotenv
from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

# SQLAlchemy sin Flask: la usan la app, Alembic, la seed y los tests.
# El .env se carga aqui tambien por si este modulo se importa primero
# (load_dotenv no pisa variables que ya existan)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

_RUTA_CERTIFICADO_CA = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ca.pem')


_HOSTS_LOCALES = {"localhost", "127.0.0.1", "mysql", "db", "host.docker.internal"}


def _usar_ssl(url):
    # ca.pem es el certificado de Aiven: solo para un MySQL remoto. Un MySQL
    # local (docker-compose) no tiene ese certificado y rechazaria la
    # conexion. DB_SSL=true|false lo fuerza en cualquier sentido.
    forzado = (os.getenv("DB_SSL") or "").lower()
    if forzado in ("true", "false"):
        return forzado == "true"
    return url.get_backend_name() == "mysql" and url.host not in _HOSTS_LOCALES


def _crear_motor():
    url = make_url(os.getenv("DB_URI"))
    # pool_pre_ping y pool_recycle hacen falta porque en produccion las
    # conexiones se quedan colgadas y MySQL las tira ("gone away")
    opciones = {"pool_pre_ping": True, "pool_recycle": 280}
    if _usar_ssl(url) and os.path.exists(_RUTA_CERTIFICADO_CA):
        opciones["connect_args"] = {"ssl": {"ca": _RUTA_CERTIFICADO_CA}}
    return create_engine(url, **opciones)


engine = _crear_motor()

# Una sesion por peticion. FastAPI ejecuta cada endpoint en un hilo de un
# pool, asi que el ambito no puede ser el hilo: un middleware fija aqui un
# identificador por peticion (ContextVar, que pasa al hilo del endpoint).
# Fuera de una peticion (seed, scripts, Flask) el ambito es el hilo.
ambito_peticion = ContextVar("ambito_peticion_db", default=None)


def _clave_ambito():
    valor = ambito_peticion.get()
    if valor is not None:
        return valor
    return threading.get_ident()


# quien atiende la peticion la cierra al terminar con session.remove()
session = scoped_session(sessionmaker(bind=engine), scopefunc=_clave_ambito)


class Base(DeclarativeBase):
    pass


# Mantiene Modelo.query como con Flask-SQLAlchemy, asi los repositorios
# no cambian
Base.query = session.query_property()


class _BaseDeDatos:
    # Envoltorio con la misma forma que el db de Flask-SQLAlchemy
    # (db.session, db.create_all...) para no tocar los repositorios
    Model = Base
    metadata = Base.metadata

    @property
    def session(self):
        return session

    @property
    def engine(self):
        return engine

    def create_all(self):
        Base.metadata.create_all(engine)

    def drop_all(self):
        Base.metadata.drop_all(engine)


db = _BaseDeDatos()
