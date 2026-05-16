from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_game_status_service import (
    establecer_status, obtener_status_juego, listar_statuses_usuario,
    listar_statuses_con_juegos, quitar_status
)

status_bp = Blueprint("status", __name__)


@status_bp.route("/set", methods=["POST"])
@jwt_required()
def set_status():
    try:
        data = request.get_json()
        id_user = int(get_jwt_identity())
        id_game = data.get("id_game")
        status = data.get("status")

        if not id_game or not status:
            return jsonify({"message": "id_game y status son obligatorios"}), 400

        resultado = establecer_status(id_user=id_user, id_game=id_game, status=status)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 400

        return jsonify({"message": "Status actualizado",
                        "status": resultado.to_dict()}), 200
    except Exception as e:
        return jsonify({"message": "Error al establecer el status"}), 500


@status_bp.route("/<int:id_game>", methods=["GET"])
@jwt_required()
def get_status(id_game):
    try:
        id_user = int(get_jwt_identity())
        registro = obtener_status_juego(id_user=id_user, id_game=id_game)

        if not registro:
            return jsonify({"status": None}), 200

        return jsonify({"status": registro.to_dict()}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener el status"}), 500


@status_bp.route("/list", methods=["GET"])
@jwt_required()
def list_statuses():
    try:
        id_user = int(get_jwt_identity())
        registros = listar_statuses_usuario(id_user=id_user)
        return jsonify({"statuses": registros}), 200
    except Exception as e:
        return jsonify({"message": "Error al listar los statuses"}), 500


@status_bp.route("/list/full", methods=["GET"])
@jwt_required()
def list_statuses_full():
    try:
        id_user = int(get_jwt_identity())
        registros = listar_statuses_con_juegos(id_user=id_user)
        return jsonify({"statuses": registros}), 200
    except Exception as e:
        return jsonify({"message": "Error al listar los statuses con juegos"}), 500


@status_bp.route("/<int:id_game>", methods=["DELETE"])
@jwt_required()
def delete_status(id_game):
    try:
        id_user = int(get_jwt_identity())
        resultado = quitar_status(id_user=id_user, id_game=id_game)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Status eliminado"}), 200
    except Exception as e:
        return jsonify({"message": "Error al eliminar el status"}), 500