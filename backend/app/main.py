import os
from dotenv import load_dotenv

# cargamos el .env antes que nada, si no los modulos que vienen despues
# no veran las variables (DB_URI, SECRET_KEY...)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from datetime import timedelta
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.database.db import db
from app.database.seed import seed
from app.limiter import limiter

# importamos los modelos aqui para que Alembic los detecte al migrar
from app.models.User import User
from app.models.Comment import Comment
from app.models.Favorite import Favorite
from app.models.AddFavorite import AddFavorite

from app.routes.welcome_route import welcome_bp
from app.routes.options_user_route import user_option_bp
from app.routes.content_overview_route import content_overview_bp
from app.routes.comment_route import comment_bp
from app.routes.favorite_route import favorite_bp
from app.routes.tendencias_route import tendencias_bp


app = Flask(__name__)
jwt = JWTManager(app)


@jwt.unauthorized_loader
def callback_token_ausente(_):
    return jsonify({"message": "Token no válido"}), 401

@jwt.expired_token_loader
def callback_token_expirado(*_):
    return jsonify({"message": "Token expirado"}), 401

@jwt.invalid_token_loader
def callback_token_invalido(_):
    return jsonify({"message": "Token inválido"}), 401


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

_ruta_certificado_ca = os.path.join(os.path.dirname(__file__), 'ca.pem')
# pool_pre_ping y pool_recycle hacen falta porque en produccion las conexiones
# se quedan colgadas y MySQL las tira (sale el famoso "gone away")
_opciones_engine = {
    "pool_pre_ping": True,
    "pool_recycle": 280
}
if os.path.exists(_ruta_certificado_ca):
    _opciones_engine["connect_args"] = {"ssl": {"ca": _ruta_certificado_ca}}

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = _opciones_engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = False

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")


app.register_blueprint(welcome_bp, url_prefix="/user")
app.register_blueprint(content_overview_bp, url_prefix="/content")
app.register_blueprint(user_option_bp, url_prefix="/settings")
app.register_blueprint(comment_bp, url_prefix="/comment")
app.register_blueprint(favorite_bp, url_prefix="/favorite")
app.register_blueprint(tendencias_bp, url_prefix="/tendencias")


db.init_app(app)
limiter.init_app(app)


@app.errorhandler(429)
def demasiadas_peticiones(_):
    return jsonify({"message": "Demasiadas peticiones. Por favor, espera un momento."}), 429


@app.after_request
def agregar_cabeceras_seguridad(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


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


migraciones = Migrate(app, db)


@app.cli.command("db-create")
def db_create():
    with app.app_context():
        db.create_all()
        print("Base de datos creada con éxito")


@app.cli.command("db-seed")
def db_seed():
    with app.app_context():
        seed(app, db, User, Comment, Favorite, AddFavorite)
        print("Los datos de prueba han sido implementados")


if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run('0.0.0.0', 5000, debug=debug)
