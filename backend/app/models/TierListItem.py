from app.database.db import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class TierListItem(db.Model):
    __tablename__ = "tierlist_item"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_tierlist = Column(Integer, ForeignKey("tierlist.id_tierlist", ondelete="CASCADE"),
                         nullable=False)
    id_game_api = Column(Integer, ForeignKey("videoGame.id_game_api", ondelete="CASCADE"),
                         nullable=False)
    rank = Column(String(1), nullable=False)
    position = Column(Integer, nullable=False)

    tierlist_rl = relationship("TierList", back_populates="items_rl")
    video_games_rl = relationship("Video_game", back_populates="tierlist_items_rl")

    def to_dict(self):
        return {
            "id_item": self.id_item,
            "id_tierlist": self.id_tierlist,
            "id_game_api": self.id_game_api,
            "rank": self.rank,
            "position": self.position
        }
