from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from app.services.game_services import (
    obtener_detalle_del_videojuego,
    obtener_juegos_del_catalogo,
    guardar_juegos,
    obtener_proximos_lanzamientos,
    obtener_video_aleatorio,
    obtener_juegos_filtrados,
    obtener_saga,
    obtener_adicciones_del_juego,
    obtener_logros_del_juego
)
from app.limiter import limiter


# Endpoints que devuelven datos de juegos (catalogo, detalles, busqueda
# con filtros, proximos lanzamientos, video del hero, saga, DLC, logros).
# La mayoria pegan contra la API de RAWG por debajo.

content_overview_bp = Blueprint('content_overview_route', __name__)


@content_overview_bp.route('/overview/<int:game_id>', methods=["GET"])
@jwt_required()
def detalle_de_juego(game_id):
    try:
        detalles = obtener_detalle_del_videojuego(id_juego=game_id)
        return jsonify(detalles), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener los detalles del juego"}), 500


@content_overview_bp.route("/release", methods=["GET"])
@jwt_required()
def proximos_lanzamientos():
    try:
        pagina = request.args.get('page', default=1, type=int)
        por_pagina = min(request.args.get('per_page', default=10, type=int), 40)

        juegos = obtener_proximos_lanzamientos(pagina=pagina, por_pagina=por_pagina)

        # Guardamos los juegos en BD en segundo plano para poder enlazarlos
        # con favoritos/comentarios/etc. cuando el usuario interactue.
        guardar_juegos(juegos=juegos, app=current_app._get_current_object())

        return jsonify(juegos), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener los juegos"}), 500


@content_overview_bp.route('/catalog', methods=["GET"])
@jwt_required()
@limiter.limit("60 per minute")
def juegos_del_catalogo():
    try:
        pagina = request.args.get('page', default=1, type=int)
        por_pagina = min(request.args.get('per_page', default=20, type=int), 40)

        resultado = obtener_juegos_del_catalogo(pagina=pagina, por_pagina=por_pagina)

        guardar_juegos(
            juegos=resultado.get("games", []),
            app=current_app._get_current_object()
        )

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener el catálogo"}), 500


@content_overview_bp.route('/filtered', methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def juegos_filtrados():
    try:
        pagina = request.args.get('page', default=1, type=int)
        por_pagina = min(request.args.get('per_page', default=20, type=int), 40)
        ordering = request.args.get('ordering', default=None, type=str)
        genres = request.args.get('genres', default=None, type=str)
        platforms = request.args.get('platforms', default=None, type=str)
        dates = request.args.get('dates', default=None, type=str)
        search = request.args.get('search', default=None, type=str)

        resultado = obtener_juegos_filtrados(
            pagina=pagina,
            por_pagina=por_pagina,
            ordering=ordering,
            genres=genres,
            platforms=platforms,
            dates=dates,
            search=search
        )

        guardar_juegos(
            juegos=resultado.get("games", []),
            app=current_app._get_current_object()
        )

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener los juegos filtrados"}), 500


@content_overview_bp.route('/overview/<int:game_id>/adicciones', methods=["GET"])
@jwt_required()
def adicciones_del_juego(game_id):
    try:
        adicciones = obtener_adicciones_del_juego(id_juego=game_id)
        return jsonify(adicciones), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener adicciones"}), 500


@content_overview_bp.route('/overview/<int:game_id>/saga', methods=["GET"])
@jwt_required()
def saga_del_juego(game_id):
    try:
        juegos = obtener_saga(id_juego=game_id)
        return jsonify(juegos), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener saga del juego"}), 500


@content_overview_bp.route('/overview/<int:game_id>/logros', methods=["GET"])
@jwt_required()
def logros_del_juego(game_id):
    try:
        logros = obtener_logros_del_juego(id_juego=game_id)
        return jsonify(logros), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener logros"}), 500


@content_overview_bp.route("/hero-video", methods=["GET"])
@limiter.limit("30 per minute")
def video_destacado():
    # Endpoint publico (sin jwt_required). El video se muestra en el hero
    # del Home antes de que el usuario inicie sesion.
    try:
        video = obtener_video_aleatorio()

        if not video:
            return jsonify({"message": "No hay videos disponibles"}), 404

        return jsonify(video), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener video"}), 500
