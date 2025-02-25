from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(70), nullable=True)
    first_name = Column(String(70), nullable=True)
    email = Column(String(70), nullable=False, unique=True)
    username = Column(String(70), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)
    departements_id = Column(Integer, ForeignKey("departements.id", ondelete="CASCADE"), nullable=False)

    # Relations
    department = relationship("Department", back_populates="users", passive_deletes=True)
    clients = relationship("Client", secondary="users_has_clients", back_populates="users")
    events = relationship("Event", secondary="users_has_events", back_populates="users")

    def __repr__(self):
        return f"User(user_id={self.id}, username='{self.username}', email='{self.email}')"
