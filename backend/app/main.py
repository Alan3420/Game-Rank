from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/gamerank"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    print("Base de datos creada")
    

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)