from app.database.db import db
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    id_comment = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, primary_key=True, nullable=False)
    description = Column(String(255), nullable=False)
    date_of_comment = Column(Date, nullable=False, default=datetime.now())

