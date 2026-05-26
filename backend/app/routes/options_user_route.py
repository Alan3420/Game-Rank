from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import user_service
from app.repositories.user_repo import obtener_usuario_por_id
from app.autorizacion.validadores import admin_required
from app.limiter import limiter
from app.models.UserGameStatus import UserGameStatus
from app.models.Favorite import Favorite
from app.models.Rate import Rate
from app.models.Comment import Comment
from sqlalchemy import func
from app.database.db import db


# Endpoints de "settings": editar perfil, cambiar contrasena, panel admin
# y estadisticas del usuario actual.

user_option_bp = Blueprint("option_route", __name__)


@user_option_bp.route("/options", methods=["PUT"])
@jwt_required()
def editar_usuario():
    try:
        id_usuario_actual = get_jwt_identity()
        datos = request.get_json()

        id_usuario_objetivo = datos.get("id_user")

        # Solo el admin puede editar la cuenta de OTRO usuario.
        # Un usuario normal solo puede editar la suya.
        usuario_actual = obtener_usuario_por_id(id_usuario_actual)
        if usuario_actual.role != 'admin' and int(id_usuario_objetivo) != int(id_usuario_actual):
            return jsonify({"message": "No tienes permisos para editar este usuario"}), 403

        resultado = user_service.actualizar_usuario(
            id_usuario=id_usuario_objetivo,
            nombre=datos.get("name"),
            apellido=datos.get("last_name"),
            nickname=datos.get("nickname"),
            email=datos.get("email"),
            contrasena=datos.get("password")
        )

        if type(resultado) != str:
            return jsonify({
                "message": "Usuario actualizado exitosamente",
                "user": resultado.to_dict()
            }), 200

        return jsonify({"message": resultado}), 409

    except Exception as e:
        return jsonify({"message": "Error al actualizar el usuario"}), 500


@user_option_bp.route("/options", methods=["DELETE"])
@jwt_required()
@admin_required
def eliminar_usuario():
    try:
        datos = request.get_json()
        id_usuario_objetivo = datos.get("id_user")

        resultado = user_service.eliminar_usuario(id_usuario=id_usuario_objetivo)

        if type(resultado) != str:
            return jsonify({"message": "Usuario eliminado exitosamente"}), 200

        return jsonify({"message": resultado}), 404

    except Exception as e:
        return jsonify({"message": "Error al eliminar el usuario"}), 500


@user_option_bp.route("/options", methods=["GET"])
@jwt_required()
@admin_required
def obtener_lista_de_usuarios():
    try:
        id_usuario_actual = get_jwt_identity()

        # Le pasamos el id del admin para que NO aparezca en la lista
        # (no tiene sentido que un admin se vea a si mismo en el panel).
        usuarios = user_service.obtener_lista_de_usuarios(excluir_id_usuario=id_usuario_actual)

        usuarios_dict = []
        for u in usuarios:
            usuarios_dict.append(u.to_dict())

        return jsonify({
            "message": "Lista de usuarios obtenida exitosamente",
            "users": usuarios_dict
        }), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener la lista de usuarios"}), 500


@user_option_bp.route("/change-role", methods=["PUT"])
@jwt_required()
@admin_required
def cambiar_rol_de_usuario():
    try:
        datos = request.get_json()

        id_usuario_objetivo = datos.get("id_user")
        nuevo_rol = datos.get("new_role")

        ROLES_PERMITIDOS = {"user", "admin"}

        if not id_usuario_objetivo or not nuevo_rol:
            return jsonify({"message": "id_user y new_role son obligatorios"}), 400

        if nuevo_rol not in ROLES_PERMITIDOS:
            return jsonify({"message": "Rol no válido"}), 400

        resultado = user_service.cambiar_rol(id_usuario=id_usuario_objetivo, nuevo_rol=nuevo_rol)

        if type(resultado) != str:
            return jsonify({
                "message": "Rol del usuario actualizado exitosamente",
                "user": resultado.to_dict()
            }), 200

        return jsonify({"message": resultado}), 404

    except ValueError as error_validacion:
        return jsonify({"message": str(error_validacion)}), 400
    except Exception as e:
        return jsonify({"message": "Error al actualizar el rol del usuario"}), 500


