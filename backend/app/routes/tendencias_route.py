from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.services.tendencias_service import obtener_tendencias
from app.limiter import limiter


# Endpoint unico que devuelve las cuatro listas de tendencias de la
# comunidad. Como el calculo implica varias consultas + llamadas a RAWG,
# aplicamos rate-limit para evitar abuso.

tendencias_bp = Blueprint("tendencias_bp", __name__)


@tendencias_bp.route("/", methods=["GET"])
@jwt_required()
@limiter.limit("60 per minute")
def tendencias():
    try:
        datos = obtener_tendencias()
        return jsonify(datos), 200

    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500
