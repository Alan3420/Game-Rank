from flask import Blueprint, jsonify, request
from app.services.game_services import get_video_game_details



content_overview_bp = Blueprint('content_overview_route', __name__)

@content_overview_bp.route('/overview')  
def get_content():

    get_game_id = request.args.get('game_id') 

    if not get_game_id:
        return jsonify({"error": "game_id is required"}), 400
    
    game = get_video_game_details(get_game_id)
    return jsonify(game), 200
