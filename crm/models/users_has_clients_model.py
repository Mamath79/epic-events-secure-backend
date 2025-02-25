from sqlalchemy import Column, Integer, ForeignKey
from crm.database.base import Base  

class UserHasClient(Base):
    __tablename__ = "users_has_clients"

    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    clients_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"UserHasClient(User_id={self.users_id}, Client_id={self.clients_id})"
