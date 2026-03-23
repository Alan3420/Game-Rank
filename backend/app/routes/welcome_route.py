from app.services import user_service
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

welcome_bp = Blueprint('welcome_route', __name__)

@welcome_bp.route("/login", methods=["POST"])
def login():
    data_log = request.get_json()

    email = data_log.get("email")
    passwd = data_log.get("password")
    

    user = user_service.user_authentication(email, passwd)

    if user:
        token_user = create_access_token(identity= str(user.id_user))
        return jsonify({"message": "Login successful",
                        "user": user.to_dict(),
                        "token": token_user}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@welcome_bp.route("/register", methods=["POST"])
def register():
    register_data = request.get_json()

    name_user = register_data.get("name")
    last_name_user = register_data.get("last_name")
    email_user = register_data.get("email")
    password_user = register_data.get("password")
    user = user_service.user_registration(name=name_user, last_name=last_name_user, email=email_user, passwd=password_user)

    if user:

        return jsonify({"message": "Registration successful", 
                        "user": user.to_dict()}), 201
    else:
        return jsonify({"message": "Email already exists"}), 400
    