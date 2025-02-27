from crm.services.base_service import BaseService
from crm.repositories.department_repository import DepartmentRepository

class DepartmentService(BaseService):
    def __init__(self, session):
        super().__init__(DepartmentRepository(session))