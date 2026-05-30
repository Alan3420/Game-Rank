from app.database.db import db
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class AddFavorite(db.Model):
    __tablename__ = 'add_favorite'

    fav_id   = Column(Integer, ForeignKey('favorites.fav_id', ondelete='CASCADE'), primary_key=True)
    id_user  = Column(Integer, ForeignKey('users.id_user',   ondelete='CASCADE'), primary_key=True)
    date_added = Column(Date, nullable=False, default=datetime.now)

    favorite_rl = relationship("Favorite", back_populates="add_favorites_rl")
    users_rl    = relationship("User",     back_populates="add_favorites_rl")
