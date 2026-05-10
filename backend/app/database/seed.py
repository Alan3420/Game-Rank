from datetime import date

def seed(app, db, User, Comment, Video_game, Rate, Favorite):
    with app.app_context():

        users = [
            User("Juan", "Pérez", "juan@gmail.com", "password123"),
            User("María", "Gómez", "maria@gmail.com", "password456"),
            User("Carlos", "López", "carlos@gmail.com", "password789"),
            User("Ana", "Martínez", "ana@gmail.com", "password321"),
            User("Luis", "Sánchez", "luis@gmail.com", "password654"),
            User("Sofía", "García", "sofia@gmail.com", "password987"),
            User("Diego", "Rodríguez", "diego@gmail.com", "password147"),
            User("Laura", "Fernández", "laura@gmail.com", "password258"),
        ]

        comments = [
            Comment(id_user=1, id_videogame=1, description="Una obra maestra absoluta, la mejor experiencia RPG que he tenido.", date_of_comment=date(2024, 11, 10)),
            Comment(id_user=2, id_videogame=2, description="Historia emotiva y combates brutales, Santa Monica lo logró de nuevo.", date_of_comment=date(2024, 11, 20)),
            Comment(id_user=3, id_videogame=3, description="Elden Ring redefinió lo que es un mundo abierto, simplemente brutal.", date_of_comment=date(2024, 12, 5)),
            Comment(id_user=4, id_videogame=4, description="Red Dead 2 es puro arte interactivo, cada detalle está cuidado.", date_of_comment=date(2024, 12, 18)),
            Comment(id_user=5, id_videogame=5, description="Cyberpunk 2077 tras sus parches es completamente redimido.", date_of_comment=date(2025, 1, 3)),
            Comment(id_user=6, id_videogame=6, description="Hollow Knight es una joya indie, difícil pero increíblemente satisfactorio.", date_of_comment=date(2025, 1, 25)),
            Comment(id_user=7, id_videogame=7, description="Disco Elysium tiene la escritura más brillante de cualquier videojuego.", date_of_comment=date(2025, 2, 10)),
            Comment(id_user=1, id_videogame=2, description="Excelente continuación, supera las expectativas completamente.", date_of_comment=date(2025, 2, 15)),
            Comment(id_user=3, id_videogame=5, description="La comunidad tiene razón, ahora es un juego increíble.", date_of_comment=date(2025, 2, 20)),
        ]

        video_games = [
            Video_game(id_game_api=1, name="The Witcher 3: Wild Hunt", date_release=date(2015, 5, 19), platforms="PC, PS4, PS5, Xbox One, Switch", development_company="CD Projekt Red"),
            Video_game(id_game_api=2, name="God of War", date_release=date(2018, 4, 20), platforms="PS4, PS5, PC", development_company="Santa Monica Studio"),
            Video_game(id_game_api=3, name="Elden Ring", date_release=date(2022, 2, 25), platforms="PC, PS4, PS5, Xbox One, Xbox Series", development_company="FromSoftware"),
            Video_game(id_game_api=4, name="Red Dead Redemption 2", date_release=date(2018, 10, 26), platforms="PS4, Xbox One, PC", development_company="Rockstar Games"),
            Video_game(id_game_api=5, name="Cyberpunk 2077", date_release=date(2020, 12, 10), platforms="PC, PS4, PS5, Xbox One, Xbox Series", development_company="CD Projekt Red"),
            Video_game(id_game_api=6, name="Hollow Knight", date_release=date(2017, 2, 24), platforms="PC, PS4, Xbox One, Switch", development_company="Team Cherry"),
            Video_game(id_game_api=7, name="Disco Elysium", date_release=date(2019, 10, 15), platforms="PC, PS4, PS5, Xbox One", development_company="ZA/UM"),
        ]

        favorites = [
            Favorite(user_id=1, id_game_api=1, date_added=date(2024, 11, 12)),
            Favorite(user_id=1, id_game_api=3, date_added=date(2024, 12, 9)),
            Favorite(user_id=2, id_game_api=2, date_added=date(2024, 11, 23)),
            Favorite(user_id=2, id_game_api=4, date_added=date(2024, 12, 21)),
            Favorite(user_id=3, id_game_api=3, date_added=date(2024, 12, 15)),
            Favorite(user_id=3, id_game_api=6, date_added=date(2025, 1, 28)),
            Favorite(user_id=4, id_game_api=4, date_added=date(2024, 12, 19)),
            Favorite(user_id=5, id_game_api=5, date_added=date(2025, 1, 10)),
            Favorite(user_id=6, id_game_api=6, date_added=date(2025, 1, 26)),
            Favorite(user_id=7, id_game_api=7, date_added=date(2025, 2, 11)),
        ]

        rates = [
            Rate(id_user=1, id_game_api=1, date_rate=date(2024, 11, 11), rating=5, status="completado"),
            Rate(id_user=1, id_game_api=3, date_rate=date(2024, 12, 8), rating=4, status="completado"),
            Rate(id_user=2, id_game_api=2, date_rate=date(2024, 11, 22), rating=5, status="completado"),
            Rate(id_user=2, id_game_api=4, date_rate=date(2024, 12, 20), rating=5, status="completado"),
            Rate(id_user=3, id_game_api=3, date_rate=date(2024, 12, 6), rating=5, status="completado"),
            Rate(id_user=3, id_game_api=6, date_rate=date(2025, 1, 27), rating=4, status="jugando"),
            Rate(id_user=4, id_game_api=4, date_rate=date(2024, 12, 19), rating=5, status="completado"),
            Rate(id_user=4, id_game_api=7, date_rate=date(2025, 2, 12), rating=4, status="jugando"),
            Rate(id_user=5, id_game_api=5, date_rate=date(2025, 1, 5), rating=3, status="completado"),
            Rate(id_user=5, id_game_api=1, date_rate=date(2024, 11, 25), rating=4, status="completado"),
            Rate(id_user=6, id_game_api=6, date_rate=date(2025, 1, 26), rating=5, status="completado"),
            Rate(id_user=6, id_game_api=2, date_rate=date(2024, 12, 1), rating=4, status="completado"),
            Rate(id_user=7, id_game_api=7, date_rate=date(2025, 2, 11), rating=5, status="completado"),
            Rate(id_user=7, id_game_api=5, date_rate=date(2025, 1, 10), rating=2, status="abandonado"),
            Rate(id_user=8, id_game_api=1, date_rate=date(2024, 12, 10), rating=5, status="completado"),
            Rate(id_user=8, id_game_api=3, date_rate=date(2025, 1, 15), rating=4, status="jugando"),
        ]

        db.session.add_all(users)
        db.session.commit()

        db.session.add_all(video_games)
        db.session.commit()

        db.session.add_all(comments)
        db.session.commit()

        db.session.add_all(favorites)
        db.session.commit()
        
        db.session.add_all(rates)
        db.session.commit()

        print("Seed importado correctamente")