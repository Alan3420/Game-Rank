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
        return jsonify({"message": "Login exitoso",
                        "user": user.to_dict(),
                        "token": token_user}), 200
    else:
        return jsonify({"message": "Correo electronico o contraseña incorrectos"}), 401

@welcome_bp.route("/register", methods=["POST"])
def register():
    try:
        register_data = request.get_json()

        name_user = register_data.get("name")
        last_name_user = register_data.get("last_name")
        email_user = register_data.get("email")
        password_user = register_data.get("password")
        user = user_service.user_registration(name=name_user, 
                                              last_name=last_name_user, 
                                              email=email_user, 
                                              passwd=password_user)

        if type(user) != str:

            return jsonify({"message": "Usuario registrado exitosamente", 
                            "user": user.to_dict()}), 201
        else:
            return jsonify({"message": user}), 409
    except Exception as e:
        return jsonify({"message": "Error al registrar el usuario", "error": str(e)}), 500

@welcome_bp.route("/logout")
def logout():
    return jsonify({"message": "A finalizado la sesion"}), 200


def edit_user():
    try:
        data_update = request.get_json()

        id_user = data_update.get("id_user")
        name_user = data_update.get("name")
        last_name_user = data_update.get("last_name")
        email_user = data_update.get("email")
        password_user = data_update.get("password")

        user_updated = user_service.user_update(user_id=id_user, 
                                                name=name_user, 
                                                last_name=last_name_user, 
                                                email=email_user, 
                                                passwd=password_user)

        if type(user_updated) != str:
            return jsonify({"message": "Usuario actualizado exitosamente", 
                            "user": user_updated.to_dict()}), 200
        else:
            return jsonify({"message": user_updated}), 409
    except Exception as e:
        return jsonify({"message": "Error al actualizar el usuario", "error": str(e)}), 500
    

def delete_user():
    try:
        data_delete = request.get_json()

        id_user = data_delete.get("id_user")

        resultado_delete = user_service.user_delete(user_id=id_user)

        if type(resultado_delete) != str:
            return jsonify({"message": "Usuario eliminado exitosamente"}), 200
        else:
            return jsonify({"message": resultado_delete}), 404
    except Exception as e:
        return jsonify({"message": "Error al eliminar el usuario", "error": str(e)}), 500
    
def get_list_users():

    try:
        users = user_service.get_list_users()
        user_dict = []

        for user in users:
            user_dict.append(user.to_dict())
        
        return jsonify({"message": "Lista de usuarios obtenida exitosamente",
                        "users": user_dict}), 200
    
    except Exception as e:
        return jsonify({"message": "Error al obtener la lista de usuarios", "error": str(e)}), 500

def change_role():
    try:
        data_role = request.get_json()

        id_user = data_role.get("id_user")
        new_role = data_role.get("new_role")

        user_updated = user_service.change_role(user_id=id_user, new_role=new_role)

        if type(user_updated) != str:
            return jsonify({"message": "Rol del usuario actualizado exitosamente", 
                            "user": user_updated.to_dict()}), 200
        else:
            return jsonify({"message": user_updated}), 404
    except Exception as e:
        return jsonify({"message": "Error al actualizar el rol del usuario", "error": str(e)}), 500