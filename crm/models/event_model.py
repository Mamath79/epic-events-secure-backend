from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.base import Base  # Import correct

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(70), nullable=False)
    event_startdate = Column(DateTime, nullable=True)
    event_enddate = Column(DateTime, nullable=True)
    location = Column(String(70), nullable=True)
    attendees = Column(Integer, nullable=True)
    note = Column(Text, nullable=True)  # Optionnel: Text(1000) si nécessaire
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    clients_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)  # ✅ Ajout de ondelete="CASCADE"

    # Relation avec Client
    client = relationship("Client", back_populates="events", cascade="all, delete")  # ✅ Ajout de la cascade si nécessaire

    def __repr__(self):
        return f"<Event {self.id} - {self.title} ({self.event_startdate} to {self.event_enddate})>"
