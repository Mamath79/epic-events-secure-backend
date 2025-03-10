import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.contract_repository import ContractRepository
from crm.utils.logger import log_error


class ContractService(BaseService):
    def __init__(self, session):
        super().__init__(ContractRepository(session))

    def get_contracts_by_client(self, client_id):
        """Récupère les contrats d'un client spécifique."""
        try:
            return self.safe_execute(
                lambda: self.repository.session.query(self.repository.model)
                .filter_by(clients_id=client_id)
                .all()
            )
        except Exception as e:
            error_message = f"Erreur lors de la récupération des contrats pour le client {client_id} : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return None

    def create(self, data):
        """Création d'un contrat après validation."""
        try:
            self.validate_inputs(data)  # Validation automatique avec BaseService
            return super().create(data)
        except ValueError as e:
            log_error(f"Validation échouée lors de la création du contrat : {str(e)}")
            raise e

    def update(self, contract_id, new_data):
        """Mise à jour d'un contrat après validation."""
        try:
            self.validate_inputs(new_data)  # Validation automatique avec BaseService
            return super().update(contract_id, new_data)
        except ValueError as e:
            log_error(
                f"Validation échouée lors de la mise à jour du contrat {contract_id} : {str(e)}"
            )
            raise e
