from crm.repositories.base_repository import BaseRepository
from crm.models.companies_model import Company

class CompanyRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Company, session)
