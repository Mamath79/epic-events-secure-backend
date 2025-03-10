from sqlalchemy import Column, Integer, ForeignKey
from crm.database.base import Base


class UserHasEvent(Base):
    __tablename__ = "users_has_events"

    users_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    events_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )

    def __repr__(self):
        return f"UserHasEvent(User_id={self.users_id}, Event_id={self.events_id})"
