from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.base import Base

class ContractStatus(Base):
    __tablename__ = "contract_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(45), nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relation avec Contracts
    contracts = relationship("Contract", back_populates="status")

    def __repr__(self):
        return f"<ContractStatus {self.id} - {self.status}>"
