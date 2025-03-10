from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base


class ContractStatus(Base):
    __tablename__ = "contract_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(45), nullable=False)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
    deleted_at = Column(DateTime, nullable=True)

    # Relation avec Contracts
    contracts = relationship(
        "Contract", back_populates="status", cascade="all, delete", passive_deletes=True
    )

    def __repr__(self):
        return f"ContractStatus(id={self.id}, status='{self.status}')"
