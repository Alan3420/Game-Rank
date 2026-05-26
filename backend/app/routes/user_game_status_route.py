from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_game_status_service import (
    establecer_estado,
    obtener_estado_del_juego,
    listar_estados_del_usuario,
    listar_estados_con_juegos,
    quitar_estado
)


# Endpoints para los estados de coleccion (pendiente, jugando, pausado,
# completado) que cada usuario asigna a sus juegos.

status_bp = Blueprint("status", __name__)


@status_bp.route("/set", methods=["POST"])
@jwt_required()
def establecer():
    try:
        datos = request.get_json()
        id_usuario = int(get_jwt_identity())
        id_juego = datos.get("id_game")
        estado = datos.get("status")

        if not id_juego or not estado:
            return jsonify({"message": "id_game y status son obligatorios"}), 400

        resultado = establecer_estado(
            id_usuario=id_usuario,
            id_juego=id_juego,
            estado=estado
        )

        if type(resultado) == str:
            return jsonify({"message": resultado}), 400

        return jsonify({
            "message": "Status actualizado",
            "status": resultado.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"message": "Error al establecer el status"}), 500


@status_bp.route("/<int:id_game>", methods=["GET"])
@jwt_required()
def obtener(id_game):
    # Devuelve el estado que el usuario tiene asignado a ese juego, o null
    # si no le ha asignado ninguno todavia.
    try:
        id_usuario = int(get_jwt_identity())
        registro = obtener_estado_del_juego(id_usuario=id_usuario, id_juego=id_game)

        if not registro:
            return jsonify({"status": None}), 200

        return jsonify({"status": registro.to_dict()}), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener el status"}), 500


@status_bp.route("/list", methods=["GET"])
@jwt_required()
def listar():
    # Lista corta (id_juego + estado) para pintar badges en las cards
    # del catalogo sin cargar mas datos.
    try:
        id_usuario = int(get_jwt_identity())
        registros = listar_estados_del_usuario(id_usuario=id_usuario)
        return jsonify({"statuses": registros}), 200

    except Exception as e:
        return jsonify({"message": "Error al listar los statuses"}), 500


@status_bp.route("/list/full", methods=["GET"])
@jwt_required()
def listar_completos():
    # Variante con datos del juego (nombre, imagen, etc.) que necesita la
    # pantalla de perfil para mostrar la coleccion entera.
    try:
        id_usuario = int(get_jwt_identity())
        registros = listar_estados_con_juegos(id_usuario=id_usuario)
        return jsonify({"statuses": registros}), 200

    except Exception as e:
        return jsonify({"message": "Error al listar los statuses con juegos"}), 500


@status_bp.route("/<int:id_game>", methods=["DELETE"])
@jwt_required()
def eliminar(id_game):
    try:
        id_usuario = int(get_jwt_identity())
        resultado = quitar_estado(id_usuario=id_usuario, id_juego=id_game)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Status eliminado"}), 200

    except Exception as e:
        return jsonify({"message": "Error al eliminar el status"}), 500
