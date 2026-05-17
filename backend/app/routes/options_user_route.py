from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import user_service
from app.repositories.user_repo import get_user_by_id
from app.autorizacion.validadores import admin_required
from app.limiter import limiter
from app.models.UserGameStatus import UserGameStatus
from app.models.Favorite import Favorite
from app.models.Rate import Rate
from app.models.Comment import Comment
from sqlalchemy import func
from app.database.db import db

user_option_bp = Blueprint("option_route", __name__)

@user_option_bp.route("/options", methods=["PUT"])
@jwt_required()
def edit_user():
    try:
        usuario_actual_id = get_jwt_identity()
        datos_actualizacion = request.get_json()

        id_usuario = datos_actualizacion.get("id_user")

        usuario_actual = get_user_by_id(usuario_actual_id)
        if usuario_actual.role != 'admin' and int(id_usuario) != int(usuario_actual_id):
            return jsonify({"message": "No tienes permisos para editar este usuario"}), 403

        nombre_usuario = datos_actualizacion.get("name")
        apellido_usuario = datos_actualizacion.get("last_name")
        nickname_usuario = datos_actualizacion.get("nickname")
        email_usuario = datos_actualizacion.get("email")
        contraseña_usuario = datos_actualizacion.get("password")

        usuario_actualizado = user_service.user_update(user_id=id_usuario,
                                                       name=nombre_usuario,
                                                       last_name=apellido_usuario,
                                                       nickname=nickname_usuario,
                                                       email=email_usuario,
                                                       passwd=contraseña_usuario)

        if type(usuario_actualizado) != str:
            return jsonify({"message": "Usuario actualizado exitosamente",
                            "user": usuario_actualizado.to_dict()}), 200
        else:
            return jsonify({"message": usuario_actualizado}), 409
    except Exception as error:
        return jsonify({"message": "Error al actualizar el usuario"}), 500

@user_option_bp.route("/options", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user():
    try:
        datos_eliminacion = request.get_json()

        id_usuario = datos_eliminacion.get("id_user")

        resultado_eliminacion = user_service.user_delete(user_id=id_usuario)

        if type(resultado_eliminacion) != str:
            return jsonify({"message": "Usuario eliminado exitosamente"}), 200
        else:
            return jsonify({"message": resultado_eliminacion}), 404
    except Exception as error:
        return jsonify({"message": "Error al eliminar el usuario"}), 500

@user_option_bp.route("/options", methods=["GET"])
@jwt_required()
@admin_required
def get_list_users():
    try:
        usuario_actual_id = get_jwt_identity()
        usuarios = user_service.get_list_users(exclude_user_id=usuario_actual_id)
        usuarios_dict = []

        for usuario in usuarios:
            usuarios_dict.append(usuario.to_dict())

        return jsonify({"message": "Lista de usuarios obtenida exitosamente",
                        "users": usuarios_dict}), 200

    except Exception as error:
        return jsonify({"message": "Error al obtener la lista de usuarios"}), 500

@user_option_bp.route("/change-role", methods=["PUT"])
@jwt_required()
@admin_required
def change_role():
    try:
        datos_rol = request.get_json()

        id_usuario = datos_rol.get("id_user")
        nuevo_rol = datos_rol.get("new_role")

        ROLES_PERMITIDOS = {"user", "admin"}

        if not id_usuario or not nuevo_rol:
            return jsonify({"message": "id_user y new_role son obligatorios"}), 400

        if nuevo_rol not in ROLES_PERMITIDOS:
            return jsonify({"message": "Rol no válido"}), 400

        usuario_actualizado = user_service.change_role(user_id=id_usuario, new_role=nuevo_rol)

        if type(usuario_actualizado) != str:
            return jsonify({"message": "Rol del usuario actualizado exitosamente",
                            "user": usuario_actualizado.to_dict()}), 200
        else:
            return jsonify({"message": usuario_actualizado}), 404
    except ValueError as error_validacion:
        return jsonify({"message": str(error_validacion)}), 400
    except Exception as error:
        return jsonify({"message": "Error al actualizar el rol del usuario"}), 500

@user_option_bp.route("/account", methods=["DELETE"])
@jwt_required()
@limiter.limit("3 per minute")
def delete_own_account():
    try:
        usuario_actual_id = get_jwt_identity()

        resultado = user_service.user_delete(user_id=usuario_actual_id)

        if type(resultado) != str:
            return jsonify({"message": "Cuenta eliminada exitosamente"}), 200
        else:
            return jsonify({"message": resultado}), 404
    except Exception as error:
        return jsonify({"message": "Error al eliminar la cuenta"}), 500


@user_option_bp.route("/change-password", methods=["PUT"])
@jwt_required()
@limiter.limit("5 per minute")
def change_password():
    try:
        usuario_actual_id = get_jwt_identity()
        datos_cambio = request.get_json()

        contraseña_actual = datos_cambio.get("current_password")
        contraseña_nueva = datos_cambio.get("new_password")

        if not contraseña_actual or not contraseña_nueva:
            return jsonify({"message": "Las contraseñas actual y nueva son obligatorias"}), 400

        resultado = user_service.change_password(
            user_id=usuario_actual_id,
            contraseña_actual=contraseña_actual,
            contraseña_nueva=contraseña_nueva
        )

        if type(resultado) != str:
            return jsonify({"message": "Contraseña actualizada exitosamente",
                            "user": resultado.to_dict()}), 200
        else:
            return jsonify({"message": resultado}), 400

    except Exception as error:
        return jsonify({"message": "Error al cambiar la contraseña"}), 500


@user_option_bp.route("/stats", methods=["GET"])
@jwt_required()
def obtener_estadisticas():
    try:
        id_user = get_jwt_identity()

        estados = db.session.query(
            UserGameStatus.status,
            func.count(UserGameStatus.id_status)
        ).filter(UserGameStatus.id_user == id_user).group_by(UserGameStatus.status).all()
        estados_dict = {e[0]: e[1] for e in estados}

        total_favs = db.session.query(func.count(Favorite.fav_id)).filter(Favorite.user_id == id_user).scalar() or 0

        total_comentarios = db.session.query(func.count(Comment.id_comment)).filter(Comment.id_user == id_user).scalar() or 0

        ratings = db.session.query(Rate.rating).filter(Rate.id_user == id_user).all()
        valores = [r[0] for r in ratings]
        rating_medio = round(sum(valores) / len(valores), 1) if valores else None

        return jsonify({
            "coleccion": {
                "total": sum(estados_dict.values()),
                "completado": estados_dict.get("completado", 0),
                "jugando": estados_dict.get("jugando", 0),
                "pendiente": estados_dict.get("pendiente", 0),
                "pausado": estados_dict.get("pausado", 0)
            },
            "favoritos": total_favs,
            "comentarios": total_comentarios,
            "valoraciones": len(valores),
            "rating_medio": rating_medio
        }), 200

    except Exception as error:
        return jsonify({"message": "Error al obtener estadísticas"}), 500