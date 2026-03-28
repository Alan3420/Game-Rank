from app.database.db import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Video_game(db.Model):
    __tablename__="videoGame"

    id_game_api = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_release = Column(Date, nullable=False)
    platforms = Column(String(200), nullable=True)
    development_company =Column(String(100), nullable=False)
    id_comment = Column(Integer, ForeignKey("comments.id_comment"), nullable=True)
    

    rates_rl = relationship("Rate", back_populates="video_games_rl")
    users_rl = relationship("User", secondary="rates", back_populates="video_games_rl")
    comments_rl =relationship("Comment", foreign_keys="[Video_game.id_comment]",back_populates="video_game_rl")
    favorites_rl = relationship("Favorite", foreign_keys="[Favorite.id_game_api]",back_populates="video_games_rl")