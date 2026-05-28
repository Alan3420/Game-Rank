from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.favorite_services import (
    agregar_favorito,
    eliminar_favorito,
    obtener_favoritos_del_usuario,
    es_favorito
)


favorite_bp = Blueprint("favorite", __name__)


@favorite_bp.route("/add", methods=["POST"])
@jwt_required()
def agregar():
    try:
        datos = request.get_json()
        id_usuario = get_jwt_identity()
        id_juego = datos.get("id_game")

        if not id_juego:
            return jsonify({"message": "id_game es obligatorio"}), 400

        resultado = agregar_favorito(id_usuario=id_usuario, id_juego=id_juego)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({
            "message": "Juego añadido a favoritos",
            "favorite": resultado.to_dict()
        }), 201

    except Exception as e:
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

    except Exception as e:
        return jsonify({"message": "Error al eliminar favorito"}), 500


@favorite_bp.route("/listFav", methods=["GET"])
@jwt_required()
def listar_favoritos():
    try:
        id_usuario = get_jwt_identity()
        favoritos = obtener_favoritos_del_usuario(id_usuario=id_usuario)
        return jsonify({"favorites": favoritos}), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener favoritos"}), 500


@favorite_bp.route("/check/<int:game_id>", methods=["GET"])
@jwt_required()
def comprobar(game_id):
    try:
        id_usuario = get_jwt_identity()
        es_fav = es_favorito(id_usuario=id_usuario, id_juego=game_id)
        return jsonify({"is_favorite": es_fav}), 200

    except Exception as e:
        return jsonify({"message": "Error al comprobar favorito"}), 500
