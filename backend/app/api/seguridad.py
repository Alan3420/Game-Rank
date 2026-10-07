import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Request

from app.api.respuestas import ErrorApi
from app.repositories.user_repo import obtener_usuario_por_id

DURACION_TOKEN = timedelta(hours=2)
ALGORITMO = "HS256"


def _clave():
    return os.getenv("SECRET_KEY")


def crear_token(id_usuario):
    # Mismos campos que los tokens de flask-jwt-extended: los tokens que ya
    # tienen los usuarios siguen valiendo tras la migracion y viceversa
    ahora = datetime.now(timezone.utc)
    carga = {
        "fresh": False,
        "iat": ahora,
        "jti": str(uuid.uuid4()),
        "type": "access",
        "sub": str(id_usuario),
        "nbf": ahora,
        "csrf": str(uuid.uuid4()),
        "exp": ahora + DURACION_TOKEN,
    }
    return jwt.encode(carga, _clave(), algorithm=ALGORITMO)


def _token_de_cabecera(request: Request):
    cabecera = request.headers.get("Authorization")
    if not cabecera:
        return None
    partes = cabecera.split(" ")
    if len(partes) != 2 or partes[0] != "Bearer" or not partes[1]:
        return None
    return partes[1]


def leer_identidad(request: Request, obligatorio=True):
    # Mismos mensajes que los callbacks de JWTManager en la version Flask
    token = _token_de_cabecera(request)
    if token is None:
        if obligatorio:
            raise ErrorApi(401, {"message": "Token no válido"})
        return None
    try:
        carga = jwt.decode(token, _clave(), algorithms=[ALGORITMO])
    except jwt.ExpiredSignatureError:
        if obligatorio:
            raise ErrorApi(401, {"message": "Token expirado"})
        return None
    except jwt.PyJWTError:
        if obligatorio:
            raise ErrorApi(401, {"message": "Token inválido"})
        return None
    if carga.get("type") != "access" or "sub" not in carga:
        if obligatorio:
            raise ErrorApi(401, {"message": "Token inválido"})
        return None
    return carga["sub"]


def id_usuario_actual(request: Request) -> str:
    # Dependencia: equivale a @jwt_required() + get_jwt_identity()
    return leer_identidad(request)


def admin_requerido(request: Request) -> str:
    # Dependencia: equivale a @jwt_required() + @admin_required
    id_usuario = leer_identidad(request)
    usuario = obtener_usuario_por_id(id_usuario)
    if not usuario:
        raise ErrorApi(404, {"message": "Usuario no encontrado"})
    if usuario.role != 'admin':
        raise ErrorApi(403, {"message": "Acceso denegado. Se requieren permisos de administrador"})
    return id_usuario
