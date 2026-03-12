from flask import Flask
from app.database.db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/pruebaconnection"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from app.models.md_prueba import Prueba

with app.app_context():
    db.create_all()          # 1️⃣ Primero crea las tablas
    
    prueba = Prueba(name="Alan Novas")
    prueba2 = Prueba(name="Felipe Novas")
    prueba3 = Prueba(name="Sofia Novas")
    
    db.session.add(prueba)   # 2️⃣ Luego inserta datos
    db.session.add(prueba2)
    db.session.add(prueba3)
    db.session.commit()
    print("Datos insertados ✅")

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)