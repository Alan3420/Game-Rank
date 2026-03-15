from app.database.db import db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    date_of_registration = Column(Date, nullable=False, default=datetime.now)
    role = Column(String(20), nullable=False)

    comments_rl = relationship('Comment',back_populates="users_rl")
    video_games_rl = relationship("Video_game", secondary="rates", back_populates="users_rl")
    rates_rl = relationship("Rate", back_populates="users_rl")
    favorites_rl = relationship("Favorite", back_populates="users_rl")
