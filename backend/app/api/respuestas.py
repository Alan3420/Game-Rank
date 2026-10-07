import json
from datetime import date, datetime
from decimal import Decimal

from fastapi import Request
from fastapi.responses import JSONResponse
from werkzeug.http import http_date


def _por_defecto(valor):
    # Igual que jsonify de Flask: fechas en RFC 1123 ("Sun, 17 May 2026
    # 00:00:00 GMT") y Decimal como texto. El frontend no cambia.
    if isinstance(valor, (datetime, date)):
        return http_date(valor)
    if isinstance(valor, Decimal):
        return str(valor)
    raise TypeError(f"No se puede serializar {type(valor).__name__}")


class RespuestaJson(JSONResponse):
    def render(self, contenido) -> bytes:
        return json.dumps(contenido, default=_por_defecto, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def responder(cuerpo, estado=200):
    return RespuestaJson(cuerpo, status_code=estado)


class ErrorApi(Exception):
    # Error con cuerpo propio ({"message": ...}) en vez del {"detail": ...}
    # de FastAPI, para mantener el formato que espera el frontend
    def __init__(self, estado, cuerpo):
        self.estado = estado
        self.cuerpo = cuerpo


def entero_de_query(request: Request, nombre, defecto):
    # Como request.args.get(..., type=int) de Flask: si no es un numero se
    # usa el valor por defecto en vez de devolver un error
    valor = request.query_params.get(nombre)
    if valor is None:
        return defecto
    try:
        return int(valor)
    except ValueError:
        return defecto


def texto_de_query(request: Request, nombre):
    return request.query_params.get(nombre)


async def leer_json(request: Request):
    # Como request.get_json() de Flask: el cuerpo como dict (o None si no
    # hay o no es JSON). Las rutas comprueban los campos que necesitan.
    try:
        datos = await request.json()
    except Exception:
        return None
    return datos
