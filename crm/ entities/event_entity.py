from datetime import datetime

class Event:
    def __init__(self, id: int, title: str, event_startdate: datetime, event_enddate: datetime, location: str, attendees: int, note: str, created_at: datetime, updated_at: datetime = None, deleted_at: datetime = None, clients_id: int = None):
        self.id = id
        self.title = title
        self.event_startdate = event_startdate
        self.event_enddate = event_enddate
        self.location = location
        self.attendees = attendees
        self.note = note
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.clients_id = clients_id  # Lien avec un client

    def __repr__(self):
        return f"<Event {self.title} - Client {self.clients_id}>"
