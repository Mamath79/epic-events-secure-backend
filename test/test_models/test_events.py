import pytest
from crm.models.events_model import Event
from datetime import datetime, timedelta


def test_create_event(new_event):
    assert new_event.id is not None
    assert new_event.event_startdate < new_event.event_enddate


def test_update_event(test_session, new_event):
    new_event.event_enddate += timedelta(days=1)
    test_session.commit()
    assert new_event.event_enddate > new_event.event_startdate


def test_delete_event(test_session, new_event):
    test_session.delete(new_event)
    test_session.commit()
    assert test_session.query(Event).filter_by(id=new_event.id).first() is None
