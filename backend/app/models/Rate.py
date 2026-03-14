from datetime import datetime
from app.database.db import db
from sqlalchemy import Column, String, Integer, Date,ForeignKey
from sqlalchemy.orm import relationship

class Rate(db.Model):
    __tablename__ ="rates"

    id_user = Column(Integer,ForeignKey("users.id_user"), primary_key=True)
    id_game= Column(Integer,ForeignKey("videoGame.id_game"), primary_key=True)
    date_rate= Column(Date, nullable=False, default=datetime.today)
    rating = Column(Integer, nullable=False)
    status = Column(String(20), nullable=True)

    video_games_rl = relationship("Video_game", back_populates="rates_rl")
    users_rl =relationship("User", back_populates="rates_rl")

