from app.services import user_service
from flask import Blueprint, request, jsonify

welcome_bp = Blueprint('welcome_route', __name__)

@welcome_bp.route("/login", methods=["POST"])
def login():
    data_log = request.get_json()

    email = data_log.get("email")
    passwd = data_log.get("password")
    

    user = user_service.user_authentication(email, passwd)

    if user:
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    