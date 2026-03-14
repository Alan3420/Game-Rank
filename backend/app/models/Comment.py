from app.database.db import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

class Comment(db.Model):
    __tablename__ = 'comments'

    id_comment = Column(Integer, primary_key=True, unique=True,autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user"),primary_key=True)
    description = Column(String(255), nullable=False)
    date_of_comment = Column(Date, nullable=False, default=date.today)

    users_rl = relationship('User',back_populates="comments_rl")
    video_game_rl = relationship("Video_game", foreign_keys="[Video_game.id_comment]", back_populates="comments_rl")



