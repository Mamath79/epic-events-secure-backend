from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(70), nullable=False)
    event_startdate = Column(DateTime, nullable=True)
    event_enddate = Column(DateTime, nullable=True)
    location = Column(String(70), nullable=True)
    attendees = Column(Integer, nullable=True)
    note = Column(Text, nullable=True)  
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)
    clients_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False) 
    contracts_id = Column(Integer, ForeignKey("contracts.id", ondelete="CASCADE", use_alter=True), nullable=False)

    # Relations
    client = relationship("Client", back_populates="events", passive_deletes=True) 
    contract = relationship("Contract", back_populates="event")
    users = relationship("User", secondary="users_has_events", back_populates="events", passive_deletes=True)

    def __repr__(self):
        return f"Event(id={self.id}, title='{self.title}', from {self.event_startdate} to {self.event_enddate})"
