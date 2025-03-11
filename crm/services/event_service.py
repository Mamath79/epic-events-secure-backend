from sqlalchemy.orm import joinedload
from sqlalchemy import and_
import sentry_sdk
from crm.models.events_model import Event
from crm.models.users_model import User
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
        """
        Vérifie la validité des données avant insertion.
        """
        self.validate_inputs(data)
        if not self.validate_client_contract(data["clients_id"], data["contracts_id"]):
            raise ValueError("Le client ou le contrat spécifié n'existe pas.")

    def validate_client_contract(self, clients_id, contracts_id):
        """
        Vérifie que le client et le contrat existent.
        """
        client = self.client_repo.get_by_id(clients_id)
        contract = self.contract_repo.get_by_id(contracts_id)
        return client is not None and contract is not None

    def assign_support(self, event, user):
        """
        Assigne ou retire un support manager d'un événement.
        """
        try:
            if not event:
                raise ValueError("Événement introuvable.")

            if not user:
                raise ValueError("Utilisateur introuvable.")

            if user in event.users:
                event.users.remove(user)
            else:
                event.users.append(user)

            self.repository.session.commit()
            log_info(f"Utilisateur {user.id} assigné à l'événement {event.id}")

        except ValueError as e:
            log_error(f"Erreur de validation : {str(e)}")
            raise
        except Exception as e:
            log_error(
                f"Erreur lors de l'assignation du support (event_id={event.id}, user_id={user.id}): {str(e)}"
            )
            self.repository.session.rollback()
            sentry_sdk.capture_exception(e)
            raise

    def create(self, data, support_id=None):
        """Crée un événement après validation des données et assigne un support si nécessaire."""
        try:
            self.validate_event_data(data)  # Valide les données
            event = super().create(data)  # Crée l'événement

            if support_id:  # Ajouter le support manager si un ID est fourni
                support_user = self.user_repo.get_by_id(support_id)
                if support_user:
                    event.users.append(support_user)
                    self.repository.session.commit()

            return event
        except ValueError as e:
            log_error(
                f"Erreur de validation lors de la création de l'événement : {str(e)}"
            )
            raise
        except Exception as e:
            log_error(f"Erreur lors de la création de l'événement : {str(e)}")
            sentry_sdk.capture_exception(e)
            raise

    def update(self, event_id, new_data):
        """
        Met à jour un événement et gère l'affectation des supports.
        """
        try:
            event = self.get_by_id(event_id)
            if not event:
                raise ValueError(f"L'événement {event_id} n'existe pas.")

            support_id = new_data.pop("support_id", None)  # Récupère l'ID du support

            # Mise à jour des autres champs
            for key, value in new_data.items():
                setattr(event, key, value)

            # Gère l'affectation du support avec assign_support()
            if support_id is not None:
                support_user = self.user_repo.get_by_id(support_id)
                self.assign_support(event, support_user)

            self.repository.session.commit()  # Sauvegarde des modifications

            return event
        except Exception as e:
            log_error(
                f"Erreur lors de la mise à jour de l'événement {event_id} : {str(e)}"
            )
            sentry_sdk.capture_exception(e)
            raise

    def get_all(self):
        """
        Récupère tous les événements avec leurs relations client, contrat et users.
        """
        try:
            return (
                self.repository.session.query(Event)
                .options(
                    joinedload(Event.client),  # Associe le client lié à l'événement
                    joinedload(Event.contract),  # Associe le contrat lié à l'événement
                    joinedload(
                        Event.users
                    ),  # Charge les utilisateurs (supports) assignés
                )
                .all()
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la récupération des événements avec relations : {str(e)}"
            )
            sentry_sdk.capture_exception(e)
            raise

    def get_by_id_with_relations(self, event_id):
        """
        Récupère un événement avec ses relations client, contrat et users.
        """
        try:
            return (
                self.repository.session.query(Event)
                .options(
                    joinedload(Event.client),
                    joinedload(Event.contract),
                    joinedload(Event.users),
                )
                .filter(Event.id == event_id)
                .first()
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la récupération de l'événement ID {event_id} avec relations : {str(e)}"
            )
            raise

    def get_all_filtered(self, filters):
        """
        Récupère les événements en appliquant des filtres dynamiques.
        """
        try:
            query = self.repository.session.query(Event).options(
                joinedload(Event.client),
                joinedload(Event.contract),
                joinedload(Event.users),
            )

            if "event_startdate" in filters:
                query = query.filter(
                    Event.event_startdate >= filters["event_startdate"]
                )
            if "event_enddate" in filters:
                query = query.filter(Event.event_enddate <= filters["event_enddate"])
            if "clients_id" in filters:
                query = query.filter(Event.clients_id == filters["clients_id"])
            if "contracts_id" in filters:
                query = query.filter(Event.contracts_id == filters["contracts_id"])
            if "support_id" in filters:
                query = query.join(Event.users).filter(User.id == filters["support_id"])

            return query.all()
        except Exception as e:
            log_error(f"Erreur lors du filtrage des événements : {str(e)}")
            sentry_sdk.capture_exception(e)
            return []
