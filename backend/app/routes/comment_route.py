from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_services import crear_comentario, actualizar_comentario, eliminar_comentario, get_comentarios_juego, get_comentarios_usuario
from app.services import user_service
from app.repositories.user_repo import get_user_by_id
from app.limiter import limiter

comment_bp = Blueprint("comment", __name__)

@comment_bp.route("/create", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def create():
    try:
        data = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")
        description = data.get("description")

        if not id_game or not description:
            return jsonify({"message": "id_game y description son obligatorios"}), 400

        if len(description) > 255:
            return jsonify({"message": "El comentario no puede superar los 255 caracteres"}), 400

        resultado = crear_comentario(id_user=id_user, id_game=id_game,
                                      description=description)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({"message": "Comentario creado",
                        "comment": resultado.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": "Error al crear el comentario"}), 500

@comment_bp.route("/update/<int:comment_id>", methods=["PUT"])
@jwt_required()
@limiter.limit("10 per minute")
def update(comment_id):
    try:
        data = request.get_json()
        description = data.get("description")

        if not description:
            return jsonify({"message": "description es obligatoria"}), 400

        if len(description) > 255:
            return jsonify({"message": "El comentario no puede superar los 255 caracteres"}), 400

        user_id = get_jwt_identity()
        usuario = get_user_by_id(user_id)
        es_admin = usuario.role == 'admin' if usuario else False

        resultado = actualizar_comentario(comment_id=comment_id,
                                           description=description,
                                           user_id=user_id,
                                           es_admin=es_admin)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Comentario actualizado",
                        "comment": resultado.to_dict()}), 200
    except Exception as e:
        return jsonify({"message": "Error al actualizar el comentario"}), 500

@comment_bp.route("/delete/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete(comment_id):
    try:
        user_id = get_jwt_identity()
        usuario = get_user_by_id(user_id)
        es_admin = usuario.role == 'admin' if usuario else False

        resultado = eliminar_comentario(comment_id, user_id, es_admin=es_admin)

        if resultado is True:
            return jsonify({"msg": "Comentario eliminado"}), 200

        return jsonify({"msg": resultado}), 403

    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@comment_bp.route("/game/<int:game_id>", methods=["GET"])
def get_by_game(game_id):
    try:
        comments = get_comentarios_juego(id_game=game_id)
        return jsonify({"comments": comments}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener comentarios"}), 500

@comment_bp.route("/user", methods=["GET"])
@jwt_required()
def get_by_user():
    try:
        id_user  = get_jwt_identity()
        comments = get_comentarios_usuario(id_user=id_user)
        user = user_service.get_user_by_id(id_user=id_user)
        
        return jsonify({"comments": comments, "user": user}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener comentarios"}), 500

