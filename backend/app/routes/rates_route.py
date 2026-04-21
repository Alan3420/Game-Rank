from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.rate_services import crear_valoracion, actualizar_valoracion, eliminar_valoracion, get_media_juego, get_valoraciones_juego, get_valoraciones_usuario, get_estado_juego

rates_bp = Blueprint("rates", __name__)


@rates_bp.route("/create", methods=["POST"])
@jwt_required()
def create():
    try:
        data    = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")
        rating  = data.get("rating")
        status  = data.get("status")

        if not id_game or not rating:
            return jsonify({"message": "id_game y rating son obligatorios"}), 400

        resultado = crear_valoracion(id_user=id_user, id_game=id_game,
                                     rating=rating, status=status)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({"message": "Valoración creada",
                        "rate": resultado.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": "Error al crear la valoración",
                        "error": str(e)}), 500


@rates_bp.route("/update", methods=["PUT"])
@jwt_required()
def update():
    try:
        data    = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")
        rating  = data.get("rating")
        status  = data.get("status")

        if not id_game:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = actualizar_valoracion(id_user=id_user, id_game=id_game,
                                          rating=rating, status=status)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Valoración actualizada",
                        "rate": resultado.to_dict()}), 200
    except Exception as e:
        return jsonify({"message": "Error al actualizar la valoración",
                        "error": str(e)}), 500

@rates_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete():
    try:
        data    = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")

        if not id_game:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = eliminar_valoracion(id_user=id_user, id_game=id_game)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Valoración eliminada"}), 200
    except Exception as e:
        return jsonify({"message": "Error al eliminar la valoración",
                        "error": str(e)}), 500
    

@rates_bp.route("/avg/<int:game_id>", methods=["GET"])
def get_avg(game_id):
    try:
        avg = get_media_juego(id_game=game_id)
        return jsonify({"game_id": game_id, "avg_rating": avg}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener la media",
                        "error": str(e)}), 500


@rates_bp.route("/game/<int:game_id>", methods=["GET"])
def get_by_game(game_id):
    try:
        rates = get_valoraciones_juego(id_game=game_id)
        return jsonify({"rates": rates}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener valoraciones",
                        "error": str(e)}), 500

@rates_bp.route("/user", methods=["GET"])
@jwt_required()
def get_by_user():
    try:
        id_user = get_jwt_identity()
        rates   = get_valoraciones_usuario(id_user=id_user)
        return jsonify({"rates": rates}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener valoraciones",
                        "error": str(e)}), 500


@rates_bp.route("/status", methods=["GET"])
@jwt_required()
def get_status():
    try:
        data    = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")

        if not id_game:
            return jsonify({"message": "id_game es obligatorio"}), 400

        status = get_estado_juego(id_user=id_user, id_game=id_game)

        if not status:
            return jsonify({"message": "No tienes valoración para este juego"}), 404

        return jsonify({"status": status}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener el estado",
                        "error": str(e)}), 500