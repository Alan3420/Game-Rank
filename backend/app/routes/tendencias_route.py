from flask import Blueprint, jsonify
from app.services.tendencias_service import obtener_tendencias
from app.limiter import limiter

tendencias_bp = Blueprint("tendencias_bp", __name__)


@tendencias_bp.route("/", methods=["GET"])
@limiter.limit("60 per minute")
def get_tendencias():
    try:
        datos = obtener_tendencias()
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500
