from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=True)
    siret = Column(String(45), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    # Relation avec Client
    clients = relationship("Client", back_populates="company", cascade="all, delete")

    def __repr__(self):
        return f"Company(id={self.id}, title='{self.title}', siret='{self.siret}')"
