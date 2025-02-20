from sqlalchemy import Column, Integer, ForeignKey
from database.base import Base  

class UserHasClient(Base):
    __tablename__ = "users_has_clients"

    users_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    clients_id = Column(Integer, ForeignKey("clients.id"), primary_key=True)

    def __repr__(self):
        return f"<UserHasClient User {self.users_id} - Client {self.clients_id}>"
