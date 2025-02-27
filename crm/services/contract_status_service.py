from crm.services.base_service import BaseService
from crm.repositories.contract_status_repository import ContractStatusRepository

class ContractStatusService(BaseService):
    def __init__(self, session):
        super().__init__(ContractStatusRepository(session))


