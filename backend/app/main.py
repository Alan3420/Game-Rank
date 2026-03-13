from flask import Flask
from app.database.db import db
from app.database.seed import seed
from app.models.User import User
from app.models.Comment import Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/game_rank"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.cli.command("db-create")
def db_create():
    with app.app_context():
        db.create_all()
        print("Base de datos creada con éxito")

@app.cli.command("db-reset")
def db_reset():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("🔄 Base de datos reiniciada con éxito")
    seed(app, db, User, Comment)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)