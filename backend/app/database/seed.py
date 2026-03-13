from datetime import date

def seed(app, db, User, Comment):  # ← recibe todo, no importa nada de main
    with app.app_context():

        users = [
            User(id=1, name="Carlos",  last_name="García",    email="carlos@gmail.com",  role="admin", date_of_registration=date(2024, 1, 15)),
            User(id=2, name="María",   last_name="López",     email="maria@gmail.com",   role="user",  date_of_registration=date(2024, 3, 22)),
            User(id=3, name="Pedro",   last_name="Martínez",  email="pedro@gmail.com",   role="user",  date_of_registration=date(2024, 6, 10)),
            User(id=4, name="Lucía",   last_name="Sánchez",   email="lucia@gmail.com",   role="mod",   date_of_registration=date(2025, 1, 5)),
            User(id=5, name="Andrés",  last_name="Fernández", email="andres@gmail.com",  role="user")
        ]

        comments = [
            Comment(id_comment=1, id_user=1, description="Este juego es increíble, muy adictivo.",        date_of_comment=date(2025, 2, 10)),
            Comment(id_comment=2, id_user=2, description="Me parece que el balanceo está roto.",          date_of_comment=date(2025, 2, 15)),
            Comment(id_comment=3, id_user=3, description="Buena experiencia, recomendado para todos.",    date_of_comment=date(2025, 3, 1)),
            Comment(id_comment=4, id_user=1, description="La actualización mejoró mucho el rendimiento.", date_of_comment=date(2025, 3, 20)),
            Comment(id_comment=5, id_user=4, description="Esperaba más del modo historia.",               date_of_comment=date(2025, 4, 5)),
            Comment(id_comment=6, id_user=5, description="Los gráficos son de otro nivel.",               date_of_comment=date(2025, 5, 12)),
            Comment(id_comment=7, id_user=2, description="El matchmaking necesita mejoras urgentes.")
        ]

        db.session.add_all(users)
        db.session.commit()
        db.session.add_all(comments)
        db.session.commit()

        print("✅ Seed completado con éxito")