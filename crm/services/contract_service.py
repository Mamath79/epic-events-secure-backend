import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.contract_repository import ContractRepository
from crm.utils.logger import log_error

class ContractService(BaseService):
    def __init__(self, session):
        super().__init__(ContractRepository(session))

    def get_contracts_by_client(self, client_id):
        """ Récupère les contrats d'un client spécifique. """
        try:
            return self.safe_execute(
                lambda: self.repository.session.query(self.repository.model)
                .filter_by(clients_id=client_id)
                .all()
            )
        except Exception as e:
            error_message = f"Erreur lors de la récupération des contrats pour le client {client_id} : {str(e)}"
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return None  #Évite un crash si erreur SQL
