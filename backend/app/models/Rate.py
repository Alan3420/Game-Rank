from datetime import datetime
from app.database.db import db
from sqlalchemy import Column, String, Integer, Date,ForeignKey
from sqlalchemy.orm import relationship

class Rate(db.Model):
    __tablename__ ="rates"

    id_rate = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer,ForeignKey("users.id_user"), primary_key=True)
    id_game_api= Column(Integer,ForeignKey("videoGame.id_game_api"), primary_key=True)
    date_rate= Column(Date, nullable=False, default=datetime.today)
    rating = Column(Integer, nullable=False)
    status = Column(String(20), nullable=True)

    video_games_rl = relationship("Video_game", back_populates="rates_rl", overlaps="users_rl,video_games_rl")
    users_rl =relationship("User", back_populates="rates_rl", overlaps="users_rl,video_games_rl,rates_rl")

def to_dict(self):
    return {
        "id_rate": self.id_rate,
        "id_user": self.id_user,
        "id_game_api": self.id_game_api,
        "date_rate": str(self.date_rate),
        "rating": self.rating,
        "status": self.status
    }