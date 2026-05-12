from datetime import datetime
from app.database.db import db
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship


class TierList(db.Model):
    __tablename__ = "tierlist"

    id_tierlist = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"),
                     nullable=False)
    title = Column(String(255), nullable=False)
    date_creation = Column(Date, nullable=False, default=datetime.today)
    date_modified = Column(Date, nullable=True)

    users_rl = relationship("User", back_populates="tierlists_rl")
    items_rl = relationship("TierListItem", back_populates="tierlist_rl",
                            cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_tierlist": self.id_tierlist,
            "id_user": self.id_user,
            "title": self.title,
            "date_creation": str(self.date_creation) if self.date_creation else None,
            "date_modified": str(self.date_modified) if self.date_modified else None
        }
