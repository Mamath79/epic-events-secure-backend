from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(70), unique=True, nullable=False)
    phone_number = Column(String(45), nullable=True)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, default=None, onupdate=datetime.datetime.utcnow)
    delete_at = Column(DateTime, default=None, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")

    def __repr__(self):
        return f"<Client {self.first_name} {self.last_name} ({self.email})>"
