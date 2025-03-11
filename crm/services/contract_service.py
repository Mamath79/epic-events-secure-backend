import sentry_sdk
from sqlalchemy.orm import joinedload
from crm.services.base_service import BaseService
from crm.models.contracts_model import Contract
from crm.repositories.contract_repository import ContractRepository
from crm.utils.logger import log_error


class ContractService(BaseService):
    def __init__(self, session):
        super().__init__(ContractRepository(session))

    def get_all(self):
        """Récupère tous les contrats avec les informations du client et des événements associés."""
        try:
            return (
                self.repository.session.query(Contract)
                .options(
                    joinedload(Contract.client),  # Jointure avec Client
                    joinedload(Contract.event),  # Jointure avec les Événements liés
                    joinedload(Contract.sales_contact),  # Jointure avec le commercial
                )
                .all()
            )
        except Exception as e:
            log_error(f"Erreur lors de la récupération des contrats : {str(e)}")
            sentry_sdk.capture_exception(e)
            return []

    def get_by_id(self, contract_id):
        """Récupère un contrat avec son client et ses événements."""
        try:
            return (
                self.repository.session.query(Contract)
                .options(
                    joinedload(Contract.client),
                    joinedload(Contract.event),
                    joinedload(Contract.sales_contact),
                )
                .filter(Contract.id == contract_id)
                .first()
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la récupération du contrat {contract_id} : {str(e)}"
            )
            sentry_sdk.capture_exception(e)
            return None

    def get_contracts_by_client(self, client_id):
        """Récupère les contrats d'un client spécifique avec ses événements."""
        try:
            return (
                self.repository.session.query(Contract)
                .options(joinedload(Contract.events))
                .filter_by(clients_id=client_id)
                .all()
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la récupération des contrats pour le client {client_id} : {str(e)}"
            )
            sentry_sdk.capture_exception(e)
            return []

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

    def get_all_filtered(self, filters):
        """
        Récupère les contrats en appliquant des filtres dynamiques.
        """
        try:
            query = self.repository.session.query(Contract).options(
                joinedload(Contract.client),  # Charger le client lié
                joinedload(Contract.sales_contact),  # Charger le commercial lié
                joinedload(Contract.status),  # Charger le statut du contrat
            )

            if "contract_status_id" in filters:
                query = query.filter(
                    Contract.contract_status_id == filters["contract_status_id"]
                )
            if "clients_id" in filters:
                query = query.filter(Contract.clients_id == filters["clients_id"])
            if "sales_contact_id" in filters:
                query = query.filter(
                    Contract.sales_contact_id == filters["sales_contact_id"]
                )
            if "total_amount_min" in filters:
                query = query.filter(
                    Contract.total_amount >= filters["total_amount_min"]
                )
            if "total_amount_max" in filters:
                query = query.filter(
                    Contract.total_amount <= filters["total_amount_max"]
                )
            if "payed_amount_min" in filters:
                query = query.filter(
                    Contract.payed_amount >= filters["payed_amount_min"]
                )
            if "payed_amount_max" in filters:
                query = query.filter(
                    Contract.payed_amount <= filters["payed_amount_max"]
                )

            return query.all()
        except Exception as e:
            log_error(f"Erreur lors du filtrage des contrats : {str(e)}")
            sentry_sdk.capture_exception(e)
            return []
