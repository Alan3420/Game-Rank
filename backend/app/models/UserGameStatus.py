from app.database.db import db
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint


class UserGameStatus(db.Model):
    __tablename__ = "user_game_status"
    __table_args__ = (PrimaryKeyConstraint('id_user', 'id_game_api'),)

    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    id_game_api = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "id_game_api": self.id_game_api,
            "status": self.status
        }