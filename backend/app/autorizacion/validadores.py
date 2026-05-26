from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.repositories.user_repo import obtener_usuario_por_id


# Decoradores para validar permisos sobre las rutas. Se aplican DESPUES
# del decorador @jwt_required() porque dependen de poder leer la identity
# del token.


def admin_required(ruta_protegida):
    """
    Permite acceder a la ruta solo si el usuario actual tiene rol "admin".
    Si no es admin, devuelve 403; si no existe el usuario, devuelve 404.
    """
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
    """
    Version generica de admin_required: permite indicar el rol concreto
    que debe tener el usuario para acceder a la ruta. Se usa como:

        @role_required("moderador")
        def alguna_ruta(): ...

    De momento solo se usa admin_required, pero esto queda preparado por
    si en el futuro anadimos mas roles.
    """
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
