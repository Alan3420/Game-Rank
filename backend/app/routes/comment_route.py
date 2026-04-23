from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_services import crear_comentario, actualizar_comentario,eliminar_comentario, get_comentarios_juego,get_comentarios_usuario
from app.services import user_service

comment_bp = Blueprint("comment", __name__)

@comment_bp.route("/create", methods=["POST"])
@jwt_required()
def create():
    try:
        data = request.get_json()
        id_user = get_jwt_identity()
        id_game = data.get("id_game")
        description = data.get("description")

        if not id_game or not description:
            return jsonify({"message": "id_game y description son obligatorios"}), 400

        comment = crear_comentario(id_user=id_user, id_game=id_game,
                                    description=description)

        return jsonify({"message": "Comentario creado",
                        "comment": comment.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": "Error al crear el comentario",
                        "error": str(e)}), 500

@comment_bp.route("/update/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update(comment_id):
    try:
        data = request.get_json()
        description = data.get("description")

        if not description:
            return jsonify({"message": "description es obligatoria"}), 400

        resultado = actualizar_comentario(comment_id=comment_id,
                                           description=description)

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({"message": "Comentario actualizado",
                        "comment": resultado.to_dict()}), 200
    except Exception as e:
        return jsonify({"message": "Error al actualizar el comentario",
                        "error": str(e)}), 500

@comment_bp.route("/delete/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete(comment_id):
    try:
        user_id = get_jwt_identity()
        resultado = eliminar_comentario(comment_id, user_id)
        
      
        if resultado is True:
            return jsonify({"msg": "Comentario eliminado"}), 200
        

        return jsonify({"msg": resultado}), 403 

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/game/<int:game_id>", methods=["GET"])
def get_by_game(game_id):
    try:
        comments = get_comentarios_juego(id_game=game_id)
        return jsonify({"comments": comments}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener comentarios",
                        "error": str(e)}), 500

@comment_bp.route("/user", methods=["GET"])
@jwt_required()
def get_by_user():
    try:
        id_user  = get_jwt_identity()
        comments = get_comentarios_usuario(id_user=id_user)
        user = user_service.get_user_by_id(id_user=id_user)
        
        return jsonify({"comments": comments, "user": user}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener comentarios",
                        "error": str(e)}), 500

