import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from datetime import timedelta
from flask import Flask, jsonify
from flask_migrate import Migrate
from app.database.db import db
from app.database.seed import seed
from app.models.User import User
from app.models.Comment import Comment
from app.models.Video_game import Video_game
from app.models.Rate import Rate
from app.models.Favorite import Favorite
from app.models.UserGameStatus import UserGameStatus
from app.routes.welcome_route import welcome_bp
from app.routes.options_user_route import user_option_bp
from app.routes.content_overview_route import content_overview_bp
from app.routes.rates_route import rates_bp
from app.routes.comment_route import comment_bp
from app.routes.favorite_route import favorite_bp
from app.routes.user_game_status_route import status_bp
from app.routes.tendencias_route import tendencias_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.limiter import limiter


app = Flask(__name__)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(_):
    return jsonify({"message": "Token no válido"}), 401

@jwt.expired_token_loader
def expired_token_callback(*_):
    return jsonify({"message": "Token expirado"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(_):
    return jsonify({"message": "Token inválido"}), 401


# Configuración proyecto
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "connect_args": {
        "ssl": {
            "ca": os.path.join(os.path.dirname(__file__), 'ca.pem')
        }
    }
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")


# Registro de Blueprints
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
    return jsonify({"message": "Demasiadas peticiones. Por favor, espera un momento."}), 429

@app.after_request
def agregar_cabeceras_seguridad(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

# Configurar CORS restrictivamente
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

# Migraciones
migraciones = Migrate(app, db)

# Comandos personalizados para la gestión de la base de datos
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


# Punto de entrada de la aplicación
if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run('0.0.0.0', 5000, debug=debug)