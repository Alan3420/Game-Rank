from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_services import (
    crear_comentario,
    actualizar_comentario,
    eliminar_comentario,
    obtener_comentarios_del_juego,
    obtener_comentarios_del_usuario,
    obtener_todos_los_comentarios
)
from app.services import user_service
from app.repositories.user_repo import obtener_usuario_por_id
from app.limiter import limiter
from app.autorizacion.validadores import admin_required


comment_bp = Blueprint("comment", __name__)


@comment_bp.route("/create", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def crear():
    try:
        datos = request.get_json()
        id_usuario = get_jwt_identity()
        id_juego = datos.get("id_game")
        descripcion = datos.get("description")

        if not id_juego or not descripcion:
            return jsonify({"message": "id_game y description son obligatorios"}), 400

        if len(descripcion) > 255:
            return jsonify({"message": "El comentario no puede superar los 255 caracteres"}), 400

        resultado = crear_comentario(
            id_usuario=id_usuario,
            id_juego=id_juego,
            descripcion=descripcion
        )

        if type(resultado) == str:
            return jsonify({"message": resultado}), 409

        return jsonify({
            "message": "Comentario creado",
            "comment": resultado.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"message": "Error al crear el comentario"}), 500


@comment_bp.route("/update/<int:comment_id>", methods=["PUT"])
@jwt_required()
@limiter.limit("10 per minute")
def actualizar(comment_id):
    try:
        datos = request.get_json()
        descripcion = datos.get("description")

        if not descripcion:
            return jsonify({"message": "description es obligatoria"}), 400

        if len(descripcion) > 255:
            return jsonify({"message": "El comentario no puede superar los 255 caracteres"}), 400

        id_usuario = get_jwt_identity()
        usuario = obtener_usuario_por_id(id_usuario)

        es_admin = False
        if usuario and usuario.role == 'admin':
            es_admin = True

        resultado = actualizar_comentario(
            id_comentario=comment_id,
            descripcion=descripcion,
            id_usuario=id_usuario,
            es_admin=es_admin
        )

        if type(resultado) == str:
            return jsonify({"message": resultado}), 404

        return jsonify({
            "message": "Comentario actualizado",
            "comment": resultado.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"message": "Error al actualizar el comentario"}), 500


@comment_bp.route("/delete/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def eliminar(comment_id):
    try:
        id_usuario = get_jwt_identity()
        usuario = obtener_usuario_por_id(id_usuario)

        es_admin = False
        if usuario and usuario.role == 'admin':
            es_admin = True

        resultado = eliminar_comentario(
            id_comentario=comment_id,
            id_usuario=id_usuario,
            es_admin=es_admin
        )

        if resultado is True:
            return jsonify({"msg": "Comentario eliminado"}), 200

        return jsonify({"msg": resultado}), 403

    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@comment_bp.route("/game/<int:game_id>", methods=["GET"])
@jwt_required()
def obtener_por_juego(game_id):
    try:
        # Topes para que nadie pida 5000 comentarios de golpe
        limite = min(request.args.get('limit', default=10, type=int), 40)
        desplazamiento = max(request.args.get('offset', default=0, type=int), 0)

        datos = obtener_comentarios_del_juego(
            id_juego=game_id,
            limite=limite,
            desplazamiento=desplazamiento
        )
        return jsonify(datos), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener comentarios"}), 500


@comment_bp.route("/all", methods=["GET"])
@jwt_required()
@admin_required
@limiter.limit("30 per minute")
def obtener_todos_admin():
    try:
        comentarios = obtener_todos_los_comentarios()
        return jsonify({"comments": comentarios}), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener comentarios"}), 500


@comment_bp.route("/user", methods=["GET"])
@jwt_required()
def obtener_por_usuario():
    try:
        id_usuario = get_jwt_identity()
        comentarios = obtener_comentarios_del_usuario(id_usuario=id_usuario)
        usuario = user_service.obtener_usuario_por_id(id_usuario=id_usuario)

        usuario_dict = None
        if usuario:
            usuario_dict = usuario.to_dict()

        return jsonify({
            "comments": comentarios,
            "user": usuario_dict
        }), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener comentarios"}), 500
