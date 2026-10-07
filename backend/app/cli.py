# Tareas de base de datos sin Flask (antes: flask db-create / flask db-seed)
#   python -m app.cli crear-tablas
#   python -m app.cli seed
# Las migraciones van con Alembic: alembic -c migrations/alembic.ini upgrade head
import sys

from app.database.db import db
from app.database.seed import seed
from app.models.User import User
from app.models.Comment import Comment
from app.models.Favorite import Favorite
from app.models.AddFavorite import AddFavorite


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""

    if orden == "crear-tablas":
        db.create_all()
        print("Base de datos creada con éxito")
    elif orden == "seed":
        seed(db, User, Comment, Favorite, AddFavorite)
        print("Los datos de prueba han sido implementados")
    else:
        print("Uso: python -m app.cli crear-tablas | seed")
        sys.exit(1)

    db.session.remove()


if __name__ == "__main__":
    main()
