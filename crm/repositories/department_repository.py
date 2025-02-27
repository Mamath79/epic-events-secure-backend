from crm.repositories.base_repository import BaseRepository
from crm.models.departments_model import Department

class DepartmentRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Department, session)
