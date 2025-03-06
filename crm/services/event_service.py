from sqlalchemy.orm import joinedload
from crm.models.events_model import Event
from crm.repositories.event_repository import EventRepository
from crm.repositories.client_repository import ClientRepository
from crm.repositories.contract_repository import ContractRepository
from crm.repositories.user_repository import UserRepository
from crm.services.base_service import BaseService
from crm.utils.logger import log_error

class EventService(BaseService):
    def __init__(self, session):
        super().__init__(EventRepository(session))
        self.client_repo = ClientRepository(session)
        self.contract_repo = ContractRepository(session)
        self.user_repo = UserRepository(session)

    def check_event_dates(self, event):
        """ Vérifie que la date de fin ne peut pas être avant la date de début. """
        try:
            if event.event_startdate and event.event_enddate:
                if event.event_enddate < event.event_startdate:
                    raise ValueError("La date de fin ne peut pas être avant la date de début.")
        except Exception as e:
            log_error(f"Erreur dans check_event_dates : {str(e)}")
            raise

    def validate_client_contract(self, clients_id, contracts_id):
        """ Vérifie que le client et le contrat existent. """
        try:
            client = self.client_repo.get_by_id(clients_id)
            contract = self.contract_repo.get_by_id(contracts_id)
            return client is not None and contract is not None
        except Exception as e:
            log_error(f"Erreur lors de la validation du client/contrat (client_id={clients_id}, contract_id={contracts_id}): {str(e)}")
            raise

    def create_event(self, data):
        """ Crée un événement après validation des dates et des relations. """
        try:
            if not self.validate_client_contract(data["clients_id"], data["contracts_id"]):
                raise ValueError("Le client ou le contrat spécifié n'existe pas.")

            event = self.repository.create(data)
            self.check_event_dates(event)
            return event
        except Exception as e:
            log_error(f"Erreur lors de la création de l'événement : {str(e)}")
            raise

    def get_all_with_relations(self):
        """Récupère tous les événements avec leurs relations client, contrat et users."""
        try:
            return (
                self.repository.session.query(Event)
                .options(joinedload(Event.client), joinedload(Event.contract), joinedload(Event.users))
                .all()
            )
        except Exception as e:
            log_error(f"Erreur lors de la récupération des événements avec relations : {str(e)}")
            raise

    def assign_support(self, event, user):
        """
        Ajoute ou enlève un support manager (user) à un événement.
        Si l'utilisateur est déjà assigné, il sera retiré.
        """
        try:
            if user in event.users:
                event.users.remove(user)  # Supprimer le support s'il est déjà assigné
            else:
                event.users.append(user)  # Ajouter le support

            self.repository.session.commit()
        except Exception as e:
            log_error(f"Erreur lors de l'assignation du support (event_id={event.id}, user_id={user.id}): {str(e)}")
            self.repository.session.rollback()
            raise

    def get_by_id_with_relations(self, event_id):
        """Récupère un événement avec ses relations client, contrat et users."""
        try:
            return (
                self.repository.session.query(Event)
                .options(joinedload(Event.client), joinedload(Event.contract), joinedload(Event.users))
                .filter(Event.id == event_id)
                .first()
            )
        except Exception as e:
            log_error(f"Erreur lors de la récupération de l'événement ID {event_id} avec relations : {str(e)}")
            raise
