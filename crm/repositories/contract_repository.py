from crm.repositories.base_repository import BaseRepository
from crm.models.contracts_model import Contract

class ContractRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Contract, session)
