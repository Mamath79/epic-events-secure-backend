from crm.services.base_service import BaseService
from crm.repositories.event_repository import EventRepository

class EventService(BaseService):
    def __init__(self, session):
        super().__init__(EventRepository(session))
    
    def check_event_dates(self, event):
        """ Vérifie que event_enddate ne peut pas être avant event_startdate. """
        if event.event_startdate and event.event_enddate:
            if event.event_enddate < event.event_startdate:
                raise ValueError("event_enddate ne peut pas être avant event_startdate.")

    def create_event(self, data):
        """ Crée un événement après validation des dates. """
        event = self.repository.create(data)
        self.check_event_dates(event)
        return event