@user_option_bp.route("/account", methods=["DELETE"])
@jwt_required()
@limiter.limit("3 per minute")
def eliminar_propia_cuenta():
    # El usuario actual pide borrar SU PROPIA cuenta. Rate-limit 3/min
    # para evitar abuso (no es una accion que deba pulsarse en rafaga).
    try:
        id_usuario_actual = get_jwt_identity()
        resultado = user_service.eliminar_usuario(id_usuario=id_usuario_actual)

        if type(resultado) != str:
            return jsonify({"message": "Cuenta eliminada exitosamente"}), 200

        return jsonify({"message": resultado}), 404

    except Exception as e:
        return jsonify({"message": "Error al eliminar la cuenta"}), 500


@user_option_bp.route("/change-password", methods=["PUT"])
@jwt_required()
@limiter.limit("5 per minute")
def cambiar_contrasena():
    try:
        id_usuario_actual = get_jwt_identity()
        datos = request.get_json()

        contrasena_actual = datos.get("current_password")
        contrasena_nueva = datos.get("new_password")

        if not contrasena_actual or not contrasena_nueva:
            return jsonify({"message": "Las contraseñas actual y nueva son obligatorias"}), 400

        resultado = user_service.cambiar_contrasena(
            id_usuario=id_usuario_actual,
            contrasena_actual=contrasena_actual,
            contrasena_nueva=contrasena_nueva
        )

        if type(resultado) != str:
            return jsonify({
                "message": "Contraseña actualizada exitosamente",
                "user": resultado.to_dict()
            }), 200

        return jsonify({"message": resultado}), 400

    except Exception as e:
        return jsonify({"message": "Error al cambiar la contraseña"}), 500


@user_option_bp.route("/stats", methods=["GET"])
@jwt_required()
def obtener_estadisticas():
    # Estadisticas que pinta el perfil: total por estado, favoritos,
    # comentarios y media de las calificaciones del usuario actual.
    try:
        id_usuario = get_jwt_identity()

        # Conteo por estado: agrupamos las filas de user_game_status por
        # su columna "status" y contamos cuantas hay en cada uno.
        estados = db.session.query(
            UserGameStatus.status,
            func.count(UserGameStatus.id_status)
        ).filter(UserGameStatus.id_user == id_usuario)\
         .group_by(UserGameStatus.status).all()

        estados_dict = {}
        for fila in estados:
            estados_dict[fila[0]] = fila[1]

        total_favoritos = db.session.query(func.count(Favorite.fav_id))\
                                     .filter(Favorite.user_id == id_usuario)\
                                     .scalar() or 0

        total_comentarios = db.session.query(func.count(Comment.id_comment))\
                                       .filter(Comment.id_user == id_usuario)\
                                       .scalar() or 0

        # Media de las calificaciones: pedimos todos los valores y
        # calculamos la media en Python para mantener el tipo float.
        calificaciones = db.session.query(Rate.rating)\
                                    .filter(Rate.id_user == id_usuario).all()

        valores = []
        for fila in calificaciones:
            valores.append(fila[0])

        rating_medio = None
        if valores:
            rating_medio = round(sum(valores) / len(valores), 1)

        return jsonify({
            "coleccion": {
                "total": sum(estados_dict.values()),
                "completado": estados_dict.get("completado", 0),
                "jugando": estados_dict.get("jugando", 0),
                "pendiente": estados_dict.get("pendiente", 0),
                "pausado": estados_dict.get("pausado", 0)
            },
            "favoritos": total_favoritos,
            "comentarios": total_comentarios,
            "valoraciones": len(valores),
            "rating_medio": rating_medio
        }), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener estadísticas"}), 500
