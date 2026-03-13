from app.database.db import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

class Comment(db.Model):
    __tablename__ = 'comments'

    id_comment = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(255), nullable=False)
    date_of_comment = Column(Date, nullable=False, default=date.today())

    usuarios = db.relationship('User', back_populates="comentarios")

    def __init__(self, id_comment, id_user, description, date_of_comment=date.today()):
        self.id_comment = id_comment
        self.id_user = id_user
        self.description = description
        self.date_of_comment = date_of_comment

