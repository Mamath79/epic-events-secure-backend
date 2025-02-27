from crm.repositories.base_repository import BaseRepository
from crm.models.events_model import Event

class EventRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Event, session)
