from fastapi import APIRouter, Depends, Request

from app.api.esquemas import DatosCambioContrasena, DatosCambioRol, DatosEdicionUsuario, DatosUsuarioObjetivo
from app.api.limites import limiter
from app.api.respuestas import responder
from app.api.seguridad import admin_requerido, id_usuario_actual
from app.repositories.user_repo import obtener_usuario_por_id
from app.services import user_service

router = APIRouter(prefix="/settings", tags=["Cuenta y administración"])

ROLES_PERMITIDOS = {"user", "admin"}


@router.put("/options")
def editar_usuario(datos: DatosEdicionUsuario, id_usuario_actual_: str = Depends(id_usuario_actual)):
    try:
        id_usuario_objetivo = datos.id_user

        # un usuario normal solo puede editar lo suyo; el admin, cualquier cuenta
        usuario_actual = obtener_usuario_por_id(id_usuario_actual_)
        if usuario_actual.role != 'admin' and int(id_usuario_objetivo) != int(id_usuario_actual_):
            return responder({"message": "No tienes permisos para editar este usuario"}, 403)

        resultado = user_service.actualizar_usuario(
            id_usuario=id_usuario_objetivo,
            nombre=datos.name,
            apellido=datos.last_name,
            nickname=datos.nickname,
            email=datos.email,
            contrasena=datos.password
        )

        if type(resultado) != str:
            return responder({"message": "Usuario actualizado exitosamente", "user": resultado.to_dict()}, 200)

        return responder({"message": resultado}, 409)

    except Exception:
        return responder({"message": "Error al actualizar el usuario"}, 500)


@router.delete("/options")
def eliminar_usuario(datos: DatosUsuarioObjetivo, id_admin: str = Depends(admin_requerido)):
    try:
        resultado = user_service.eliminar_usuario(id_usuario=datos.id_user)

        if type(resultado) != str:
            return responder({"message": "Usuario eliminado exitosamente"}, 200)

        return responder({"message": resultado}, 404)

    except Exception:
        return responder({"message": "Error al eliminar el usuario"}, 500)


@router.get("/options")
def obtener_lista_de_usuarios(id_admin: str = Depends(admin_requerido)):
    try:
        # el admin no aparece en su propia lista
        usuarios = user_service.obtener_lista_de_usuarios(excluir_id_usuario=id_admin)
        return responder({
            "message": "Lista de usuarios obtenida exitosamente",
            "users": [u.to_dict() for u in usuarios]
        }, 200)

    except Exception:
        return responder({"message": "Error al obtener la lista de usuarios"}, 500)


@router.put("/change-role")
def cambiar_rol_de_usuario(datos: DatosCambioRol, id_admin: str = Depends(admin_requerido)):
    try:
        if not datos.id_user or not datos.new_role:
            return responder({"message": "id_user y new_role son obligatorios"}, 400)

        if datos.new_role not in ROLES_PERMITIDOS:
            return responder({"message": "Rol no válido"}, 400)

        resultado = user_service.cambiar_rol(id_usuario=datos.id_user, nuevo_rol=datos.new_role)

        if type(resultado) != str:
            return responder({"message": "Rol del usuario actualizado exitosamente", "user": resultado.to_dict()}, 200)

        return responder({"message": resultado}, 404)

    except ValueError as error_validacion:
        return responder({"message": str(error_validacion)}, 400)
    except Exception:
        return responder({"message": "Error al actualizar el rol del usuario"}, 500)


@router.delete("/account")
@limiter.limit("3 per minute")
def eliminar_propia_cuenta(request: Request, id_usuario: str = Depends(id_usuario_actual)):
    try:
        resultado = user_service.eliminar_usuario(id_usuario=id_usuario)

        if type(resultado) != str:
            return responder({"message": "Cuenta eliminada exitosamente"}, 200)

        return responder({"message": resultado}, 404)

    except Exception:
        return responder({"message": "Error al eliminar la cuenta"}, 500)


@router.put("/change-password")
@limiter.limit("5 per minute")
def cambiar_contrasena(request: Request, datos: DatosCambioContrasena, id_usuario: str = Depends(id_usuario_actual)):
    try:
        if not datos.current_password or not datos.new_password:
            return responder({"message": "Las contraseñas actual y nueva son obligatorias"}, 400)

        resultado = user_service.cambiar_contrasena(
            id_usuario=id_usuario,
            contrasena_actual=datos.current_password,
            contrasena_nueva=datos.new_password
        )

        if type(resultado) != str:
            return responder({"message": "Contraseña actualizada exitosamente", "user": resultado.to_dict()}, 200)

        return responder({"message": resultado}, 400)

    except Exception:
        return responder({"message": "Error al cambiar la contraseña"}, 500)


@router.get("/stats")
def obtener_estadisticas(id_usuario: str = Depends(id_usuario_actual)):
    try:
        return responder(user_service.obtener_estadisticas_usuario(id_usuario), 200)
    except Exception:
        return responder({"message": "Error al obtener estadísticas"}, 500)
