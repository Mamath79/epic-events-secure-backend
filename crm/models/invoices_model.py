from sqlalchemy import Column, Integer, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base  

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(DECIMAL(7, 2), nullable=True)
    contracts_id = Column(Integer, ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    contract = relationship("Contract", back_populates="invoices", passive_deletes=True)

    def __repr__(self):
        return f"Invoice(id={self.id}, contract_id={self.contracts_id}, Amount: {self.amount})"
