from flask import Flask
from app.database.db import db
from app.database.seed import seed
from app.models.User import User
from app.models.Comment import Comment
from app.models.Video_game import Video_game
from app.models.Rate import Rate
from app.models.Favorite import Favorite
from app.routes.welcome_route import welcome_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/game_rank"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

# Registro de Blueprints
app.register_blueprint(welcome_bp, url_prefix="/user")


db.init_app(app)

# Comandos personalizados para la gestión de la base de datos
@app.cli.command("db-create")
def db_create():
    with app.app_context():
        db.create_all()
        print("Base de datos creada con éxito")

@app.cli.command("db-drop")
def db_drop():
    with app.app_context():
        db.drop_all()
        print("Base de datos eliminada con éxito")

@app.cli.command("db-seed")
def db_seed():
    with app.app_context():
        seed(app, db, User, Comment, Video_game, Rate, Favorite)
        print("Los datos de prueba han sido implementados")

@app.cli.command("db-reset")
def db_reset():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("🔄 Base de datos reiniciada con éxito")
    seed(app, db, User, Comment, Video_game, Rate, Favorite)


# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)