from datetime import date

SEED_EMAILS = [
    "juan@gmail.com", "maria@gmail.com", "carlos@gmail.com", "ana@gmail.com",
    "luis@gmail.com", "sofia@gmail.com", "diego@gmail.com", "laura@gmail.com",
]

# IDs reales de la API de RAWG
SEED_GAME_IDS = [3328, 3498, 4062, 5679, 13536, 28, 41494, 58175, 326243, 27789]


def seed(app, db, User, Comment, Video_game, Rate, Favorite, UserGameStatus):
    with app.app_context():

        # ── Limpiar datos previos del seed ──
        existing_games = [
            g.id_game_api for g in
            Video_game.query.filter(Video_game.id_game_api.in_(SEED_GAME_IDS)).all()
        ]
        if existing_games:
            # CASCADE elimina favorites, rates, comments y user_game_status relacionados
            Video_game.query.filter(
                Video_game.id_game_api.in_(existing_games)
            ).delete(synchronize_session=False)
            db.session.commit()

        User.query.filter(User.email.in_(SEED_EMAILS)).delete(synchronize_session=False)
        db.session.commit()

        # ── Usuarios ──
        users = [
            User("Juan",   "Pérez",      "juan@gmail.com",   "password123"),
            User("María",  "Gómez",      "maria@gmail.com",  "password456"),
            User("Carlos", "López",      "carlos@gmail.com", "password789"),
            User("Ana",    "Martínez",   "ana@gmail.com",    "password321"),
            User("Luis",   "Sánchez",    "luis@gmail.com",   "password654"),
            User("Sofía",  "García",     "sofia@gmail.com",  "password987"),
            User("Diego",  "Rodríguez",  "diego@gmail.com",  "password147"),
            User("Laura",  "Fernández",  "laura@gmail.com",  "password258"),
        ]
        db.session.add_all(users)
        db.session.flush()   # asigna IDs sin hacer commit aún

        j  = users[0].id_user   # Juan
        m  = users[1].id_user   # María
        c  = users[2].id_user   # Carlos
        a  = users[3].id_user   # Ana
        l  = users[4].id_user   # Luis
        s  = users[5].id_user   # Sofía
        d  = users[6].id_user   # Diego
        r  = users[7].id_user   # Laura

        # ── Videojuegos (RAWG IDs) ──
        video_games = [
            Video_game(id_game_api=3328,   name="The Witcher 3: Wild Hunt",   date_release=date(2015, 5, 19),  platforms="PC, PS4, PS5, Xbox One, Switch",         development_company="CD Projekt Red"),
            Video_game(id_game_api=3498,   name="Grand Theft Auto V",         date_release=date(2013, 9, 17),  platforms="PC, PS3, PS4, PS5, Xbox 360, Xbox One",  development_company="Rockstar Games"),
            Video_game(id_game_api=4062,   name="Portal 2",                   date_release=date(2011, 4, 19),  platforms="PC, PS3, Xbox 360",                      development_company="Valve"),
            Video_game(id_game_api=5679,   name="The Elder Scrolls V: Skyrim",date_release=date(2011, 11, 11), platforms="PC, PS3, PS4, Xbox 360, Xbox One, Switch",development_company="Bethesda Game Studios"),
            Video_game(id_game_api=13536,  name="Half-Life 2",                date_release=date(2004, 11, 16), platforms="PC",                                     development_company="Valve"),
            Video_game(id_game_api=28,     name="Red Dead Redemption",        date_release=date(2010, 5, 18),  platforms="PS3, Xbox 360",                          development_company="Rockstar San Diego"),
            Video_game(id_game_api=41494,  name="Cyberpunk 2077",             date_release=date(2020, 12, 10), platforms="PC, PS4, PS5, Xbox One, Xbox Series",    development_company="CD Projekt Red"),
            Video_game(id_game_api=58175,  name="God of War",                 date_release=date(2018, 4, 20),  platforms="PS4, PS5, PC",                           development_company="Santa Monica Studio"),
            Video_game(id_game_api=326243, name="Elden Ring",                 date_release=date(2022, 2, 25),  platforms="PC, PS4, PS5, Xbox One, Xbox Series",    development_company="FromSoftware"),
            Video_game(id_game_api=27789,  name="Hollow Knight",              date_release=date(2017, 2, 24),  platforms="PC, PS4, Xbox One, Switch",              development_company="Team Cherry"),
        ]
        db.session.add_all(video_games)
        db.session.commit()

        # ── Favoritos ──
        # Witcher 3 (3328): 8 users — 1º en favoritos
        # GTA V     (3498): 7 users — 2º
        # God of War(58175): 6 users — 3º
        # Elden Ring(326243): 5 users — 4º
        # Skyrim    (5679): 5 users — 5º
        # Cyberpunk (41494): 4 users — 6º
        # RDR       (28):   4 users — 7º
        # Half-Life (13536): 3 users — 8º
        # Portal 2  (4062): 2 users — 9º
        # Hollow    (27789): 1 user  — 10º
        favorites = [
            # The Witcher 3
            Favorite(user_id=j, id_game_api=3328,   date_added=date(2024, 11, 1)),
            Favorite(user_id=m, id_game_api=3328,   date_added=date(2024, 11, 2)),
            Favorite(user_id=c, id_game_api=3328,   date_added=date(2024, 11, 3)),
            Favorite(user_id=a, id_game_api=3328,   date_added=date(2024, 11, 4)),
            Favorite(user_id=l, id_game_api=3328,   date_added=date(2024, 11, 5)),
            Favorite(user_id=s, id_game_api=3328,   date_added=date(2024, 11, 6)),
            Favorite(user_id=d, id_game_api=3328,   date_added=date(2024, 11, 7)),
            Favorite(user_id=r, id_game_api=3328,   date_added=date(2024, 11, 8)),
            # GTA V
            Favorite(user_id=j, id_game_api=3498,   date_added=date(2024, 11, 10)),
            Favorite(user_id=m, id_game_api=3498,   date_added=date(2024, 11, 11)),
            Favorite(user_id=c, id_game_api=3498,   date_added=date(2024, 11, 12)),
            Favorite(user_id=a, id_game_api=3498,   date_added=date(2024, 11, 13)),
            Favorite(user_id=l, id_game_api=3498,   date_added=date(2024, 11, 14)),
            Favorite(user_id=s, id_game_api=3498,   date_added=date(2024, 11, 15)),
            Favorite(user_id=d, id_game_api=3498,   date_added=date(2024, 11, 16)),
            # God of War
            Favorite(user_id=j, id_game_api=58175,  date_added=date(2024, 12, 1)),
            Favorite(user_id=m, id_game_api=58175,  date_added=date(2024, 12, 2)),
            Favorite(user_id=c, id_game_api=58175,  date_added=date(2024, 12, 3)),
            Favorite(user_id=a, id_game_api=58175,  date_added=date(2024, 12, 4)),
            Favorite(user_id=l, id_game_api=58175,  date_added=date(2024, 12, 5)),
            Favorite(user_id=s, id_game_api=58175,  date_added=date(2024, 12, 6)),
            # Elden Ring
            Favorite(user_id=j, id_game_api=326243, date_added=date(2025, 1, 1)),
            Favorite(user_id=m, id_game_api=326243, date_added=date(2025, 1, 2)),
            Favorite(user_id=c, id_game_api=326243, date_added=date(2025, 1, 3)),
            Favorite(user_id=a, id_game_api=326243, date_added=date(2025, 1, 4)),
            Favorite(user_id=l, id_game_api=326243, date_added=date(2025, 1, 5)),
            # Skyrim
            Favorite(user_id=m, id_game_api=5679,   date_added=date(2024, 12, 10)),
            Favorite(user_id=c, id_game_api=5679,   date_added=date(2024, 12, 11)),
            Favorite(user_id=d, id_game_api=5679,   date_added=date(2024, 12, 12)),
            Favorite(user_id=r, id_game_api=5679,   date_added=date(2024, 12, 13)),
            Favorite(user_id=s, id_game_api=5679,   date_added=date(2024, 12, 14)),
            # Cyberpunk
            Favorite(user_id=c, id_game_api=41494,  date_added=date(2025, 2, 1)),
            Favorite(user_id=d, id_game_api=41494,  date_added=date(2025, 2, 2)),
            Favorite(user_id=r, id_game_api=41494,  date_added=date(2025, 2, 3)),
            Favorite(user_id=l, id_game_api=41494,  date_added=date(2025, 2, 4)),
            # Red Dead Redemption
            Favorite(user_id=j, id_game_api=28,     date_added=date(2025, 1, 15)),
            Favorite(user_id=a, id_game_api=28,     date_added=date(2025, 1, 16)),
            Favorite(user_id=s, id_game_api=28,     date_added=date(2025, 1, 17)),
            Favorite(user_id=r, id_game_api=28,     date_added=date(2025, 1, 18)),
            # Half-Life 2
            Favorite(user_id=j, id_game_api=13536,  date_added=date(2025, 3, 1)),
            Favorite(user_id=d, id_game_api=13536,  date_added=date(2025, 3, 2)),
            Favorite(user_id=m, id_game_api=13536,  date_added=date(2025, 3, 3)),
            # Portal 2
            Favorite(user_id=a, id_game_api=4062,   date_added=date(2025, 3, 10)),
            Favorite(user_id=r, id_game_api=4062,   date_added=date(2025, 3, 11)),
            # Hollow Knight
            Favorite(user_id=s, id_game_api=27789,  date_added=date(2025, 4, 1)),
        ]
        db.session.add_all(favorites)
        db.session.commit()

        # ── Valoraciones ──
        rates = [
            # The Witcher 3 — avg ~4.9
            Rate(id_user=j, id_game_api=3328,   date_rate=date(2024, 11, 10), rating=5),
            Rate(id_user=m, id_game_api=3328,   date_rate=date(2024, 11, 11), rating=5),
            Rate(id_user=c, id_game_api=3328,   date_rate=date(2024, 11, 12), rating=5),
            Rate(id_user=a, id_game_api=3328,   date_rate=date(2024, 11, 13), rating=5),
            Rate(id_user=l, id_game_api=3328,   date_rate=date(2024, 11, 14), rating=5),
            Rate(id_user=s, id_game_api=3328,   date_rate=date(2024, 11, 15), rating=4),
            Rate(id_user=d, id_game_api=3328,   date_rate=date(2024, 11, 16), rating=5),
            Rate(id_user=r, id_game_api=3328,   date_rate=date(2024, 11, 17), rating=5),
            # God of War — avg ~4.9
            Rate(id_user=j, id_game_api=58175,  date_rate=date(2024, 12, 1),  rating=5),
            Rate(id_user=m, id_game_api=58175,  date_rate=date(2024, 12, 2),  rating=5),
            Rate(id_user=c, id_game_api=58175,  date_rate=date(2024, 12, 3),  rating=5),
            Rate(id_user=a, id_game_api=58175,  date_rate=date(2024, 12, 4),  rating=5),
            Rate(id_user=l, id_game_api=58175,  date_rate=date(2024, 12, 5),  rating=5),
            Rate(id_user=s, id_game_api=58175,  date_rate=date(2024, 12, 6),  rating=4),
            Rate(id_user=d, id_game_api=58175,  date_rate=date(2024, 12, 7),  rating=5),
            Rate(id_user=r, id_game_api=58175,  date_rate=date(2024, 12, 8),  rating=5),
            # Half-Life 2 — avg ~4.8
            Rate(id_user=j, id_game_api=13536,  date_rate=date(2025, 1, 5),   rating=5),
            Rate(id_user=m, id_game_api=13536,  date_rate=date(2025, 1, 6),   rating=5),
            Rate(id_user=c, id_game_api=13536,  date_rate=date(2025, 1, 7),   rating=5),
            Rate(id_user=a, id_game_api=13536,  date_rate=date(2025, 1, 8),   rating=5),
            Rate(id_user=l, id_game_api=13536,  date_rate=date(2025, 1, 9),   rating=4),
            # Elden Ring — avg ~4.8
            Rate(id_user=j, id_game_api=326243, date_rate=date(2025, 2, 1),   rating=5),
            Rate(id_user=m, id_game_api=326243, date_rate=date(2025, 2, 2),   rating=5),
            Rate(id_user=c, id_game_api=326243, date_rate=date(2025, 2, 3),   rating=5),
            Rate(id_user=a, id_game_api=326243, date_rate=date(2025, 2, 4),   rating=5),
            Rate(id_user=l, id_game_api=326243, date_rate=date(2025, 2, 5),   rating=4),
            Rate(id_user=s, id_game_api=326243, date_rate=date(2025, 2, 6),   rating=5),
            Rate(id_user=d, id_game_api=326243, date_rate=date(2025, 2, 7),   rating=5),
            # Portal 2 — avg ~4.7
            Rate(id_user=j, id_game_api=4062,   date_rate=date(2025, 3, 1),   rating=5),
            Rate(id_user=m, id_game_api=4062,   date_rate=date(2025, 3, 2),   rating=5),
            Rate(id_user=c, id_game_api=4062,   date_rate=date(2025, 3, 3),   rating=5),
            Rate(id_user=a, id_game_api=4062,   date_rate=date(2025, 3, 4),   rating=4),
            Rate(id_user=l, id_game_api=4062,   date_rate=date(2025, 3, 5),   rating=5),
            # Skyrim — avg ~4.5
            Rate(id_user=m, id_game_api=5679,   date_rate=date(2024, 12, 20), rating=5),
            Rate(id_user=c, id_game_api=5679,   date_rate=date(2024, 12, 21), rating=4),
            Rate(id_user=d, id_game_api=5679,   date_rate=date(2024, 12, 22), rating=5),
            Rate(id_user=r, id_game_api=5679,   date_rate=date(2024, 12, 23), rating=5),
            Rate(id_user=s, id_game_api=5679,   date_rate=date(2024, 12, 24), rating=4),
            Rate(id_user=l, id_game_api=5679,   date_rate=date(2024, 12, 25), rating=4),
            Rate(id_user=a, id_game_api=5679,   date_rate=date(2024, 12, 26), rating=5),
            # Red Dead Redemption — avg ~4.5
            Rate(id_user=j, id_game_api=28,     date_rate=date(2025, 1, 20),  rating=5),
            Rate(id_user=a, id_game_api=28,     date_rate=date(2025, 1, 21),  rating=4),
            Rate(id_user=s, id_game_api=28,     date_rate=date(2025, 1, 22),  rating=5),
            Rate(id_user=r, id_game_api=28,     date_rate=date(2025, 1, 23),  rating=4),
            Rate(id_user=d, id_game_api=28,     date_rate=date(2025, 1, 24),  rating=5),
            # GTA V — avg ~4.3
            Rate(id_user=j, id_game_api=3498,   date_rate=date(2024, 11, 20), rating=5),
            Rate(id_user=m, id_game_api=3498,   date_rate=date(2024, 11, 21), rating=4),
            Rate(id_user=c, id_game_api=3498,   date_rate=date(2024, 11, 22), rating=4),
            Rate(id_user=a, id_game_api=3498,   date_rate=date(2024, 11, 23), rating=5),
            Rate(id_user=l, id_game_api=3498,   date_rate=date(2024, 11, 24), rating=4),
            Rate(id_user=s, id_game_api=3498,   date_rate=date(2024, 11, 25), rating=4),
            # Cyberpunk — avg ~4.0
            Rate(id_user=c, id_game_api=41494,  date_rate=date(2025, 2, 10),  rating=4),
            Rate(id_user=d, id_game_api=41494,  date_rate=date(2025, 2, 11),  rating=4),
            Rate(id_user=r, id_game_api=41494,  date_rate=date(2025, 2, 12),  rating=5),
            Rate(id_user=l, id_game_api=41494,  date_rate=date(2025, 2, 13),  rating=3),
            Rate(id_user=m, id_game_api=41494,  date_rate=date(2025, 2, 14),  rating=4),
            # Hollow Knight — avg ~4.7
            Rate(id_user=s, id_game_api=27789,  date_rate=date(2025, 4, 5),   rating=5),
            Rate(id_user=a, id_game_api=27789,  date_rate=date(2025, 4, 6),   rating=4),
            Rate(id_user=j, id_game_api=27789,  date_rate=date(2025, 4, 7),   rating=5),
        ]
        db.session.add_all(rates)
        db.session.commit()

        # ── Comentarios ──
        texts = {
            3328:   ["Una obra maestra, la mejor experiencia RPG de mi vida.",
                     "El mejor juego de rol que he jugado jamás, historia increíble.",
                     "Cada DLC vale lo que pesa, Blood and Wine es espectacular.",
                     "El mundo abierto más vivo que existe en un videojuego.",
                     "Geralt es el personaje mejor escrito de la historia de los RPG.",
                     "100 horas y sigo sin cansarme. Obra de arte total.",
                     "La banda sonora te pone los pelos de punta en cada combate.",
                     "Imposible que no te enamore este juego, es perfecto."],
            3498:   ["El mundo de GTA V sigue siendo increíble después de tantos años.",
                     "Online es adictivo, pero la historia también merece la pena.",
                     "Tres protagonistas que funcionan a la perfección juntos.",
                     "Rockstar en su máximo esplendor, una ciudad viva de verdad.",
                     "La misión final es de las mejores que he jugado.",
                     "Siguen sacando contenido después de 10 años, increíble.",
                     "Trevor es el personaje más loco de la historia de los videojuegos."],
            58175:  ["La historia de Kratos y Atreus te llega al alma.",
                     "El combate es brutal y satisfactorio al máximo nivel.",
                     "Santa Monica hizo un reboot perfecto, redefinió la saga.",
                     "Los gráficos son una barbaridad, parece una película de Hollywood.",
                     "El final me dejó sin palabras, la mejor aventura que he vivido.",
                     "Cada enemigo es un desafío diferente, no te aburres nunca."],
            326243: ["Elden Ring es puro masoquismo del bueno, no puedo parar.",
                     "El mundo abierto de FromSoftware es una revolución.",
                     "Los jefes finales son los más épicos que he visto en ningún juego.",
                     "Difícil pero increíblemente justo, cada muerte es un aprendizaje.",
                     "George R.R. Martin y Miyazaki juntos son una combinación brutal."],
            5679:   ["Skyrim es el juego al que siempre vuelvo, la nostalgia es real.",
                     "Las mazmorras aleatorias son infinitas, nunca te quedas sin contenido.",
                     "Los mods lo hacen prácticamente un juego nuevo cada vez.",
                     "El sistema de progresión de habilidades es adictivo.",
                     "Bethesda sabe crear mundos que te enganchan durante cientos de horas."],
            13536:  ["Half-Life 2 inventó el shooter moderno, referencia absoluta.",
                     "La física del Gravity Gun cambió los FPS para siempre.",
                     "Sigue siendo uno de los mejores juegos de la historia."],
            28:     ["Red Dead Redemption tiene la mejor historia del oeste en videojuegos.",
                     "John Marston es un personaje con una profundidad tremenda.",
                     "El final te parte el corazón, qué escritura tan brutal.",
                     "El ambiente del lejano oeste está recreado a la perfección."],
            41494:  ["Tras los parches, Cyberpunk 2077 es otro juego completamente.",
                     "Night City es la ciudad más impresionante de cualquier videojuego.",
                     "La historia de V es emotiva y te engancha de principio a fin.",
                     "El DLC Phantom Liberty es mejor que el juego base."],
            4062:   ["Portal 2 es el mejor puzzle game jamás creado, punto.",
                     "El humor de GLaDOS y Wheatley no tiene rival."],
            27789:  ["Hollow Knight es la mejor metroidvania que existe, es una joya."],
        }

        user_cycle = [j, m, c, a, l, s, d, r]
        comments = []
        base_date = date(2024, 10, 1)
        day_offset = 0
        for game_id, txts in texts.items():
            for i, txt in enumerate(txts):
                u = user_cycle[i % len(user_cycle)]
                comments.append(Comment(
                    id_user=u,
                    id_videogame=game_id,
                    description=txt,
                    date_of_comment=date(
                        base_date.year,
                        base_date.month,
                        min(base_date.day + day_offset, 28)
                    )
                ))
                day_offset = (day_offset + 3) % 25

        db.session.add_all(comments)
        db.session.commit()

        # ── Estados de colección ──
        statuses_map = [
            # (user, game_id, status)
            # The Witcher 3 — 8 usuarios
            (j, 3328, "completado"), (m, 3328, "completado"), (c, 3328, "completado"),
            (a, 3328, "completado"), (l, 3328, "jugando"),    (s, 3328, "completado"),
            (d, 3328, "completado"), (r, 3328, "pendiente"),
            # GTA V — 7 usuarios
            (j, 3498, "completado"), (m, 3498, "jugando"),    (c, 3498, "completado"),
            (a, 3498, "completado"), (l, 3498, "pendiente"),  (s, 3498, "completado"),
            (d, 3498, "jugando"),
            # God of War — 6 usuarios
            (j, 58175, "completado"), (m, 58175, "completado"), (c, 58175, "completado"),
            (a, 58175, "jugando"),    (l, 58175, "completado"), (s, 58175, "pendiente"),
            # Elden Ring — 6 usuarios
            (j, 326243, "jugando"),    (m, 326243, "completado"), (c, 326243, "pendiente"),
            (a, 326243, "completado"), (d, 326243, "jugando"),    (r, 326243, "completado"),
            # Skyrim — 5 usuarios
            (m, 5679, "completado"), (c, 5679, "completado"), (d, 5679, "completado"),
            (r, 5679, "jugando"),    (s, 5679, "pendiente"),
            # Cyberpunk — 5 usuarios
            (c, 41494, "completado"), (d, 41494, "jugando"),    (r, 41494, "completado"),
            (l, 41494, "pendiente"),  (a, 41494, "completado"),
            # Red Dead Redemption — 4 usuarios
            (j, 28, "completado"), (a, 28, "completado"), (s, 28, "jugando"), (r, 28, "pendiente"),
            # Half-Life 2 — 4 usuarios
            (j, 13536, "completado"), (d, 13536, "completado"), (m, 13536, "completado"), (l, 13536, "pendiente"),
            # Portal 2 — 3 usuarios
            (a, 4062, "completado"), (r, 4062, "completado"), (s, 4062, "jugando"),
            # Hollow Knight — 2 usuarios
            (s, 27789, "jugando"), (j, 27789, "pendiente"),
        ]

        statuses = [
            UserGameStatus(id_user=u, id_game_api=g, status=st)
            for u, g, st in statuses_map
        ]
        db.session.add_all(statuses)
        db.session.commit()

        print(f"Seed completado: {len(users)} usuarios, {len(video_games)} juegos, "
              f"{len(favorites)} favoritos, {len(rates)} valoraciones, "
              f"{len(comments)} comentarios, {len(statuses)} estados.")
