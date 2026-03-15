from datetime import date

def seed(app, db, User, Comment, Video_game, Rate, Favorite):
    with app.app_context():

        users = [
            User(id_user=1, name="Carlos",    last_name="García",   email="carlos@gmail.com",    role="admin",     date_of_registration=date(2024, 1, 15)),
            User(id_user=2, name="Laura",     last_name="Martínez", email="laura@gmail.com",     role="user",      date_of_registration=date(2024, 3, 22)),
            User(id_user=3, name="Pedro",     last_name="López",    email="pedro@gmail.com",     role="user",      date_of_registration=date(2024, 6, 10)),
            User(id_user=4, name="Sofía",     last_name="Ramírez",  email="sofia@gmail.com",     role="moderator", date_of_registration=date(2024, 9, 5)),
            User(id_user=5, name="Miguel",    last_name="Torres",   email="miguel@gmail.com",    role="user",      date_of_registration=date(2024, 11, 18)),
            User(id_user=6, name="Valentina", last_name="Herrera",  email="valentina@gmail.com", role="user",      date_of_registration=date(2025, 1, 7)),
            User(id_user=7, name="Andrés",    last_name="Castillo", email="andres@gmail.com",    role="moderator", date_of_registration=date(2025, 2, 14)),
        ]

        comments = [
            Comment(id_comment=1, id_user=1, description="Una obra maestra absoluta, la mejor experiencia RPG que he tenido.",          date_of_comment=date(2025, 1, 10)),
            Comment(id_comment=2, id_user=2, description="Historia emotiva y combates brutales, Santa Monica lo logró de nuevo.",       date_of_comment=date(2025, 1, 20)),
            Comment(id_comment=3, id_user=3, description="Elden Ring redefinió lo que es un mundo abierto, simplemente brutal.",        date_of_comment=date(2025, 2, 5)),
            Comment(id_comment=4, id_user=4, description="Red Dead 2 es puro arte interactivo, cada detalle está cuidado al máximo.",   date_of_comment=date(2025, 2, 18)),
            Comment(id_comment=5, id_user=5, description="Cyberpunk 2077 tras sus parches es otro juego, completamente redimido.",      date_of_comment=date(2025, 3, 3)),
            Comment(id_comment=6, id_user=6, description="Hollow Knight es una joya indie, difícil pero increíblemente satisfactorio.", date_of_comment=date(2025, 3, 25)),
            Comment(id_comment=7, id_user=7, description="Disco Elysium es la escritura más brillante que he visto en un videojuego.",  date_of_comment=date(2025, 4, 10)),
        ]

        video_games = [
            Video_game(id_game=1, name="The Witcher 3: Wild Hunt",  date_release=date(2015, 5, 19),  platforms="PC, PS4, PS5, Xbox One, Switch",      development_company="CD Projekt Red",     id_comment=1),
            Video_game(id_game=2, name="God of War",                date_release=date(2018, 4, 20),  platforms="PS4, PS5, PC",                        development_company="Santa Monica Studio", id_comment=2),
            Video_game(id_game=3, name="Elden Ring",                date_release=date(2022, 2, 25),  platforms="PC, PS4, PS5, Xbox One, Xbox Series", development_company="FromSoftware",       id_comment=3),
            Video_game(id_game=4, name="Red Dead Redemption 2",     date_release=date(2018, 10, 26), platforms="PS4, Xbox One, PC",                   development_company="Rockstar Games",     id_comment=4),
            Video_game(id_game=5, name="Cyberpunk 2077",            date_release=date(2020, 12, 10), platforms="PC, PS4, PS5, Xbox One, Xbox Series", development_company="CD Projekt Red",     id_comment=5),
            Video_game(id_game=6, name="Hollow Knight",             date_release=date(2017, 2, 24),  platforms="PC, PS4, Xbox One, Switch",           development_company="Team Cherry",        id_comment=6),
            Video_game(id_game=7, name="Disco Elysium",             date_release=date(2019, 10, 15), platforms="PC, PS4, PS5, Xbox One",              development_company="ZA/UM",              id_comment=7),
        ]

        favorites = [
            Favorite(user_id=1, id_game=1, date_added=date(2025, 1, 12)),
            Favorite(user_id=1, id_game=3, date_added=date(2025, 2, 9)),
            Favorite(user_id=2, id_game=2, date_added=date(2025, 1, 23)),
            Favorite(user_id=2, id_game=4, date_added=date(2025, 2, 21)),
            Favorite(user_id=3, id_game=3),
            Favorite(user_id=3, id_game=6, date_added=date(2025, 3, 28)),
            Favorite(user_id=4, id_game=4),
        ]

        rates = [
            Rate(id_user=1, id_game=1, date_rate=date(2025, 1, 11), rating=10, status="completado"),
            Rate(id_user=1, id_game=3, date_rate=date(2025, 2, 8),  rating=9,  status="completado"),
            Rate(id_user=2, id_game=2, date_rate=date(2025, 1, 22), rating=9,  status="completado"),
            Rate(id_user=2, id_game=4, date_rate=date(2025, 2, 20), rating=10, status="completado"),
            Rate(id_user=3, id_game=3, date_rate=date(2025, 2, 6),  rating=10, status="completado"),
            Rate(id_user=3, id_game=6, date_rate=date(2025, 3, 27), rating=8,  status="jugando"),
            Rate(id_user=4, id_game=4, date_rate=date(2025, 2, 19), rating=10, status="completado"),
            Rate(id_user=4, id_game=7, date_rate=date(2025, 4, 12), rating=8,  status="jugando"),
            Rate(id_user=5, id_game=5, date_rate=date(2025, 3, 5),  rating=8,  status="completado"),
            Rate(id_user=5, id_game=1, date_rate=date(2025, 1, 25), rating=9,  status="completado"),
            Rate(id_user=6, id_game=6, date_rate=date(2025, 3, 26), rating=10, status="completado"),
            Rate(id_user=6, id_game=2, date_rate=date(2025, 2, 1),  rating=9,  status="completado"),
            Rate(id_user=7, id_game=7, date_rate=date(2025, 4, 11), rating=10, status="completado"),
            Rate(id_user=7, id_game=5, date_rate=date(2025, 3, 10), rating=7,  status="abandonado"),
        ]

        db.session.add_all(users)
        db.session.commit()
        db.session.add_all(comments)
        db.session.commit()
        db.session.add_all(video_games)
        db.session.commit()
        db.session.add_all(favorites)
        db.session.commit()
        db.session.add_all(rates)
        db.session.commit()

        print("✅ Seed completada")