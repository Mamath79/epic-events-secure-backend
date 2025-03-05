from sqlalchemy.orm import joinedload
from crm.models.events_model import Event
from crm.models.users_model import User
from crm.repositories.event_repository import EventRepository
from crm.repositories.client_repository import ClientRepository
from crm.repositories.contract_repository import ContractRepository
from crm.repositories.user_repository import UserRepository
from crm.services.base_service import BaseService

class EventService(BaseService):
    def __init__(self, session):
        super().__init__(EventRepository(session))
        self.client_repo = ClientRepository(session)
        self.contract_repo = ContractRepository(session)
        self.user_repo = UserRepository(session)

    def check_event_dates(self, event):
        """ Vérifie que la date de fin ne peut pas être avant la date de début. """
        if event.event_startdate and event.event_enddate:
            if event.event_enddate < event.event_startdate:
                raise ValueError("La date de fin ne peut pas être avant la date de début.")

    def validate_client_contract(self, clients_id, contracts_id):
        """ Vérifie que le client et le contrat existent. """
        client = self.client_repo.get_by_id(clients_id)
        contract = self.contract_repo.get_by_id(contracts_id)
        return client is not None and contract is not None

    def create_event(self, data):
        """ Crée un événement après validation des dates et des relations. """
        if not self.validate_client_contract(data["clients_id"], data["contracts_id"]):
            raise ValueError("Le client ou le contrat spécifié n'existe pas.")

        event = self.repository.create(data)
        self.check_event_dates(event)
        return event

    def get_all_with_relations(self):
        """Récupère tous les événements avec leurs relations client, contrat et users."""
        return (
            self.repository.session.query(Event)
            .options(joinedload(Event.client), joinedload(Event.contract), joinedload(Event.users))
            .all()
        )

    def assign_support(self, event, user):
        """
        Ajoute ou enlève un support manager (user) à un événement.
        Si l'utilisateur est déjà assigné, il sera retiré.
        """
        if user in event.users:
            event.users.remove(user)  # Supprimer le support s'il est déjà assigné
        else:
            event.users.append(user)  # Ajouter le support

        self.repository.session.commit()

    def get_by_id_with_relations(self, event_id):
        """Récupère un événement avec ses relations client, contrat et users."""
        return (
            self.repository.session.query(Event)
            .options(joinedload(Event.client), joinedload(Event.contract), joinedload(Event.users))
            .filter(Event.id == event_id)
            .first()
        )
