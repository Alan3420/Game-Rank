from datetime import date


SEED_EMAILS = [
    "juan@gmail.com",   "maria@gmail.com",  "carlos@gmail.com", "ana@gmail.com",
    "luis@gmail.com",   "sofia@gmail.com",  "diego@gmail.com",  "laura@gmail.com",
    "pedro@gmail.com",  "elena@gmail.com",  "miguel@gmail.com", "carmen@gmail.com",
    "raul@gmail.com",   "alba@gmail.com",   "ivan@gmail.com",
]

SEED_GAME_IDS = [3328, 3498, 4062, 5679, 13536, 28, 41494, 58175, 326243, 27789]


def seed(app, db, User, Comment, Favorite, AddFavorite):
    with app.app_context():

        User.query.filter(User.email.in_(SEED_EMAILS)).delete(synchronize_session=False)
        db.session.commit()

        users = [
            User("Juan",   "Pérez",     "JuanP",     "juan@gmail.com",   "password123"),
            User("María",  "Gómez",     "MariaG",    "maria@gmail.com",  "password456"),
            User("Carlos", "López",     "CarlosL",   "carlos@gmail.com", "password789"),
            User("Ana",    "Martínez",  "AnaMart",   "ana@gmail.com",    "password321"),
            User("Luis",   "Sánchez",   "LuisS",     "luis@gmail.com",   "password654"),
            User("Sofía",  "García",    "SofiaG",    "sofia@gmail.com",  "password987"),
            User("Diego",  "Rodríguez", "DiegoR",    "diego@gmail.com",  "password147"),
            User("Laura",  "Fernández", "LauraF",    "laura@gmail.com",  "password258"),
            User("Pedro",  "Jiménez",   "PedroJ",    "pedro@gmail.com",  "password369"),
            User("Elena",  "Torres",    "ElenaT",    "elena@gmail.com",  "password741"),
            User("Miguel", "Ruiz",      "MiguelR",   "miguel@gmail.com", "password852"),
            User("Carmen", "Vargas",    "CarmenV",   "carmen@gmail.com", "password963"),
            User("Raúl",   "Moreno",    "RaulM",     "raul@gmail.com",   "password111"),
            User("Alba",   "Castro",    "AlbaC",     "alba@gmail.com",   "password222"),
            User("Iván",   "Molina",    "IvanMolina","ivan@gmail.com",   "password333"),
        ]
        db.session.add_all(users)
        db.session.flush()

        j  = users[0].id_user
        m  = users[1].id_user
        c  = users[2].id_user
        a  = users[3].id_user
        l  = users[4].id_user
        s  = users[5].id_user
        d  = users[6].id_user
        r  = users[7].id_user
        p  = users[8].id_user
        e  = users[9].id_user
        mi = users[10].id_user
        ca = users[11].id_user
        ra = users[12].id_user
        al = users[13].id_user
        iv = users[14].id_user

        datos_favorites = [
            (j, 3328,   date(2024, 11, 1),  "completado"),
            (m, 3328,   date(2024, 11, 2),  "completado"),
            (c, 3328,   date(2024, 11, 3),  "completado"),
            (a, 3328,   date(2024, 11, 4),  "completado"),
            (l, 3328,   date(2024, 11, 5),  "jugando"),
            (s, 3328,   date(2024, 11, 6),  "completado"),
            (d, 3328,   date(2024, 11, 7),  "completado"),
            (r, 3328,   date(2024, 11, 8),  "pendiente"),
            (j, 3498,   date(2024, 11, 10), "completado"),
            (m, 3498,   date(2024, 11, 11), "jugando"),
            (c, 3498,   date(2024, 11, 12), "completado"),
            (a, 3498,   date(2024, 11, 13), "completado"),
            (l, 3498,   date(2024, 11, 14), "pendiente"),
            (s, 3498,   date(2024, 11, 15), "completado"),
            (d, 3498,   date(2024, 11, 16), "jugando"),
            (j, 58175,  date(2024, 12, 1),  "completado"),
            (m, 58175,  date(2024, 12, 2),  "completado"),
            (c, 58175,  date(2024, 12, 3),  "completado"),
            (a, 58175,  date(2024, 12, 4),  "jugando"),
            (l, 58175,  date(2024, 12, 5),  "completado"),
            (s, 58175,  date(2024, 12, 6),  "pendiente"),
            (j, 326243, date(2025, 1, 1),   "jugando"),
            (m, 326243, date(2025, 1, 2),   "completado"),
            (c, 326243, date(2025, 1, 3),   "pendiente"),
            (a, 326243, date(2025, 1, 4),   "completado"),
            (l, 326243, date(2025, 1, 5),   None),
            (d, 326243, date(2025, 1, 6),   "jugando"),
            (r, 326243, date(2025, 1, 7),   "completado"),
            (m, 5679,   date(2024, 12, 10), "completado"),
            (c, 5679,   date(2024, 12, 11), "completado"),
            (d, 5679,   date(2024, 12, 12), "completado"),
            (r, 5679,   date(2024, 12, 13), "jugando"),
            (s, 5679,   date(2024, 12, 14), "pendiente"),
            (c, 41494,  date(2025, 2, 1),   "completado"),
            (d, 41494,  date(2025, 2, 2),   "jugando"),
            (r, 41494,  date(2025, 2, 3),   "completado"),
            (l, 41494,  date(2025, 2, 4),   "pendiente"),
            (a, 41494,  date(2025, 2, 5),   "completado"),
            (j, 28,     date(2025, 1, 15),  "completado"),
            (a, 28,     date(2025, 1, 16),  "completado"),
            (s, 28,     date(2025, 1, 17),  "jugando"),
            (r, 28,     date(2025, 1, 18),  "pendiente"),
            (j, 13536,  date(2025, 3, 1),   "completado"),
            (d, 13536,  date(2025, 3, 2),   "completado"),
            (m, 13536,  date(2025, 3, 3),   "completado"),
            (a, 4062,   date(2025, 3, 10),  "completado"),
            (r, 4062,   date(2025, 3, 11),  "completado"),
            (s, 27789,  date(2025, 4, 1),   "jugando"),
            (j, 27789,  date(2025, 4, 2),   "pendiente"),
        ]

        for user_id, game_id, fecha, estado in datos_favorites:
            fav = Favorite(id_game_api=game_id, status=estado)
            db.session.add(fav)
            db.session.flush()
            af = AddFavorite(fav_id=fav.fav_id, id_user=user_id, date_added=fecha)
            db.session.add(af)

        db.session.commit()

        comments = [
            Comment(id_user=j,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 10), description="Una obra maestra, la mejor experiencia RPG de mi vida."),
            Comment(id_user=m,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 11), description="El mejor juego de rol que he jugado jamás, historia increíble."),
            Comment(id_user=c,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 12), description="Cada DLC vale lo que pesa, Blood and Wine es espectacular."),
            Comment(id_user=a,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 13), description="El mundo abierto más vivo que existe en un videojuego."),
            Comment(id_user=l,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 14), description="Geralt es el personaje mejor escrito de la historia de los RPG."),
            Comment(id_user=s,  id_videogame=3328,   rating=4, date_of_comment=date(2024, 11, 15), description="100 horas y sigo sin cansarme. Obra de arte total."),
            Comment(id_user=d,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 16), description="La banda sonora te pone los pelos de punta en cada combate."),
            Comment(id_user=r,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 17), description="Imposible que no te enamore este juego, es perfecto."),
            Comment(id_user=p,  id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 18), description="Los diálogos están escritos con una calidad literaria impresionante."),
            Comment(id_user=e,  id_videogame=3328,   rating=4, date_of_comment=date(2024, 11, 19), description="Hearts of Stone merece un 10 independientemente del juego base."),
            Comment(id_user=mi, id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 20), description="La ambientación medieval eslava es única y diferente a todo lo demás."),
            Comment(id_user=ca, id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 21), description="Las decisiones tienen consecuencias reales, te hacen pensar de verdad."),
            Comment(id_user=ra, id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 22), description="Nunca pensé que un juego de brujos me haría llorar, aquí estoy."),
            Comment(id_user=al, id_videogame=3328,   rating=4, date_of_comment=date(2024, 11, 23), description="El combate mezclando signos y espada es deliciosamente estratégico."),
            Comment(id_user=iv, id_videogame=3328,   rating=5, date_of_comment=date(2024, 11, 24), description="Diez años después sigue siendo el referente de los mundos abiertos."),
            Comment(id_user=j,  id_videogame=3498,   rating=5, date_of_comment=date(2024, 11, 20), description="El mundo de GTA V sigue siendo increíble después de tantos años."),
            Comment(id_user=m,  id_videogame=3498,   rating=4, date_of_comment=date(2024, 11, 21), description="Online es adictivo, pero la historia también merece la pena."),
            Comment(id_user=c,  id_videogame=3498,   rating=4, date_of_comment=date(2024, 11, 22), description="Tres protagonistas que funcionan a la perfección juntos."),
            Comment(id_user=a,  id_videogame=3498,   rating=5, date_of_comment=date(2024, 11, 23), description="Rockstar en su máximo esplendor, una ciudad viva de verdad."),
            Comment(id_user=l,  id_videogame=3498,   rating=4, date_of_comment=date(2024, 11, 24), description="La misión final es de las mejores que he jugado."),
            Comment(id_user=s,  id_videogame=3498,   rating=4, date_of_comment=date(2024, 11, 25), description="Siguen sacando contenido después de 10 años, es increíble."),
            Comment(id_user=d,  id_videogame=3498,   rating=4, date_of_comment=date(2024, 11, 26), description="Trevor es el personaje más loco de la historia de los videojuegos."),
            Comment(id_user=j,  id_videogame=58175,  rating=5, date_of_comment=date(2024, 12, 1),  description="La historia de Kratos y Atreus te llega al alma."),
            Comment(id_user=m,  id_videogame=58175,  rating=5, date_of_comment=date(2024, 12, 2),  description="El combate es brutal y satisfactorio al máximo nivel."),
            Comment(id_user=c,  id_videogame=58175,  rating=5, date_of_comment=date(2024, 12, 3),  description="Santa Monica hizo un reboot perfecto, redefinió la saga."),
            Comment(id_user=a,  id_videogame=58175,  rating=5, date_of_comment=date(2024, 12, 4),  description="Los gráficos son una barbaridad, parece una película de Hollywood."),
            Comment(id_user=l,  id_videogame=58175,  rating=5, date_of_comment=date(2024, 12, 5),  description="El final me dejó sin palabras, la mejor aventura que he vivido."),
            Comment(id_user=s,  id_videogame=58175,  rating=4, date_of_comment=date(2024, 12, 6),  description="Cada enemigo es un desafío diferente, no te aburres nunca."),
            Comment(id_user=j,  id_videogame=326243, rating=5, date_of_comment=date(2025, 2, 1),   description="Elden Ring es puro masoquismo del bueno, no puedo parar."),
            Comment(id_user=m,  id_videogame=326243, rating=5, date_of_comment=date(2025, 2, 2),   description="El mundo abierto de FromSoftware es una revolución."),
            Comment(id_user=c,  id_videogame=326243, rating=5, date_of_comment=date(2025, 2, 3),   description="Los jefes finales son los más épicos que he visto en ningún juego."),
            Comment(id_user=a,  id_videogame=326243, rating=5, date_of_comment=date(2025, 2, 4),   description="Difícil pero increíblemente justo, cada muerte es un aprendizaje."),
            Comment(id_user=l,  id_videogame=326243, rating=4, date_of_comment=date(2025, 2, 5),   description="George R.R. Martin y Miyazaki juntos son una combinación brutal."),
            Comment(id_user=m,  id_videogame=5679,   rating=5, date_of_comment=date(2024, 12, 20), description="Skyrim es el juego al que siempre vuelvo, la nostalgia es real."),
            Comment(id_user=c,  id_videogame=5679,   rating=4, date_of_comment=date(2024, 12, 21), description="Las mazmorras son infinitas, nunca te quedas sin contenido."),
            Comment(id_user=d,  id_videogame=5679,   rating=5, date_of_comment=date(2024, 12, 22), description="Los mods lo hacen prácticamente un juego nuevo cada vez."),
            Comment(id_user=r,  id_videogame=5679,   rating=5, date_of_comment=date(2024, 12, 23), description="El sistema de progresión de habilidades es increíblemente adictivo."),
            Comment(id_user=s,  id_videogame=5679,   rating=4, date_of_comment=date(2024, 12, 24), description="Bethesda sabe crear mundos que te enganchan durante cientos de horas."),
            Comment(id_user=j,  id_videogame=13536,  rating=5, date_of_comment=date(2025, 1, 5),   description="Half-Life 2 inventó el shooter moderno, es una referencia absoluta."),
            Comment(id_user=m,  id_videogame=13536,  rating=5, date_of_comment=date(2025, 1, 6),   description="La física del Gravity Gun cambió los FPS para siempre."),
            Comment(id_user=c,  id_videogame=13536,  rating=5, date_of_comment=date(2025, 1, 7),   description="Sigue siendo uno de los mejores juegos de la historia."),
            Comment(id_user=j,  id_videogame=28,     rating=5, date_of_comment=date(2025, 1, 20),  description="Red Dead Redemption tiene la mejor historia del oeste en videojuegos."),
            Comment(id_user=a,  id_videogame=28,     rating=4, date_of_comment=date(2025, 1, 21),  description="John Marston es un personaje con una profundidad tremenda."),
            Comment(id_user=s,  id_videogame=28,     rating=5, date_of_comment=date(2025, 1, 22),  description="El final te parte el corazón, qué escritura tan brutal."),
            Comment(id_user=r,  id_videogame=28,     rating=4, date_of_comment=date(2025, 1, 23),  description="El ambiente del lejano oeste está recreado a la perfección."),
            Comment(id_user=c,  id_videogame=41494,  rating=4, date_of_comment=date(2025, 2, 10),  description="Tras los parches, Cyberpunk 2077 es otro juego completamente."),
            Comment(id_user=d,  id_videogame=41494,  rating=4, date_of_comment=date(2025, 2, 11),  description="Night City es la ciudad más impresionante de cualquier videojuego."),
            Comment(id_user=r,  id_videogame=41494,  rating=5, date_of_comment=date(2025, 2, 12),  description="La historia de V es emotiva y te engancha de principio a fin."),
            Comment(id_user=l,  id_videogame=41494,  rating=3, date_of_comment=date(2025, 2, 13),  description="El DLC Phantom Liberty es mejor que el juego base, es una pasada."),
            Comment(id_user=j,  id_videogame=4062,   rating=5, date_of_comment=date(2025, 3, 1),   description="Portal 2 es el mejor puzzle game jamás creado, punto."),
            Comment(id_user=m,  id_videogame=4062,   rating=5, date_of_comment=date(2025, 3, 2),   description="El humor de GLaDOS y Wheatley no tiene rival en ningún juego."),
            Comment(id_user=s,  id_videogame=27789,  rating=5, date_of_comment=date(2025, 4, 5),   description="Hollow Knight es la mejor metroidvania que existe, es una joya."),
        ]
        db.session.add_all(comments)
        db.session.commit()

        print(f"Seed completado: {len(users)} usuarios, "
              f"{len(datos_favorites)} favoritos, {len(comments)} comentarios.")
