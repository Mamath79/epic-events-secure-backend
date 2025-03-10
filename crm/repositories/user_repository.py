from crm.repositories.base_repository import BaseRepository
from crm.models.users_model import User


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(User, session)
