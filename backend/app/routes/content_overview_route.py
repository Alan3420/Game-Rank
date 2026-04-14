from flask import Blueprint, jsonify, request
from app.services.game_services import get_video_game_details, get_video_game_by_name_details, get_video_games_pagination



content_overview_bp = Blueprint('content_overview_route', __name__)

@content_overview_bp.route('/overview')  
def overview():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        name = request.args.get('name', default=None, type=str)

        games = get_video_games_pagination(page=page, per_page=per_page)

        if name:
            games = [g for g in games if name.lower() in g["name"].lower()]

        return jsonify(games), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los juegos", "error": str(e)}), 500

@content_overview_bp.route('/search')
def search_by_name():
    try:
        name = request.args.get('name', default=None, type=str)

        if not name:
            return jsonify({"message": "Nombre requerido"}), 400

        games = get_video_game_by_name_details(game_name=name)
        return jsonify(games), 200
    except Exception as e:
        return jsonify({"message": "Error al buscar el juego", "error": str(e)}), 500
    

@content_overview_bp.route('/overview/<int:game_id>')
def overview_by_id(game_id):
    try:
        game_details = get_video_game_details(game_id=game_id)
        return jsonify(game_details), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los detalles del juego", "error": str(e)}), 500