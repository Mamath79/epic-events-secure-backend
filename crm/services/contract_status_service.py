import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.contract_status_repository import ContractStatusRepository
from crm.utils.logger import log_error


class ContractStatusService(BaseService):
    def __init__(self, session):
        super().__init__(ContractStatusRepository(session))

    def get_status_by_id(self, status_id):
        """
        Récupère un statut de contrat par son ID.
        """
        try:
            return self.safe_execute(lambda: self.repository.get_by_id(status_id))
        except Exception as e:
            error_message = f"Erreur lors de la récupération du statut de contrat {status_id} : {str(e)}"
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return None  # 🔥 Évite un crash si erreur SQL

    def get_all_statuses(self):
        """
        Récupère tous les statuts de contrat.
        """
        try:
            return self.safe_execute(lambda: self.repository.get_all())
        except Exception as e:
            error_message = (
                f"Erreur lors de la récupération des statuts de contrat : {str(e)}"
            )
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return []  # 🔥 Retourne une liste vide si erreur (évite un crash)
