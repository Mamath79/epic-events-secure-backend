from crm.services.base_service import BaseService
from crm.repositories.company_repository import CompanyRepository

class CompanyService(BaseService):
    def __init__(self, session):
        super().__init__(CompanyRepository(session))
