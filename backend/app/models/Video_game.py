from app.database.db import db
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class Video_game(db.Model):
    __tablename__ = "videoGame"

    id_game_api = Column(Integer, primary_key=True)

    rates_rl = relationship("Rate", back_populates="video_games_rl", overlaps="video_games_rl")
    users_rl = relationship("User", secondary="rates", back_populates="video_games_rl", overlaps="rates_rl,video_games_rl")
    comments_rl = relationship("Comment", back_populates="video_game_rl")
    favorites_rl = relationship("Favorite", foreign_keys="[Favorite.id_game_api]", back_populates="video_games_rl")

    def __init__(self, id_game_api, name=None, date_release=None,
                 platforms=None, development_company=None, **kwargs):
        super().__init__(id_game_api=id_game_api, **kwargs)
        self.name = name
        self.date_release = date_release
        self.platforms = platforms
        self.development_company = development_company

    def to_dict(self):
        return {
            "id_game_api": self.id_game_api,
            "name": getattr(self, "name", None),
            "date_release": str(self.date_release) if getattr(self, "date_release", None) else None,
            "platforms": getattr(self, "platforms", None),
            "development_company": getattr(self, "development_company", None)
        }