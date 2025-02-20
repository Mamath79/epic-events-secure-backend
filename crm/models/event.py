from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(70), nullable=False)
    event_startdate = Column(DateTime, nullable=True)
    event_enddate = Column(DateTime, nullable=True)
    location = Column(String(70), nullable=True)
    attendees = Column(Integer, nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, default=None, nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="events")

    def __repr__(self):
        return f"<Event {self.title} - Client {self.client_id}>"
