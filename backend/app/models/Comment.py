from app.database.db import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

class Comment(db.Model):
    __tablename__ = 'comments'

    id_comment = Column(Integer, primary_key=True, unique=True,autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"),primary_key=True)
    id_videogame = Column(Integer,ForeignKey("videoGame.id_game_api", ondelete="CASCADE"), primary_key=True)
    description = Column(String(255), nullable=False)
    date_of_comment = Column(Date, nullable=False, default=date.today)

    users_rl = relationship('User',back_populates="comments_rl", overlaps="rates_rl")
    video_game_rl = relationship("Video_game", back_populates="comments_rl")


    def to_dict(self):
        return {
            "id_comment": self.id_comment,
            "id_user": self.id_user,
            "id_videogame": self.id_videogame,
            "description": self.description,
            "date_of_comment": str(self.date_of_comment)
        }