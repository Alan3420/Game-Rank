from app.database.db import db
from sqlalchemy import Column, Integer, String, ForeignKey


class UserGameStatus(db.Model):
    __tablename__ = "user_game_status"

    id_status = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    id_game_api = Column(Integer, ForeignKey("videoGame.id_game_api", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            "id_status": self.id_status,
            "id_user": self.id_user,
            "id_game_api": self.id_game_api,
            "status": self.status
        }