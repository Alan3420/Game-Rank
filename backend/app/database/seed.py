from datetime import date


SEED_EMAILS = [
    "juan@gmail.com",   "maria@gmail.com",  "carlos@gmail.com", "ana@gmail.com",
    "luis@gmail.com",   "sofia@gmail.com",  "diego@gmail.com",  "laura@gmail.com",
    "pedro@gmail.com",  "elena@gmail.com",  "miguel@gmail.com", "carmen@gmail.com",
    "raul@gmail.com",   "alba@gmail.com",   "ivan@gmail.com",
]

SEED_GAME_IDS = [3328, 3498, 4062, 5679, 13536, 28, 41494, 58175, 326243, 27789]


def seed(app, db, User, Comment, Rate, Favorite, UserGameStatus):
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

        favorites = [
            Favorite(user_id=j, id_game_api=3328,   date_added=date(2024, 11, 1)),
            Favorite(user_id=m, id_game_api=3328,   date_added=date(2024, 11, 2)),
            Favorite(user_id=c, id_game_api=3328,   date_added=date(2024, 11, 3)),
            Favorite(user_id=a, id_game_api=3328,   date_added=date(2024, 11, 4)),
            Favorite(user_id=l, id_game_api=3328,   date_added=date(2024, 11, 5)),
            Favorite(user_id=s, id_game_api=3328,   date_added=date(2024, 11, 6)),
            Favorite(user_id=d, id_game_api=3328,   date_added=date(2024, 11, 7)),
            Favorite(user_id=r, id_game_api=3328,   date_added=date(2024, 11, 8)),
            Favorite(user_id=j, id_game_api=3498,   date_added=date(2024, 11, 10)),
            Favorite(user_id=m, id_game_api=3498,   date_added=date(2024, 11, 11)),
            Favorite(user_id=c, id_game_api=3498,   date_added=date(2024, 11, 12)),
            Favorite(user_id=a, id_game_api=3498,   date_added=date(2024, 11, 13)),
            Favorite(user_id=l, id_game_api=3498,   date_added=date(2024, 11, 14)),
            Favorite(user_id=s, id_game_api=3498,   date_added=date(2024, 11, 15)),
            Favorite(user_id=d, id_game_api=3498,   date_added=date(2024, 11, 16)),
            Favorite(user_id=j, id_game_api=58175,  date_added=date(2024, 12, 1)),
            Favorite(user_id=m, id_game_api=58175,  date_added=date(2024, 12, 2)),
            Favorite(user_id=c, id_game_api=58175,  date_added=date(2024, 12, 3)),
            Favorite(user_id=a, id_game_api=58175,  date_added=date(2024, 12, 4)),
            Favorite(user_id=l, id_game_api=58175,  date_added=date(2024, 12, 5)),
            Favorite(user_id=s, id_game_api=58175,  date_added=date(2024, 12, 6)),
            Favorite(user_id=j, id_game_api=326243, date_added=date(2025, 1, 1)),
            Favorite(user_id=m, id_game_api=326243, date_added=date(2025, 1, 2)),
            Favorite(user_id=c, id_game_api=326243, date_added=date(2025, 1, 3)),
            Favorite(user_id=a, id_game_api=326243, date_added=date(2025, 1, 4)),
            Favorite(user_id=l, id_game_api=326243, date_added=date(2025, 1, 5)),
            Favorite(user_id=m, id_game_api=5679,   date_added=date(2024, 12, 10)),
            Favorite(user_id=c, id_game_api=5679,   date_added=date(2024, 12, 11)),
            Favorite(user_id=d, id_game_api=5679,   date_added=date(2024, 12, 12)),
            Favorite(user_id=r, id_game_api=5679,   date_added=date(2024, 12, 13)),
            Favorite(user_id=s, id_game_api=5679,   date_added=date(2024, 12, 14)),
            Favorite(user_id=c, id_game_api=41494,  date_added=date(2025, 2, 1)),
            Favorite(user_id=d, id_game_api=41494,  date_added=date(2025, 2, 2)),
            Favorite(user_id=r, id_game_api=41494,  date_added=date(2025, 2, 3)),
            Favorite(user_id=l, id_game_api=41494,  date_added=date(2025, 2, 4)),
            Favorite(user_id=j, id_game_api=28,     date_added=date(2025, 1, 15)),
            Favorite(user_id=a, id_game_api=28,     date_added=date(2025, 1, 16)),
            Favorite(user_id=s, id_game_api=28,     date_added=date(2025, 1, 17)),
            Favorite(user_id=r, id_game_api=28,     date_added=date(2025, 1, 18)),
            Favorite(user_id=j, id_game_api=13536,  date_added=date(2025, 3, 1)),
            Favorite(user_id=d, id_game_api=13536,  date_added=date(2025, 3, 2)),
            Favorite(user_id=m, id_game_api=13536,  date_added=date(2025, 3, 3)),
            Favorite(user_id=a, id_game_api=4062,   date_added=date(2025, 3, 10)),
            Favorite(user_id=r, id_game_api=4062,   date_added=date(2025, 3, 11)),
            Favorite(user_id=s, id_game_api=27789,  date_added=date(2025, 4, 1)),
        ]
        db.session.add_all(favorites)
        db.session.commit()

        pares = [
            (j,  3328, 5, date(2024, 11, 10), "Una obra maestra, la mejor experiencia RPG de mi vida."),
            (m,  3328, 5, date(2024, 11, 11), "El mejor juego de rol que he jugado jamás, historia increíble."),
            (c,  3328, 5, date(2024, 11, 12), "Cada DLC vale lo que pesa, Blood and Wine es espectacular."),
            (a,  3328, 5, date(2024, 11, 13), "El mundo abierto más vivo que existe en un videojuego."),
            (l,  3328, 5, date(2024, 11, 14), "Geralt es el personaje mejor escrito de la historia de los RPG."),
            (s,  3328, 4, date(2024, 11, 15), "100 horas y sigo sin cansarme. Obra de arte total."),
            (d,  3328, 5, date(2024, 11, 16), "La banda sonora te pone los pelos de punta en cada combate."),
            (r,  3328, 5, date(2024, 11, 17), "Imposible que no te enamore este juego, es perfecto."),
            (p,  3328, 5, date(2024, 11, 18), "Los diálogos están escritos con una calidad literaria impresionante."),
            (e,  3328, 4, date(2024, 11, 19), "Hearts of Stone merece un 10 independientemente del juego base."),
            (mi, 3328, 5, date(2024, 11, 20), "La ambientación medieval eslava es única y diferente a todo lo demás."),
            (ca, 3328, 5, date(2024, 11, 21), "Las decisiones tienen consecuencias reales, te hacen pensar de verdad."),
            (ra, 3328, 5, date(2024, 11, 22), "Nunca pensé que un juego de brujos me haría llorar, aquí estoy."),
            (al, 3328, 4, date(2024, 11, 23), "El combate mezclando signos y espada es deliciosamente estratégico."),
            (iv, 3328, 5, date(2024, 11, 24), "Diez años después sigue siendo el referente de los mundos abiertos."),
            (j,  3498, 5, date(2024, 11, 20), "El mundo de GTA V sigue siendo increíble después de tantos años."),
            (m,  3498, 4, date(2024, 11, 21), "Online es adictivo, pero la historia también merece la pena."),
            (c,  3498, 4, date(2024, 11, 22), "Tres protagonistas que funcionan a la perfección juntos."),
            (a,  3498, 5, date(2024, 11, 23), "Rockstar en su máximo esplendor, una ciudad viva de verdad."),
            (l,  3498, 4, date(2024, 11, 24), "La misión final es de las mejores que he jugado."),
            (s,  3498, 4, date(2024, 11, 25), "Siguen sacando contenido después de 10 años, es increíble."),
            (d,  3498, 4, date(2024, 11, 26), "Trevor es el personaje más loco de la historia de los videojuegos."),
            (j,  58175, 5, date(2024, 12, 1), "La historia de Kratos y Atreus te llega al alma."),
            (m,  58175, 5, date(2024, 12, 2), "El combate es brutal y satisfactorio al máximo nivel."),
            (c,  58175, 5, date(2024, 12, 3), "Santa Monica hizo un reboot perfecto, redefinió la saga."),
            (a,  58175, 5, date(2024, 12, 4), "Los gráficos son una barbaridad, parece una película de Hollywood."),
            (l,  58175, 5, date(2024, 12, 5), "El final me dejó sin palabras, la mejor aventura que he vivido."),
            (s,  58175, 4, date(2024, 12, 6), "Cada enemigo es un desafío diferente, no te aburres nunca."),
            (j,  326243, 5, date(2025, 2, 1), "Elden Ring es puro masoquismo del bueno, no puedo parar."),
            (m,  326243, 5, date(2025, 2, 2), "El mundo abierto de FromSoftware es una revolución."),
            (c,  326243, 5, date(2025, 2, 3), "Los jefes finales son los más épicos que he visto en ningún juego."),
            (a,  326243, 5, date(2025, 2, 4), "Difícil pero increíblemente justo, cada muerte es un aprendizaje."),
            (l,  326243, 4, date(2025, 2, 5), "George R.R. Martin y Miyazaki juntos son una combinación brutal."),
            (m,  5679, 5, date(2024, 12, 20), "Skyrim es el juego al que siempre vuelvo, la nostalgia es real."),
            (c,  5679, 4, date(2024, 12, 21), "Las mazmorras son infinitas, nunca te quedas sin contenido."),
            (d,  5679, 5, date(2024, 12, 22), "Los mods lo hacen prácticamente un juego nuevo cada vez."),
            (r,  5679, 5, date(2024, 12, 23), "El sistema de progresión de habilidades es increíblemente adictivo."),
            (s,  5679, 4, date(2024, 12, 24), "Bethesda sabe crear mundos que te enganchan durante cientos de horas."),
            (j,  13536, 5, date(2025, 1, 5), "Half-Life 2 inventó el shooter moderno, es una referencia absoluta."),
            (m,  13536, 5, date(2025, 1, 6), "La física del Gravity Gun cambió los FPS para siempre."),
            (c,  13536, 5, date(2025, 1, 7), "Sigue siendo uno de los mejores juegos de la historia."),
            (j,  28, 5, date(2025, 1, 20), "Red Dead Redemption tiene la mejor historia del oeste en videojuegos."),
            (a,  28, 4, date(2025, 1, 21), "John Marston es un personaje con una profundidad tremenda."),
            (s,  28, 5, date(2025, 1, 22), "El final te parte el corazón, qué escritura tan brutal."),
            (r,  28, 4, date(2025, 1, 23), "El ambiente del lejano oeste está recreado a la perfección."),
            (c,  41494, 4, date(2025, 2, 10), "Tras los parches, Cyberpunk 2077 es otro juego completamente."),
            (d,  41494, 4, date(2025, 2, 11), "Night City es la ciudad más impresionante de cualquier videojuego."),
            (r,  41494, 5, date(2025, 2, 12), "La historia de V es emotiva y te engancha de principio a fin."),
            (l,  41494, 3, date(2025, 2, 13), "El DLC Phantom Liberty es mejor que el juego base, es una pasada."),
            (j,  4062, 5, date(2025, 3, 1), "Portal 2 es el mejor puzzle game jamás creado, punto."),
            (m,  4062, 5, date(2025, 3, 2), "El humor de GLaDOS y Wheatley no tiene rival en ningún juego."),
            (s,  27789, 5, date(2025, 4, 5), "Hollow Knight es la mejor metroidvania que existe, es una joya."),
        ]

        rates    = []
        comments = []
        for uid, game_id, rating, dt, txt in pares:
            rates.append(Rate(id_user=uid, id_game_api=game_id, date_rate=dt, rating=rating))
            comments.append(Comment(id_user=uid, id_videogame=game_id, description=txt, date_of_comment=dt))

        db.session.add_all(rates)
        db.session.add_all(comments)
        db.session.commit()

        statuses_map = [
            (j, 3328, "completado"), (m, 3328, "completado"), (c, 3328, "completado"),
            (a, 3328, "completado"), (l, 3328, "jugando"),    (s, 3328, "completado"),
            (d, 3328, "completado"), (r, 3328, "pendiente"),
            (j, 3498, "completado"), (m, 3498, "jugando"),    (c, 3498, "completado"),
            (a, 3498, "completado"), (l, 3498, "pendiente"),  (s, 3498, "completado"),
            (d, 3498, "jugando"),
            (j, 58175, "completado"), (m, 58175, "completado"), (c, 58175, "completado"),
            (a, 58175, "jugando"),    (l, 58175, "completado"), (s, 58175, "pendiente"),
            (j, 326243, "jugando"),    (m, 326243, "completado"), (c, 326243, "pendiente"),
            (a, 326243, "completado"), (d, 326243, "jugando"),    (r, 326243, "completado"),
            (m, 5679, "completado"), (c, 5679, "completado"), (d, 5679, "completado"),
            (r, 5679, "jugando"),    (s, 5679, "pendiente"),
            (c, 41494, "completado"), (d, 41494, "jugando"),    (r, 41494, "completado"),
            (l, 41494, "pendiente"),  (a, 41494, "completado"),
            (j, 28, "completado"), (a, 28, "completado"), (s, 28, "jugando"), (r, 28, "pendiente"),
            (j, 13536, "completado"), (d, 13536, "completado"), (m, 13536, "completado"),
            (a, 4062, "completado"), (r, 4062, "completado"),
            (s, 27789, "jugando"), (j, 27789, "pendiente"),
        ]

        statuses = [
            UserGameStatus(id_user=u, id_game_api=g, status=st)
            for u, g, st in statuses_map
        ]
        db.session.add_all(statuses)
        db.session.commit()

        print(f"Seed completado: {len(users)} usuarios, "
              f"{len(favorites)} favoritos, {len(rates)} valoraciones, "
              f"{len(comments)} comentarios, {len(statuses)} estados.")
