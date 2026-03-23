from app.database.db import db
from app.models.User import User

def get_all_users() -> list[User]:
    return User.query.all()

def get_user_by_id(user_id) -> User:
    return User.query.get(user_id)

def get_user_by_username(username) -> User:
    return User.query.filter_by(username=username).first()

def get_user_by_email(email) -> User:
    return User.query.filter_by(email=email).first()

def create_user(username, last_name, email, password) -> User:
    new_user = User(name=username, last_name=last_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def update_user(user_id, username=None, last_name=None, email=None, password=None) -> User:
    user = get_user_by_id(user_id)
    if user:
        if username:
            user.username = username
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if password:
            user.password = password
        db.session.commit()
    return user

def delete_user(user_id) -> bool:
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
