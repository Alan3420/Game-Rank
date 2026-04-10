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
    
    
    



    
