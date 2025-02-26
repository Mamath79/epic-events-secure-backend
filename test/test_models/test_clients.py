import pytest
from sqlalchemy.exc import IntegrityError
from crm.models.clients_model import Client

def test_create_client(new_client):
    assert new_client.id is not None
    assert new_client.email == "alice.smith@email.com"

def test_update_client(test_session, new_client):
    new_client.last_name = "Updated"
    test_session.commit()
    assert new_client.last_name == "Updated"

def test_delete_client(test_session, new_client):
    test_session.delete(new_client)
    test_session.commit()
    assert test_session.query(Client).filter_by(id=new_client.id).first() is None

def test_unique_client_email(test_session):
    client1 = Client(email="client@email.com")
    test_session.add(client1)
    test_session.commit()

    client2 = Client(email="client@email.com")
    test_session.add(client2)

    with pytest.raises(IntegrityError):
        test_session.commit()
