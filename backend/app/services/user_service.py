from app.repositories import user_repo
from app.models.User import User


def user_authentication(email, passwd) -> User |None:

    user = user_repo.get_user_by_email(email)

    if user and user.check_password(password=passwd):
        return user
    
    return None


def user_registration(name, last_name, email, passwd, role) -> User:

    if user_authentication(email, passwd) == None:
        new_user = user_repo.create_user(username=name, last_name=last_name, email=email, password=passwd, role=role)

        return new_user



    
