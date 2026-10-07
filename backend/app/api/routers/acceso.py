from fastapi import APIRouter, Depends, Request

from app.api.esquemas import DatosLogin, DatosRegistro
from app.api.limites import limiter
from app.api.respuestas import responder
from app.api.seguridad import crear_token, id_usuario_actual
from app.repositories.user_repo import obtener_usuario_por_id
from app.services import user_service

router = APIRouter(prefix="/user", tags=["Acceso"])


@router.post("/login")
@limiter.limit("10 per minute")
def iniciar_sesion(request: Request, datos: DatosLogin):
    usuario = user_service.autenticar_usuario(datos.email, datos.password)

    if usuario:
        return responder({
            "message": "Login exitoso",
            "user": usuario.to_dict(),
            "token": crear_token(usuario.id_user)
        }, 200)

    return responder({"message": "Correo electronico o contraseña incorrectos"}, 401)


@router.post("/register")
@limiter.limit("5 per minute")
def registrar(request: Request, datos: DatosRegistro):
    try:
        resultado = user_service.registrar_usuario(
            nombre=datos.name,
            apellido=datos.last_name,
            nickname=datos.nickname,
            email=datos.email,
            contrasena=datos.password
        )

        if type(resultado) != str:
            return responder({
                "message": "Usuario registrado exitosamente",
                "user": resultado.to_dict()
            }, 201)

        return responder({"message": resultado}, 409)

    except Exception:
        return responder({"message": "Error al registrar el usuario"}, 500)


@router.get("/me")
def obtener_mi_usuario(id_usuario: str = Depends(id_usuario_actual)):
    usuario = obtener_usuario_por_id(id_usuario)

    if not usuario:
        return responder({"message": "Usuario no encontrado"}, 404)

    return responder({"user": usuario.to_dict()}, 200)
