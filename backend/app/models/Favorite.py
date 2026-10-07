from app.database.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Favorite(Base):
    __tablename__ = 'favorites'

    fav_id      = Column(Integer, primary_key=True, autoincrement=True)
    id_game_api = Column(Integer, nullable=False)
    status      = Column(String(20), nullable=True)

    add_favorites_rl = relationship("AddFavorite", back_populates="favorite_rl", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "fav_id":      self.fav_id,
            "id_game_api": self.id_game_api,
            "status":      self.status
        }
