import os
from dotenv import load_dotenv

# Cargamos el .env ANTES de importar nada mas que dependa de variables de
# entorno (DB_URI, JWT_SECRET_KEY, etc.). Si lo dejamos al final, los
# modulos que se importan despues ya no veran las variables.
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from datetime import timedelta
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.database.db import db
from app.database.seed import seed
from app.limiter import limiter

# Importamos todos los modelos aqui para que SQLAlchemy y Alembic los
# descubran al arrancar la app (si no, las migraciones podrian generar
# diffs vacios y db.create_all() no crearia las tablas).
from app.models.User import User
from app.models.Comment import Comment
from app.models.Video_game import Video_game
from app.models.Rate import Rate
from app.models.Favorite import Favorite
from app.models.UserGameStatus import UserGameStatus

# Blueprints (uno por dominio funcional).
from app.routes.welcome_route import welcome_bp
from app.routes.options_user_route import user_option_bp
from app.routes.content_overview_route import content_overview_bp
from app.routes.rates_route import rates_bp
from app.routes.comment_route import comment_bp
from app.routes.favorite_route import favorite_bp
from app.routes.user_game_status_route import status_bp
from app.routes.tendencias_route import tendencias_bp


app = Flask(__name__)
jwt = JWTManager(app)


# Callbacks JWT: si el token no llega, esta caducado o es invalido,
# devolvemos JSON con 401 en lugar del HTML por defecto de Flask.

@jwt.unauthorized_loader
def callback_token_ausente(_):
    return jsonify({"message": "Token no válido"}), 401

@jwt.expired_token_loader
def callback_token_expirado(*_):
    return jsonify({"message": "Token expirado"}), 401

@jwt.invalid_token_loader
def callback_token_invalido(_):
    return jsonify({"message": "Token inválido"}), 401


# Configuracion de SQLAlchemy. Las opciones de pool son importantes para
# producciones detras de un proxy (PlanetScale, Aiven, etc.) donde las
# conexiones inactivas pueden caer y dejarte un MySQL gone away.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

_ruta_certificado_ca = os.path.join(os.path.dirname(__file__), 'ca.pem')
_opciones_engine = {
    "pool_pre_ping": True,
    "pool_recycle": 280
}
if os.path.exists(_ruta_certificado_ca):
    # Si existe el certificado, lo usamos para forzar TLS al conectar.
    _opciones_engine["connect_args"] = {"ssl": {"ca": _ruta_certificado_ca}}

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = _opciones_engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = False

# Sesion JWT: 2 horas. Suficiente para no molestar al usuario y corto
# como para que un token filtrado no sirva indefinidamente.
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")


# Registro de Blueprints. Cada uno se monta bajo un prefijo distinto
# para que las URLs queden limpias y agrupadas por dominio.
app.register_blueprint(welcome_bp, url_prefix="/user")
app.register_blueprint(content_overview_bp, url_prefix="/content")
app.register_blueprint(user_option_bp, url_prefix="/settings")
app.register_blueprint(rates_bp, url_prefix="/rate")
app.register_blueprint(comment_bp, url_prefix="/comment")
app.register_blueprint(favorite_bp, url_prefix="/favorite")
app.register_blueprint(status_bp, url_prefix="/status")
app.register_blueprint(tendencias_bp, url_prefix="/tendencias")


db.init_app(app)
limiter.init_app(app)


@app.errorhandler(429)
def demasiadas_peticiones(_):
    # Respuesta uniforme cuando el limiter rechaza una peticion.
    return jsonify({"message": "Demasiadas peticiones. Por favor, espera un momento."}), 429


@app.after_request
def agregar_cabeceras_seguridad(response):
    # Cabeceras de seguridad basicas. Evitan algunos vectores comunes
    # como XSS de tipo MIME-sniffing, clickjacking via iframe, etc.
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


# CORS: la lista blanca de origenes permitidos incluye los puertos de
# desarrollo y el dominio de produccion (que viene del .env). Cualquier
# otro origen no podra hacer requests con cookies/auth desde el navegador.
origenes_permitidos = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

origen_produccion = os.getenv("FRONTEND_ORIGIN")
if origen_produccion:
    origenes_permitidos.append(origen_produccion)

CORS(app, origins=origenes_permitidos, allow_headers=["Content-Type", "Authorization"])


# Configuracion de migraciones con Alembic via Flask-Migrate.
migraciones = Migrate(app, db)


# Comandos personalizados para la gestion de la base de datos.
# Los mantenemos con su nombre original ("db-create", "db-seed") porque
# son los que se invocan desde flask CLI y forman parte del workflow del
# equipo y de los scripts de despliegue.

@app.cli.command("db-create")
def db_create():
    with app.app_context():
        db.create_all()
        print("Base de datos creada con éxito")


@app.cli.command("db-seed")
def db_seed():
    with app.app_context():
        seed(app, db, User, Comment, Video_game, Rate, Favorite, UserGameStatus)
        print("Los datos de prueba han sido implementados")


# Punto de entrada cuando se ejecuta directamente (python app/main.py).
# En produccion gunicorn se encarga, asi que este bloque solo aplica en
# desarrollo o ejecuciones locales.
if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run('0.0.0.0', 5000, debug=debug)
