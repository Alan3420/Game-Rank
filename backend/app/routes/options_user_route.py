from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import user_service
from app.repositories.user_repo import obtener_usuario_por_id
from app.autorizacion.validadores import admin_required
from app.limiter import limiter


user_option_bp = Blueprint("option_route", __name__)


@user_option_bp.route("/options", methods=["PUT"])
@jwt_required()
def editar_usuario():
    try:
        id_usuario_actual = get_jwt_identity()
        datos = request.get_json()

        id_usuario_objetivo = datos.get("id_user")

        # Un usuario normal solo puede editar lo suyo, el admin puede tocar
        # la cuenta de cualquiera
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

        # Le pasamos el id del admin para que no aparezca en su propia lista
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
    try:
        id_usuario = get_jwt_identity()
        estadisticas = user_service.obtener_estadisticas_usuario(id_usuario)
        return jsonify(estadisticas), 200

    except Exception as e:
        return jsonify({"message": "Error al obtener estadísticas"}), 500
