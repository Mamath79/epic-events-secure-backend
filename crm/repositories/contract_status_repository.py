from crm.repositories.base_repository import BaseRepository
from crm.models.contract_status_model import ContractStatus


class ContractStatusRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(ContractStatus, session)
