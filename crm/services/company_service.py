import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.company_repository import CompanyRepository
from crm.utils.logger import log_error


class CompanyService(BaseService):
    def __init__(self, session):
        super().__init__(CompanyRepository(session))
