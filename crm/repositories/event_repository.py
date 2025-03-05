from crm.repositories.base_repository import BaseRepository
from crm.models.events_model import Event
from sqlalchemy.orm import joinedload

class EventRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Event, session)

    def get_all(self):
        """Récupère tous les événements avec leurs utilisateurs associés."""
        return self.session.query(Event).options(joinedload(Event.users)).all()

    def get_by_id(self, event_id):
        """Récupère un événement par ID avec ses utilisateurs associés."""
        return self.session.query(Event).options(joinedload(Event.users)).filter_by(id=event_id).first()
