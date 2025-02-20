from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.base import Base  # Import correct

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_amount = Column(Float, nullable=True)
    contract_satement_id = Column(Integer, ForeignKey("contract_status.id"), nullable=False)
    clients_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relations
    client = relationship("Client", back_populates="contracts")
    status = relationship("ContractStatus", back_populates="contracts")
    events = relationship("Event", back_populates="contract", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Contract {self.id} - Client {self.clients_id} - Status {self.contract_satement_id}>"
