from app.database.db import db
from sqlalchemy import Column, Integer, String

class Prueba(db.Model):
    __tablename__ = 'prueba'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __init__(self, name):
        self.name = name
        