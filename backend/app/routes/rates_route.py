from flask import Blueprint,jsonify, request
from app.services.rate_services import actualizar_valoracion, create_rate, eliminar_valoracion

rates_bp = Blueprint("rates", __name__)

@rates_bp.route("/management", methods=["GET", "PUT", "DELETE"])
def rate_oprions():

    pass

def edit_rate():
    date_rate_update = request.get_json()

    pass