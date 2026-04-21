from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.favorite_services import añadir_favorito, eliminar_favorito, get_favoritos_usuario, es_favorito

favorite_bp = Blueprint("favorite", __name__)

@favorite_bp.route("/add", methods=["POST"])
@jwt_required()
def add():
    try:
        data    = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")

        if not id_game:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = añadir_favorito(id_user=id_user, id_game=id_game)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({"message": "Juego añadido a favoritos",
                        "favorite": resultado.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": "Error al añadir favorito",
                        "error": str(e)}), 500
    
    
@favorite_bp.route("/remove", methods=["DELETE"])
@jwt_required()
def remove():
    try:
        data    = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")

        if not id_game:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = eliminar_favorito(id_user=id_user, id_game=id_game)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Juego eliminado de favoritos"}), 200
    except Exception as e:
        return jsonify({"message": "Error al eliminar favorito",
                        "error": str(e)}), 500
    

@favorite_bp.route("/listFav", methods=["GET"])
@jwt_required()
def list_favorites():

    try:
        id_user   = get_jwt_identity()
        favorites = get_favoritos_usuario(id_user=id_user)

        return jsonify({"favorites": favorites}), 200
    
    except Exception as e:
        return jsonify({"message": "Error al obtener favoritos",
                        "error": str(e)}), 500

@favorite_bp.route("/check/<int:game_id>", methods=["GET"])
@jwt_required()
def check(game_id):

    try:
        id_user = get_jwt_identity()
        is_fav  = es_favorito(id_user=id_user, id_game=game_id)
        
        return jsonify({"is_favorite": is_fav}), 200
    except Exception as e:
        return jsonify({"message": "Error al comprobar favorito",
                        "error": str(e)}), 500