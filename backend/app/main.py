import os
import uuid
from dotenv import load_dotenv

# el .env antes que nada: los modulos siguientes leen DB_URI, SECRET_KEY...
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.database.db import ambito_peticion, session
from app.api.limites import limiter
from app.api.respuestas import ErrorApi, RespuestaJson, responder
from app.api.routers import acceso, comentarios, contenido, cuenta, favoritos, tendencias

# registran sus tablas en Base.metadata
import app.models.User  # noqa: F401
import app.models.Comment  # noqa: F401
import app.models.Favorite  # noqa: F401
import app.models.AddFavorite  # noqa: F401

# /docs y /redoc se pueden apagar en produccion con MOSTRAR_DOCS=false
_docs = os.getenv("MOSTRAR_DOCS", "true").lower() != "false"

app = FastAPI(
    title="Game Rank API",
    description="Catálogo de RAWG con la capa personal y de comunidad de Game Rank: favoritos, estados, reseñas y tendencias.",
    version="2.0.0",
    default_response_class=RespuestaJson,
    docs_url="/docs" if _docs else None,
    redoc_url="/redoc" if _docs else None,
    openapi_url="/openapi.json" if _docs else None,
)

app.state.limiter = limiter


@app.exception_handler(ErrorApi)
async def manejar_error_api(_: Request, error: ErrorApi):
    return responder(error.cuerpo, error.estado)


@app.exception_handler(RateLimitExceeded)
async def demasiadas_peticiones(_: Request, __: RateLimitExceeded):
    return responder({"message": "Demasiadas peticiones. Por favor, espera un momento."}, 429)


@app.exception_handler(RequestValidationError)
async def cuerpo_no_valido(_: Request, __: RequestValidationError):
    # cuerpo ausente o que no es JSON: mismo formato {"message": ...}
    return responder({"message": "Datos de la petición no válidos"}, 400)


@app.middleware("http")
async def sesion_y_cabeceras(request: Request, call_next):
    # Una sesion de base de datos por peticion, cerrada al terminar
    marca = ambito_peticion.set(uuid.uuid4().hex)
    try:
        respuesta = await call_next(request)
    finally:
        session.remove()
        ambito_peticion.reset(marca)

    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "DENY"
    respuesta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    respuesta.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return respuesta


origenes_permitidos = ["https://gamerk.netlify.app"]
origen_produccion = os.getenv("FRONTEND_ORIGIN")
if origen_produccion:
    origenes_permitidos.append(origen_produccion)

# el CORS va el ultimo para envolver a todo lo demas (tambien los errores)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)

for modulo in (acceso, contenido, cuenta, comentarios, favoritos, tendencias):
    app.include_router(modulo.router)


if __name__ == "__main__":
    # python -m app.main sigue funcionando (desarrollo). En produccion se usa
    # el comando del Dockerfile: uvicorn con varios workers
    import uvicorn
    recarga = os.getenv("RECARGA", "false").lower() == "true"
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "5000")), reload=recarga)
