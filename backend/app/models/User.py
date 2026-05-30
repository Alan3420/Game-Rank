from app.database.db import db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    nickname = Column(String(30), nullable=True, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False, unique=True)
    date_of_registration = Column(Date, nullable=False, default=datetime.now)
    role = Column(String(20), default='user')

    comments_rl = relationship('Comment', back_populates="users_rl")
    add_favorites_rl = relationship("AddFavorite", back_populates="users_rl")

    def __init__(self, name, last_name, nickname, email, password, role='user'):
        self.name = name
        self.last_name = last_name
        self.nickname = nickname
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    
    def to_dict(self):
        return {
            "id_user": self.id_user,
            "name": self.name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "email": self.email,
            "date_of_registration": self.date_of_registration,
            "role": self.role
        }