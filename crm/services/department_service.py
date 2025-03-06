import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.department_repository import DepartmentRepository
from crm.utils.logger import log_error

class DepartmentService(BaseService):
    def __init__(self, session):
        super().__init__(DepartmentRepository(session))

    def get_department_by_id(self, department_id):
        """ Récupère un département par son ID. """
        try:
            return self.safe_execute(lambda: self.repository.get_by_id(department_id))
        except Exception as e:
            error_message = f"Erreur lors de la récupération du département {department_id} : {str(e)}"
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return None  # 🔥 Évite un crash si erreur SQL

    def get_all_departments(self):
        """ Récupère tous les départements. """
        try:
            return self.safe_execute(lambda: self.repository.get_all())
        except Exception as e:
            error_message = f"Erreur lors de la récupération des départements : {str(e)}"
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return []  # 🔥 Retourne une liste vide si erreur (évite un crash)
