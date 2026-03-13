from app.database.db import db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    date_of_registration = Column(Date, nullable=False, default=datetime.now())
    role = Column(String(20), nullable=False)

    comentarios = relationship('Comment', back_populates="usuarios")

    def __init__(self, id, name, last_name, email, role, date_of_registration=datetime.now()):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.date_of_registration = date_of_registration