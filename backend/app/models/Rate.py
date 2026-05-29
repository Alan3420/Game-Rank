from datetime import datetime
from app.database.db import db
from sqlalchemy import Column, Integer, Date, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

class Rate(db.Model):
    __tablename__ = "rates"
    __table_args__ = (PrimaryKeyConstraint('id_user', 'id_game_api'),)

    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    id_game_api = Column(Integer, nullable=False)
    date_rate = Column(Date, nullable=False, default=datetime.today)
    rating = Column(Integer, nullable=False)

    users_rl = relationship("User", back_populates="rates_rl")

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "id_game_api": self.id_game_api,
            "date_rate": str(self.date_rate),
            "rating": self.rating
        }