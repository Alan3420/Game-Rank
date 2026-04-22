from app.database.db import db
from sqlalchemy import Column, Integer, Date,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Favorite(db.Model):
    __tablename__ = 'favorites'

    fav_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id_user'), primary_key=True, nullable=False)
    id_game_api = Column(Integer, ForeignKey('videoGame.id_game_api'), primary_key=True, nullable=False)
    date_added = Column(Date, nullable=False, default=datetime.now)

    users_rl = relationship("User", foreign_keys="[Favorite.user_id]",back_populates="favorites_rl")
    video_games_rl = relationship("Video_game", foreign_keys="[Favorite.id_game_api]",back_populates="favorites_rl")


    def to_dict(self):
        return {
            "fav_id": self.fav_id,
            "user_id": self.user_id,
            "id_game_api": self.id_game_api,
            "date_added": str(self.date_added)
        }