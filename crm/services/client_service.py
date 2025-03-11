import sentry_sdk
from sqlalchemy.orm import joinedload
from crm.models.clients_model import Client
from crm.repositories.client_repository import ClientRepository
from crm.services.base_service import BaseService
from crm.utils.logger import log_error


class ClientService(BaseService):
    def __init__(self, session):
        super().__init__(ClientRepository(session))

    def get_all_clients(self):
        """Récupère tous les clients avec leur entreprise et leurs contrats associés."""
        try:
            return (
                self.repository.session.query(Client)
                .options(
                    joinedload(Client.company),  # Jointure avec la table company
                    joinedload(Client.contracts),  # Jointure avec les contrats liés
                )
                .all()
            )
        except Exception as e:
            log_error(f"Erreur lors de la récupération des clients : {str(e)}")
            sentry_sdk.capture_exception(e)
            return []

    def get_by_id(self, client_id):
        """Récupère un client avec son entreprise et ses contrats associés."""
        try:
            return (
                self.repository.session.query(Client)
                .options(
                    joinedload(Client.company),
                    joinedload(Client.contracts),
                )
                .filter(Client.id == client_id)
                .first()
            )
        except Exception as e:
            log_error(f"Erreur lors de la récupération du client {client_id} : {str(e)}")
            sentry_sdk.capture_exception(e)
            return None

    def get_clients_by_company(self, company_id):
        """Récupère tous les clients d'une entreprise spécifique."""
        try:
            return (
                self.repository.session.query(Client)
                .options(joinedload(Client.contracts))  # Ajout des contrats liés
                .filter(Client.company_id == company_id)
                .all()
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la récupération des clients pour l'entreprise {company_id} : {str(e)}"
            )
            sentry_sdk.capture_exception(e)
            return []
        
    def get_all_filtered(self, filters):
        """
        Récupère les clients en appliquant des filtres dynamiques.
        """
        try:
            query = self.repository.session.query(Client).options(
                joinedload(Client.company),  # Charger la société du client
            )

            # Appliquer les filtres dynamiques
            if "first_name" in filters:
                query = query.filter(Client.first_name.ilike(f"%{filters['first_name']}%"))
            if "last_name" in filters:
                query = query.filter(Client.last_name.ilike(f"%{filters['last_name']}%"))
            if "email" in filters:
                query = query.filter(Client.email.ilike(f"%{filters['email']}%"))
            if "phone_number" in filters:
                query = query.filter(Client.phone_number.ilike(f"%{filters['phone_number']}%"))
            if "companies_id" in filters:
                query = query.filter(Client.companies_id == filters["companies_id"])

            return query.all()
        except Exception as e:
            log_error(f"Erreur lors du filtrage des clients : {str(e)}")
            sentry_sdk.capture_exception(e)
            return []
