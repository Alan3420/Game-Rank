from app.repositories import user_repo
from app.models.User import User


def user_authentication(name_user, passwd) -> User |None:

    user = user_repo.get_user_by_username(name_user)

    if user and user.password == passwd:
        return user
    
    return None


def user_registration(name, last_name, email, passwd, role) -> User | None:

    if user_authentication(name, passwd) == None:
        new_user = user_repo.create_user(username=name, last_name=last_name, email=email, password=passwd, role=role)

        return new_user
    
    return None


    
