from app.repositories import user_repo
from app.models.User import User

import re

DOMINIOS_PERMITIDOS = {
    "gmail.com", "hotmail.com", "hotmail.es",
    "outlook.com", "outlook.es",
    "yahoo.com",  "yahoo.es",
    "icloud.com", "live.com",
}

_NICKNAME_RE = re.compile(r'^[a-zA-Z0-9_]{3,30}$')

def _dominio_valido(email: str) -> bool:
    partes = email.split("@")
    return len(partes) == 2 and partes[1].lower() in DOMINIOS_PERMITIDOS

def _nickname_valido(nickname: str) -> bool:
    return bool(_NICKNAME_RE.match(nickname))


def user_authentication(email, passwd) -> User |None:

    user = user_repo.get_user_by_email(email)

    if user and user.check_password(password=passwd):
        return user
    
    return None


def user_registration(name, last_name, nickname, email, passwd) -> User | str:

    try:
        if not name or len(name) < 1 or len(name) > 50:
            return "El nombre debe tener entre 1 y 50 caracteres"

        if not last_name or len(last_name) < 1 or len(last_name) > 50:
            return "El apellido debe tener entre 1 y 50 caracteres"

        if not nickname or not _nickname_valido(nickname):
            return "El nickname debe tener entre 3 y 30 caracteres y solo puede contener letras, números y guiones bajos"

        if not email or len(email) > 100:
            return "El email debe tener un máximo de 100 caracteres"

        if not _dominio_valido(email):
            return "Solo se aceptan correos de Gmail, Hotmail, Outlook, Yahoo o iCloud"

        if not passwd or len(passwd) < 8:
            return "La contraseña debe tener un mínimo de 8 caracteres"

        if user_repo.get_user_by_nickname(nickname) is not None:
            return "Ese nickname ya está en uso"

        user_exist = user_repo.get_user_by_email(email)

        if user_exist is not None:
            return "Existe un usuario registrado con ese email"

        new_user = user_repo.create_user(username=name, last_name=last_name, nickname=nickname, email=email, password=passwd)

        return new_user
        
        
    
    except Exception as e:
        print("Error en el registro del usuario:", str(e))
        raise Exception("Error en el registro del usuario")
    
#Recordatorio: esta funcion solo la podrá usar el usuario con rol "ADMIN"
def get_list_users(exclude_user_id=None) -> list[User]:

    try:
        list_users = user_repo.get_all_users(exclude_user_id=exclude_user_id)

        return list_users

    except Exception as e:
        print("Error al obtener la lista de usuarios:", str(e))
        raise Exception("Error al obtener la lista de usuarios")

def user_update(user_id, name, last_name, nickname, email, passwd) -> User | str:

    try:
        user = user_repo.get_user_by_id(user_id)

        if not user:
            return "Usuario no encontrado"

        if name and (len(name) < 1 or len(name) > 50):
            return "El nombre debe tener entre 1 y 50 caracteres"

        if last_name and (len(last_name) < 1 or len(last_name) > 50):
            return "El apellido debe tener entre 1 y 50 caracteres"

        if nickname:
            if not _nickname_valido(nickname):
                return "El nickname debe tener entre 3 y 30 caracteres y solo puede contener letras, números y guiones bajos"
            if nickname.lower() != (user.nickname or "").lower():
                nick_exists = user_repo.get_user_by_nickname(nickname)
                if nick_exists:
                    return "Ese nickname ya está en uso"

        if email:
            if len(email) > 100:
                return "El email debe tener un máximo de 100 caracteres"
            if not _dominio_valido(email):
                return "Solo se aceptan correos de Gmail, Hotmail, Outlook, Yahoo o iCloud"
            if email != user.email:
                email_exists = user_repo.get_user_by_email(email)
                if email_exists:
                    return "El correo electrónico ya está en uso por otro usuario"

        if passwd and len(passwd) < 8:
            return "La contraseña debe tener un mínimo de 8 caracteres"

        updated_user = user_repo.update_user(user_id=user_id, username=name, last_name=last_name, nickname=nickname, email=email, password=passwd)

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

#Recordatorio: lo mismo en esta funcion solo el admin puede cambiar los roles a los usuarios que quiera.
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

def get_user_by_id(id_user):
    return user_repo.get_user_by_id(user_id=id_user)

def change_password(user_id, contraseña_actual, contraseña_nueva) -> User | str:
    try:
        user = user_repo.get_user_by_id(user_id)

        if not user:
            return "Usuario no encontrado"

        if not user.check_password(contraseña_actual):
            return "La contraseña actual es incorrecta"

        if len(contraseña_nueva) < 8:
            return "La contraseña debe tener un mínimo de 8 caracteres"

        if contraseña_actual == contraseña_nueva:
            return "La nueva contraseña debe ser diferente a la actual"

        usuario_actualizado = user_repo.update_user(user_id=user_id, password=contraseña_nueva)

        return usuario_actualizado

    except Exception as e:
        print("Error al cambiar la contraseña:", str(e))
        raise Exception("Error al cambiar la contraseña")

