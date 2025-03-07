from sqlalchemy.orm import joinedload
import sentry_sdk
from crm.models.events_model import Event
from crm.repositories.event_repository import EventRepository
from crm.repositories.client_repository import ClientRepository
from crm.repositories.contract_repository import ContractRepository
from crm.repositories.user_repository import UserRepository
from crm.services.base_service import BaseService
from crm.utils.logger import log_error, log_info


class EventService(BaseService):
    def __init__(self, session):
        super().__init__(EventRepository(session))
        self.client_repo = ClientRepository(session)
        self.contract_repo = ContractRepository(session)
        self.user_repo = UserRepository(session)

    def validate_event_data(self, data):
        """ Vérifie la validité des données avant insertion. """
        self.validate_inputs(data)  # Validation et nettoyage des inputs
        if not self.validate_client_contract(data["clients_id"], data["contracts_id"]):
            raise ValueError("Le client ou le contrat spécifié n'existe pas.")

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
    
    def assign_support(self, event, user):
        """ Assigne ou retire un support manager d'un événement. """
        try:
            if not event:
                raise ValueError("Événement introuvable.")

            if not user:
                raise ValueError("Utilisateur introuvable.")

            if user in event.users:
                event.users.remove(user)  # Supprime si déjà assigné
            else:
                event.users.append(user)  # Ajoute sinon
            
            self.repository.session.commit()
            log_info(f"Utilisateur {user.id} assigné à l'événement {event.id}")
        
        except ValueError as e:
            log_error(f"Erreur de validation : {str(e)}")
            raise
        except Exception as e:
            log_error(f"Erreur lors de l'assignation du support (event_id={event.id}, user_id={user.id}): {str(e)}")
            self.repository.session.rollback()
            sentry_sdk.capture_exception(e)
            raise


    def create(self, data):
        """ Crée un événement après validation des données. """
        try:
            self.validate_event_data(data)
            event = super().create(data)
            self.check_event_dates(event)
            return event
        except ValueError as e:
            log_error(f"Erreur de validation lors de la création de l'événement : {str(e)}")
            raise
        except Exception as e:
            log_error(f"Erreur lors de la création de l'événement : {str(e)}")
            sentry_sdk.capture_exception(e)
            raise

    def update(self, event_id, new_data):
        """ Met à jour un événement après validation des données. """
        try:
            event = self.get_by_id(event_id)
            if not event:
                raise ValueError(f"Événement ID {event_id} introuvable.")

            # Compléter les données manquantes avec les valeurs actuelles
            new_data.setdefault("clients_id", event.clients_id)
            new_data.setdefault("contracts_id", event.contracts_id)

            self.validate_event_data(new_data)
            return super().update(event_id, new_data)

        except ValueError as e:
            log_error(f"Erreur de validation lors de la mise à jour de l'événement {event_id} : {str(e)}")
            raise
        except Exception as e:
            log_error(f"Erreur inattendue lors de la mise à jour de l'événement {event_id} : {str(e)}")
            sentry_sdk.capture_exception(e)
            raise


    def get_all_with_relations(self):
        """ Récupère tous les événements avec leurs relations client, contrat et users. """
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
        """ Assigne un support manager à un événement. """
        try:
            if user in event.users:
                event.users.remove(user)  # Supprime si déjà assigné
            else:
                event.users.append(user)  # Ajoute sinon
            self.repository.session.commit()
        except Exception as e:
            log_error(f"Erreur lors de l'assignation du support (event_id={event.id}, user_id={user.id}): {str(e)}")
            self.repository.session.rollback()
            raise

    def get_by_id_with_relations(self, event_id):
        """ Récupère un événement avec ses relations client, contrat et users. """
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
