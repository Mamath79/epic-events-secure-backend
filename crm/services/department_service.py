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
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return None  # Évite un crash si erreur SQL

    def get_all_departments(self):
        """ Récupère tous les départements. """
        try:
            return self.safe_execute(lambda: self.repository.get_all())
        except Exception as e:
            error_message = f"Erreur lors de la récupération des départements : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return []  # Retourne une liste vide si erreur (évite un crash)

    def create(self, data):
        """ Crée un département après validation des données. """
        try:
            self.validate_inputs(data)  # Validation et nettoyage des entrées
            return self.safe_execute(lambda: self.repository.create(data))
        except ValueError as e:
            log_error(f"Erreur de validation lors de la création du département : {str(e)}")
            raise
        except Exception as e:
            error_message = f"Erreur lors de la création du département : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return None

    def update(self, department_id, new_data):
        """ Met à jour un département existant. """
        try:
            department = self.repository.get_by_id(department_id)
            if not department:
                raise ValueError("Département introuvable.")

            self.validate_inputs(new_data)  # Vérification des nouvelles valeurs
            return self.safe_execute(lambda: self.repository.update(department, new_data))
        except ValueError as e:
            log_error(f"Erreur de validation lors de la mise à jour du département {department_id} : {str(e)}")
            raise
        except Exception as e:
            error_message = f"Erreur lors de la mise à jour du département {department_id} : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return None

    def delete(self, department_id):
        """ Supprime un département. """
        try:
            department = self.repository.get_by_id(department_id)
            if not department:
                raise ValueError("Département introuvable.")

            self.safe_execute(lambda: self.repository.delete(department))
        except ValueError as e:
            log_error(f"Erreur de validation : {str(e)}")
            raise
        except Exception as e:
            error_message = f"Erreur lors de la suppression du département {department_id} : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
