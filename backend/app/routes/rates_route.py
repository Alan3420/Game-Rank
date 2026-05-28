from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.rate_services import (
    crear_calificacion,
    actualizar_calificacion,
    eliminar_calificacion,
    obtener_promedio_del_juego,
    obtener_calificaciones_del_juego,
    obtener_calificaciones_del_usuario
)
from app.limiter import limiter


rates_bp = Blueprint("rates", __name__)


def _validar_valor_rating(rating):
    if not isinstance(rating, (int, float)) or not (1 <= rating <= 5):
        return "El rating debe ser un número entre 1 y 5"
    return None


@rates_bp.route("/create", methods=["POST"])
@jwt_required()
@limiter.limit("10 per minute")
def crear():
    try:
        datos = request.get_json()
        id_usuario = get_jwt_identity()
        id_juego = datos.get("id_game")
        rating = datos.get("rating")

        if not id_juego or rating is None:
            return jsonify({"message": "id_game y rating son obligatorios"}), 400

        error_validacion = _validar_valor_rating(rating)
        if error_validacion:
            return jsonify({"message": error_validacion}), 400

        resultado = crear_calificacion(id_usuario=id_usuario, id_juego=id_juego, valor=rating)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({
            "message": "Valoración creada",
            "rate": resultado.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"message": "Error al crear la valoración"}), 500


@rates_bp.route("/update", methods=["PUT"])
@jwt_required()
@limiter.limit("10 per minute")
def actualizar():
    try:
        datos = request.get_json()
        id_usuario = get_jwt_identity()
        id_juego = datos.get("id_game")
        rating = datos.get("rating")

        if not id_juego or rating is None:
            return jsonify({"message": "id_game y rating son obligatorios"}), 400

        error_validacion = _validar_valor_rating(rating)
        if error_validacion:
            return jsonify({"message": error_validacion}), 400

        resultado = actualizar_calificacion(id_usuario=id_usuario, id_juego=id_juego, valor=rating)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({
            "message": "Valoración actualizada",
            "rate": resultado.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"message": "Error al actualizar la valoración"}), 500


@rates_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def eliminar():
    try:
        datos = request.get_json()
        id_usuario = get_jwt_identity()
        id_juego = datos.get("id_game")

        if not id_juego:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = eliminar_calificacion(id_usuario=id_usuario, id_juego=id_juego)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Valoración eliminada"}), 200

    except Exception as e:
        return jsonify({"message": "Error al eliminar la valoración"}), 500


@rates_bp.route("/avg/<int:game_id>", methods=["GET"])
@jwt_required()
def obtener_promedio(game_id):
    try:
        promedio = obtener_promedio_del_juego(id_juego=game_id)
        return jsonify({"game_id": game_id, "avg_rating": promedio}), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener la media"}), 500


@rates_bp.route("/game/<int:game_id>", methods=["GET"])
@jwt_required()
def obtener_por_juego(game_id):
    try:
        calificaciones = obtener_calificaciones_del_juego(id_juego=game_id)
        return jsonify({"rates": calificaciones}), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener valoraciones"}), 500


@rates_bp.route("/user", methods=["GET"])
@jwt_required()
def obtener_por_usuario():
    try:
        id_usuario = get_jwt_identity()
        calificaciones = obtener_calificaciones_del_usuario(id_usuario=id_usuario)
        return jsonify({"rates": calificaciones}), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener valoraciones"}), 500
