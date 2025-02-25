from sqlalchemy import Column, Integer, ForeignKey
from crm.database.base import Base  

class DepartmentHasPermission(Base):
    __tablename__ = "departements_has_permissions"

    departements_id = Column(Integer, ForeignKey("departements.id", ondelete="CASCADE"), primary_key=True)
    permissions_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"DepartmentHasPermission(Department_id={self.departements_id}, Permission_id={self.permissions_id})"
