from app.repositories import user_repo
from app.models.User import User


def user_authentication(email, passwd) -> User |None:

    user = user_repo.get_user_by_email(email)

    if user and user.check_password(password=passwd):
        return user
    
    return None


def user_registration(name, last_name, email, passwd) -> User | str:

    try:
        user_exist = user_repo.get_user_by_email(email)

        if user_exist is not None:
            return "Existe un usuario registrado con ese email"
       
        new_user = user_repo.create_user(username=name, last_name=last_name, email=email, password=passwd)

        return new_user
        
        
    
    except Exception as e:
        print("Error en el registro del usuario:", str(e))
        raise Exception("Error en el registro del usuario")

def user_update(user_id, name, last_name, email, passwd) -> User | str:

    try:
        user = user_repo.get_user_by_id(user_id)

        if not user:
            return "Usuario no encontrado"

        if email and email != user.email:
            email_exists = user_repo.get_user_by_email(email)
            if email_exists:
                return "El correo electrónico ya está en uso por otro usuario"

        updated_user = user_repo.update_user(user_id=user_id, username=name, last_name=last_name, email=email, password=passwd)

        return updated_user
    
    except Exception as e:
        print("Error al actualizar el usuario:", str(e))
        raise Exception("Error al actualizar el usuario")
    
def user_delete(user_id) -> bool | str:

    try:
        user = user_repo.get_user_by_id(user_id)

        if not user:
            return "Usuario no encontrado"

        resultado_bool = user_repo.delete_user(user_id)

        return resultado_bool
    
    except Exception as e:
        print("Error al eliminar el usuario:", str(e))
        raise Exception("Error al eliminar el usuario")
    
def change_role(user_id, new_role) -> User | str:

    try:
        user = user_repo.get_user_by_id(user_id)

        if not user:
            return "Usuario no encontrado"

        updated_user = user_repo.update_user_role(user_id=user_id, new_role=new_role)

        return updated_user
    
    except Exception as e:
        print("Error al cambiar el rol del usuario:", str(e))
        raise Exception("Error al cambiar el rol del usuario")




    
