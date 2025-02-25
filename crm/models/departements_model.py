from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from crm.database.base import Base  

class Department(Base):
    __tablename__ = "departements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    # Relation avec Users
    users = relationship("User", back_populates="department", passive_deletes=True)

    # Relation avec Permissions
    permissions = relationship("Permission", secondary="departements_has_permissions", back_populates="departments")

    def __repr__(self):
        return f"Departement(id={self.id}, title='{self.title}'"
