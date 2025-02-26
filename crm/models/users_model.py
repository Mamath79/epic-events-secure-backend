from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from crm.database.base import Base  
from argon2 import PasswordHasher


ph = PasswordHasher()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(70), nullable=True)
    first_name = Column(String(70), nullable=True)
    email = Column(String(70), nullable=False, unique=True)
    username = Column(String(70), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)
    departments_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)

    # Relations
    department = relationship("Department", back_populates="users", passive_deletes=True)
    clients = relationship("Client", secondary="users_has_clients", back_populates="users")
    events = relationship("Event", secondary="users_has_events", back_populates="users")

    # Hashage du mot de passe
    def set_password(self, password):
        self.password = ph.hash(password)

    # methode de verification du mot de passe
    def check_password(self,password):
        try:
            return ph.verify(self.password, password)
        except:
            return False

    def __repr__(self):
        return f"User(user_id={self.id}, username='{self.username}', email='{self.email}')"
