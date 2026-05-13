from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.tierlist_services import (
    crear_nueva_tierlist, obtener_tierlist_completa, listar_tierlists_usuario,
    renombrar_tierlist, borrar_tierlist,
    agregar_juego_a_tierlist, mover_juego_en_tierlist, quitar_juego_de_tierlist
)

tierlist_bp = Blueprint("tierlist", __name__)


@tierlist_bp.route("/create", methods=["POST"])
@jwt_required()
def crear():
    try:
        data = request.get_json()
        id_user = get_jwt_identity()
        title = data.get("title")

        if not title:
            return jsonify({"message": "El titulo es obligatorio"}), 400

        resultado = crear_nueva_tierlist(id_user=id_user, title=title)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 400

        return jsonify({"message": "Tierlist creada",
                        "tierlist": resultado.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": "Error al crear la tierlist",
                        "error": str(e)}), 500


@tierlist_bp.route("/list", methods=["GET"])
@jwt_required()
def listar():
    try:
        id_user = get_jwt_identity()
        tierlists = listar_tierlists_usuario(id_user=id_user)
        return jsonify({"tierlists": tierlists}), 200
    except Exception as e:
        return jsonify({"message": "Error al listar las tierlists",
                        "error": str(e)}), 500


@tierlist_bp.route("/<int:id_tierlist>", methods=["GET"])
@jwt_required()
def obtener(id_tierlist):
    try:
        id_user = get_jwt_identity()
        resultado = obtener_tierlist_completa(id_tierlist=id_tierlist, id_user=id_user)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"tierlist": resultado}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener la tierlist",
                        "error": str(e)}), 500


@tierlist_bp.route("/<int:id_tierlist>/rename", methods=["PUT"])
@jwt_required()
def renombrar(id_tierlist):
    try:
        data = request.get_json()
        id_user = get_jwt_identity()
        nuevo_titulo = data.get("title")

        resultado = renombrar_tierlist(id_tierlist=id_tierlist,
                                       id_user=id_user,
                                       nuevo_titulo=nuevo_titulo)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 400

        return jsonify({"message": "Titulo actualizado",
                        "tierlist": resultado.to_dict()}), 200
    except Exception as e:
        return jsonify({"message": "Error al renombrar la tierlist",
                        "error": str(e)}), 500


@tierlist_bp.route("/<int:id_tierlist>", methods=["DELETE"])
@jwt_required()
def eliminar(id_tierlist):
    try:
        id_user = get_jwt_identity()
        resultado = borrar_tierlist(id_tierlist=id_tierlist, id_user=id_user)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Tierlist eliminada"}), 200
    except Exception as e:
        return jsonify({"message": "Error al eliminar la tierlist",
                        "error": str(e)}), 500


@tierlist_bp.route("/<int:id_tierlist>/add", methods=["POST"])
@jwt_required()
def agregar_juego(id_tierlist):
    try:
        data = request.get_json()
        id_user = get_jwt_identity()
        id_game_api = data.get("id_game")
        rank = data.get("rank")

        if not id_game_api or not rank:
            return jsonify({"message": "id_game y rank son obligatorios"}), 400

        resultado = agregar_juego_a_tierlist(
            id_tierlist=id_tierlist,
            id_user=id_user,
            id_game_api=id_game_api,
            rank=rank
        )

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({"message": "Juego agregado",
                        "item": resultado.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": "Error al agregar el juego",
                        "error": str(e)}), 500


@tierlist_bp.route("/item/<int:id_item>/move", methods=["PUT"])
@jwt_required()
def mover_juego(id_item):
    try:
        data = request.get_json()
        id_user = get_jwt_identity()
        nuevo_rank = data.get("rank")

        if not nuevo_rank:
            return jsonify({"message": "rank es obligatorio"}), 400

        resultado = mover_juego_en_tierlist(
            id_item=id_item,
            id_user=id_user,
            nuevo_rank=nuevo_rank
        )

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({"message": "Juego movido",
                        "item": resultado.to_dict()}), 200
    except Exception as e:
        return jsonify({"message": "Error al mover el juego",
                        "error": str(e)}), 500


@tierlist_bp.route("/item/<int:id_item>", methods=["DELETE"])
@jwt_required()
def quitar_juego(id_item):
    try:
        id_user = get_jwt_identity()
        resultado = quitar_juego_de_tierlist(id_item=id_item, id_user=id_user)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Juego quitado de la tierlist"}), 200
    except Exception as e:
        return jsonify({"message": "Error al quitar el juego",
                        "error": str(e)}), 500
