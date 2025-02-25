from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base  

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    # Relation avec Department
    departments = relationship("Department",
                               secondary="departements_has_permissions",
                               back_populates="permissions",
                               passive_deletes=True)

    def __repr__(self):
        return f"Permission(id={self.id}, title='{self.title}')"
