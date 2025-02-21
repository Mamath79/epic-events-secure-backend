from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base  

class UserHasClient(Base):
    __tablename__ = "users_has_clients"

    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    clients_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), primary_key=True)

    # Relations bidirectionnelles
    user = relationship("User", back_populates="clients")
    client = relationship("Client", back_populates="users")

    def __repr__(self):
        return f"<UserHasClient User {self.users_id} - Client {self.clients_id}>"
