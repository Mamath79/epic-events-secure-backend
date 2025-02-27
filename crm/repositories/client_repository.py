from crm.repositories.base_repository import BaseRepository
from crm.models.clients_model import Client

class ClientRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Client, session)
