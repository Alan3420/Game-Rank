from flask import Blueprint, jsonify, request
from app.services.game_services import get_video_game_details, get_video_game_by_name_details



content_overview_bp = Blueprint('content_overview_route', __name__)

@content_overview_bp.route('/overview')  
def get_content():

    try:
        get_game_id = request.args.get('game_id') 
        game_name = request.args.get('game_name')

        if not get_game_id and not game_name:
            return jsonify({"error": "Debes enviar 'game_id' o 'game_name'"}), 400

        if game_name and game_name.strip() == "":
            return jsonify({"error": "El nombre del juego no puede estar vacío"}), 400

        if get_game_id:
            game = get_video_game_details(get_game_id)
        else:
            game = get_video_game_by_name_details(game_name)

        return jsonify(game), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
