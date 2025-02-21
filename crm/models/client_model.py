from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=True)
    last_name = Column(String(45), nullable=True)
    email = Column(String(70), nullable=False, unique=True)
    phone_number = Column(String(45), nullable=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_date = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    companies_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)

    # Relation avec Company
    company = relationship("Company", back_populates="clients", passive_deletes=True)

    # Relation avec Contracts
    contracts = relationship("Contract", back_populates="client", cascade="all, delete")


    def __repr__(self):
        return f"<Client {self.first_name} {self.last_name} ({self.email})>"
