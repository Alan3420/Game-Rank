from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from app.services.game_services import get_video_game_details, get_video_game_by_name_details, get_video_games_pagination, save_games, get_upcoming_launch_games, get_random_game_video, get_video_games_filtered, obtener_saga_servicio


content_overview_bp = Blueprint('content_overview_route', __name__)


@content_overview_bp.route('/overview', methods=["GET"])
@jwt_required()
def overview():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        name = request.args.get('name', default=None, type=str)

        games = get_video_games_pagination(page=page, per_page=per_page)

        save_games(games=games.get("games", []), app=current_app._get_current_object())
        

        if name:
            games = [g for g in games if name.lower() in g["name"].lower()]

        return jsonify(games), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los juegos", "error": str(e)}), 500

@content_overview_bp.route('/search', methods=["GET"])
@jwt_required()
def search_by_name():
    try:
        name = request.args.get('name', default=None, type=str)

        if not name:
            return jsonify({"message": "Nombre requerido"}), 400

        games = get_video_game_by_name_details(game_name=name)
        save_games(games=games, app=current_app._get_current_object())

        return jsonify(games), 200
    except Exception as e:
        return jsonify({"message": "Error al buscar el juego", "error": str(e)}), 500
    

@content_overview_bp.route('/overview/<int:game_id>', methods=["GET"])
@jwt_required()
def overview_by_id(game_id):
    try:
        game_details = get_video_game_details(game_id=game_id)
        return jsonify(game_details), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los detalles del juego", "error": str(e)}), 500


@content_overview_bp.route("/release", methods=["GET"])
@jwt_required()
def future_release():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        games = get_upcoming_launch_games(page=page, per_page=per_page)
        save_games(games=games, app=current_app._get_current_object())


        return jsonify(games), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener los juegos", "error": str(e)}), 500


@content_overview_bp.route('/filtered', methods=["GET"])
@jwt_required()
def filtered_games():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        ordering = request.args.get('ordering', default=None, type=str)
        genres = request.args.get('genres', default=None, type=str)
        platforms = request.args.get('platforms', default=None, type=str)
        dates = request.args.get('dates', default=None, type=str)
        search = request.args.get('search', default=None, type=str)

        games = get_video_games_filtered(
            page=page,
            per_page=per_page,
            ordering=ordering,
            genres=genres,
            platforms=platforms,
            dates=dates,
            search=search
        )
        save_games(games=games.get("games", []), app=current_app._get_current_object())

        return jsonify(games), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los juegos filtrados", "error": str(e)}), 500


@content_overview_bp.route('/overview/<int:game_id>/saga', methods=["GET"])
@jwt_required()
def saga_del_juego(game_id):
    try:
        juegos = obtener_saga_servicio(game_id=game_id)
        return jsonify(juegos), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener saga del juego", "error": str(e)}), 500


@content_overview_bp.route("/hero-video", methods=["GET"])
def get_hero_video():
    try:
        video = get_random_game_video()

        if not video:
            return jsonify({"message": "No hay videos disponibles"}), 404

        return jsonify(video), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener video", "error": str(e)}), 500
