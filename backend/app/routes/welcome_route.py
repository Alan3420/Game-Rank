from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import user_service
from app.repositories.user_repo import obtener_usuario_por_id
from app.limiter import limiter


welcome_bp = Blueprint('welcome_route', __name__)


@welcome_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def iniciar_sesion():
    datos_login = request.get_json()

    email = datos_login.get("email")
    contrasena = datos_login.get("password")

    usuario = user_service.autenticar_usuario(email, contrasena)

    if usuario:
        # flask-jwt-extended >= 4 obliga a que la identity sea string
        token = create_access_token(identity=str(usuario.id_user))
        return jsonify({
            "message": "Login exitoso",
            "user": usuario.to_dict(),
            "token": token
        }), 200

    return jsonify({"message": "Correo electronico o contraseña incorrectos"}), 401


@welcome_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def registrar():
    try:
        datos_registro = request.get_json()

        nombre = datos_registro.get("name")
        apellido = datos_registro.get("last_name")
        nickname = datos_registro.get("nickname")
        email = datos_registro.get("email")
        contrasena = datos_registro.get("password")

        resultado = user_service.registrar_usuario(
            nombre=nombre,
            apellido=apellido,
            nickname=nickname,
            email=email,
            contrasena=contrasena
        )

        if type(resultado) != str:
            return jsonify({
                "message": "Usuario registrado exitosamente",
                "user": resultado.to_dict()
            }), 201

        return jsonify({"message": resultado}), 409

    except Exception as e:
        return jsonify({"message": "Error al registrar el usuario"}), 500


@welcome_bp.route("/me", methods=["GET"])
@jwt_required()
def obtener_mi_usuario():
    id_usuario = get_jwt_identity()
    usuario = obtener_usuario_por_id(id_usuario)

    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify({"user": usuario.to_dict()}), 200
