from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base
from crm.models.companies_model import Company


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(45), nullable=True)
    last_name = Column(String(45), nullable=True)
    email = Column(String(70), nullable=False, unique=True)
    phone_number = Column(String(45), nullable=True)
    creation_date = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_date = Column(
        DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
    deleted_at = Column(DateTime, nullable=True)
    companies_id = Column(
        Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=True
    )

    # Relations
    company = relationship("Company", back_populates="clients", passive_deletes=True)
    contracts = relationship("Contract", back_populates="client", cascade="all, delete")
    events = relationship(
        "Event", back_populates="client", cascade="all, delete-orphan"
    )
    users = relationship(
        "User", secondary="users_has_clients", back_populates="clients"
    )

    def __repr__(self):
        return f"Client(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})"
