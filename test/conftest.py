import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crm.database.base import Base
from crm.models import User, Client, Contract, Event, ContractStatus
from datetime import datetime, timedelta

# Connexion à une base de données temporaire pour les tests (ex: SQLite en mémoire)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def test_session():
    """Fixture qui crée une session de base de données pour chaque test"""
    Base.metadata.create_all(bind=engine)  # Création des tables
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)  # Suppression des tables après chaque test

@pytest.fixture
def new_user(test_session):
    user = User(
        last_name="Doe",
        first_name="John",
        email="john.doe@email.com",
        username="johndoe",
        password="securepassword",
        departments_id=1
    )
    test_session.add(user)
    test_session.commit()
    return user

@pytest.fixture
def new_client(test_session):
    client = Client(
        last_name="Smith",
        first_name="Alice",
        phone_number='+331234567654',
        email="alice.smith@email.com"
    )
    test_session.add(client)
    test_session.commit()
    return client

@pytest.fixture
def new_contract(test_session, new_client):
    contract_status = ContractStatus(status="Signé")
    test_session.add(contract_status)
    test_session.commit()

    contract = Contract(
        clients_id=new_client.id,
        contract_status_id=contract_status.id,
        total_amount=5000,
    )
    test_session.add(contract)
    test_session.commit()
    return contract

@pytest.fixture
def new_event(test_session, new_client, new_contract):
    event = Event(
        title='Test Event',
        clients_id=new_client.id,
        attendees=500,
        contracts_id=new_contract.id,
        location='12 grande rue Versailles 78100',
        note='Texte de la note',
        event_startdate=datetime.now(),
        event_enddate=datetime.now() + timedelta(days=3)
    )
    test_session.add(event)
    test_session.commit()
    return event