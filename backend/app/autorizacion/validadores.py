from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.repositories.user_repo import obtener_usuario_por_id


def admin_required(ruta_protegida):
    @wraps(ruta_protegida)
    def validar_admin(*args, **kwargs):
        id_usuario = get_jwt_identity()
        usuario = obtener_usuario_por_id(id_usuario)

        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        if usuario.role != 'admin':
            return jsonify({
                "message": "Acceso denegado. Se requieren permisos de administrador"
            }), 403

        return ruta_protegida(*args, **kwargs)
    return validar_admin


def role_required(rol_requerido):
    def decorador(ruta_protegida):
        @wraps(ruta_protegida)
        def validar_rol(*args, **kwargs):
            id_usuario = get_jwt_identity()
            usuario = obtener_usuario_por_id(id_usuario)

            if not usuario:
                return jsonify({"message": "Usuario no encontrado"}), 404

            if usuario.role != rol_requerido:
                return jsonify({
                    "message": f"Acceso denegado. Se requiere rol: {rol_requerido}"
                }), 403

            return ruta_protegida(*args, **kwargs)
        return validar_rol
    return decorador
