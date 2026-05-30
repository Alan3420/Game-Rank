from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.favorite_services import (
    agregar_favorito,
    eliminar_favorito,
    obtener_favoritos_del_usuario,
    es_favorito,
    actualizar_status,
    obtener_estado_del_juego,
    quitar_status,
    listar_favoritos_con_status,
    listar_favoritos_completos
)


favorite_bp = Blueprint("favorite", __name__)


@favorite_bp.route("/add", methods=["POST"])
@jwt_required()
def agregar():
    try:
        datos = request.get_json()
        id_usuario = get_jwt_identity()
        id_juego = datos.get("id_game")
        status = datos.get("status")

        if not id_juego:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = agregar_favorito(id_usuario=id_usuario, id_juego=id_juego, status=status)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({
            "message": "Juego añadido a favoritos",
            "favorite": resultado.to_dict()
        }), 201

    except Exception:
        return jsonify({"message": "Error al añadir favorito"}), 500


@favorite_bp.route("/remove", methods=["DELETE"])
@jwt_required()
def quitar():
    try:
        datos = request.get_json()
        id_usuario = get_jwt_identity()
        id_juego = datos.get("id_game")

        if not id_juego:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = eliminar_favorito(id_usuario=id_usuario, id_juego=id_juego)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Juego eliminado de favoritos"}), 200

    except Exception:
        return jsonify({"message": "Error al eliminar favorito"}), 500


@favorite_bp.route("/status", methods=["PUT"])
@jwt_required()
def actualizar_estado():
    try:
        datos = request.get_json()
        id_usuario = int(get_jwt_identity())
        id_juego = datos.get("id_game")
        nuevo_status = datos.get("status")

        if not id_juego or not nuevo_status:
            return jsonify({"message": "id_game y status son obligatorios"}), 400

        resultado = actualizar_status(
            id_usuario=id_usuario,
            id_juego=id_juego,
            nuevo_status=nuevo_status
        )

        if type(resultado) == str:
            return jsonify({"message": resultado}), 400

        return jsonify({
            "message": "Status actualizado",
            "favorite": resultado.to_dict()
        }), 200

    except Exception:
        return jsonify({"message": "Error al actualizar el status"}), 500


@favorite_bp.route("/status/<int:game_id>", methods=["GET"])
@jwt_required()
def obtener_estado(game_id):
    try:
        id_usuario = int(get_jwt_identity())
        favorito = obtener_estado_del_juego(id_usuario=id_usuario, id_juego=game_id)

        if not favorito:
            return jsonify({"status": None}), 200

        return jsonify({"status": favorito.to_dict()}), 200

    except Exception:
        return jsonify({"message": "Error al obtener el status"}), 500


@favorite_bp.route("/status/<int:game_id>", methods=["DELETE"])
@jwt_required()
def eliminar_estado(game_id):
    try:
        id_usuario = int(get_jwt_identity())
        resultado = quitar_status(id_usuario=id_usuario, id_juego=game_id)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Status eliminado"}), 200

    except Exception:
        return jsonify({"message": "Error al eliminar el status"}), 500


@favorite_bp.route("/listFav", methods=["GET"])
@jwt_required()
def listar_favoritos():
    try:
        id_usuario = get_jwt_identity()
        favoritos = obtener_favoritos_del_usuario(id_usuario=id_usuario)
        return jsonify({"favorites": favoritos}), 200

    except Exception:
        return jsonify({"message": "Error al obtener favoritos"}), 500


@favorite_bp.route("/list", methods=["GET"])
@jwt_required()
def listar_con_status():
    try:
        id_usuario = int(get_jwt_identity())
        favoritos = listar_favoritos_con_status(id_usuario=id_usuario)
        return jsonify({"statuses": favoritos}), 200

    except Exception:
        return jsonify({"message": "Error al listar estados"}), 500


@favorite_bp.route("/list/full", methods=["GET"])
@jwt_required()
def listar_completos():
    try:
        id_usuario = int(get_jwt_identity())
        resultado = listar_favoritos_completos(id_usuario=id_usuario)
        return jsonify({"statuses": resultado}), 200

    except Exception:
        return jsonify({"message": "Error al listar favoritos completos"}), 500


@favorite_bp.route("/check/<int:game_id>", methods=["GET"])
@jwt_required()
def comprobar(game_id):
    try:
        id_usuario = get_jwt_identity()
        es_fav = es_favorito(id_usuario=id_usuario, id_juego=game_id)
        return jsonify({"is_favorite": es_fav}), 200

    except Exception:
        return jsonify({"message": "Error al comprobar favorito"}), 500
