from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, default=None, nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("contract_status.id"), nullable=False)

    client = relationship("Client", back_populates="contracts")
    status = relationship("ContractStatus")

    def __repr__(self):
        return f"<Contract {self.id} - Client {self.client_id}>"
