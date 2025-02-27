from crm.services.base_service import BaseService
from crm.repositories.user_repository import UserRepository

class UserService(BaseService):
    def __init__(self, session):
        super().__init__(UserRepository(session))

    def get_users_by_department(self, department_id):
        """ Récupère tous les utilisateurs d'un département donné. """
        return self.repository.session.query(self.repository.model).filter_by(departments_id=department_id).all()
