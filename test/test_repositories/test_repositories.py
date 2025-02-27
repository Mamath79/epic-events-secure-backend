import pytest
from sqlalchemy.exc import IntegrityError
from crm.repositories.client_repository import ClientRepository
from crm.repositories.contract_repository import ContractRepository
from crm.repositories.event_repository import EventRepository
from crm.repositories.user_repository import UserRepository
from crm.repositories.contract_status_repository import ContractStatusRepository
from crm.services.client_service import ClientService
from crm.services.contract_service import ContractService
from crm.services.event_service import EventService
from crm.services.user_service import UserService
from crm.services.contract_status_service import ContractStatusService
from crm.database.base import SessionLocal
from crm.models import Client, Contract, Event, User, ContractStatus, Department

# --- Fixtures ---
@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def client_repo(db_session):
    return ClientRepository(db_session)

@pytest.fixture
def contract_repo(db_session):
    return ContractRepository(db_session)

@pytest.fixture
def event_repo(db_session):
    return EventRepository(db_session)

@pytest.fixture
def user_repo(db_session):
    return UserRepository(db_session)

@pytest.fixture
def contract_status_repo(db_session):
    return ContractStatusRepository(db_session)

@pytest.fixture
def client_service(db_session):
    return ClientService(db_session)

@pytest.fixture
def contract_service(db_session):
    return ContractService(db_session)

@pytest.fixture
def event_service(db_session):
    return EventService(db_session)

@pytest.fixture
def user_service(db_session):
    return UserService(db_session)

@pytest.fixture
def contract_status_service(db_session):
    return ContractStatusService(db_session)

# --- Tests Repositories ---
def test_client_repository_create(client_repo):
    client = Client(first_name="John", last_name="Doe", email="johndoe@email.com")
    client_repo.create(client)
    assert client.id is not None

def test_contract_repository_create(contract_repo, db_session):
    client = Client(first_name="John", last_name="Doe", email="johndoe@email.com")
    db_session.add(client)
    db_session.commit()

    status = db_session.query(ContractStatus).filter_by(status="pending").first()
    if not status:
        status = ContractStatus(status="pending")
        db_session.add(status)
        db_session.commit()

    contract = Contract(clients_id=client.id, total_amount=1000, status=status)
    contract_repo.create(contract)
    assert contract.id is not None

def test_event_repository_create(event_repo, db_session):
    client = Client(first_name="John", last_name="Doe", email="johndoe@email.com")
    db_session.add(client)
    db_session.commit()
    event = Event(title="Event Test", clients_id=client.id)
    event_repo.create(event)
    assert event.id is not None

def test_user_repository_create(user_repo, db_session):
    department = db_session.query(Department).filter_by(id=1).first()
    if not department:
        department = Department(id=1, title="Support")
        db_session.add(department)
        db_session.commit()

    # Vérifier si l'utilisateur existe déjà et le supprimer
    existing_user = db_session.query(User).filter_by(email="testuser@gmail.com").first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    user = User(username="testuser", email="testuser@gmail.com", password="hashedpassword", departments_id=department.id)
    user_repo.create(user)
    assert user.id is not None


def test_contract_status_repository_create(contract_status_repo):
    status = ContractStatus(status="Approved")
    contract_status_repo.create(status)
    assert status.id is not None

# --- Tests Services ---
def test_client_service_create(client_service):
    client = client_service.create({"first_name": "Alice", "last_name": "Smith", "email": "alice@email.com"})
    assert client.id is not None

def test_contract_service_create(contract_service, db_session):
    client = Client(first_name="Alice", last_name="Smith", email="alice@email.com")
    db_session.add(client)
    db_session.commit()

    status = db_session.query(ContractStatus).filter_by(status="pending").first()
    if not status:
        status = ContractStatus(status="pending")
        db_session.add(status)
        db_session.commit()

    contract_data = {
        "clients_id": client.id,
        "total_amount": 1000,
        "contract_status_id": status.id  # Assure-toi que la clé correspond à celle attendue dans ton modèle
    }
    
    contract = contract_service.create(contract_data)
    assert contract.id is not None

    assert contract.id is not None

def test_event_service_create(event_service, db_session):
    client = Client(first_name="Alice", last_name="Smith", email="alice@email.com")
    db_session.add(client)
    db_session.commit()
    event = event_service.create({"title": "Conference", "clients_id": client.id})
    assert event.id is not None

def test_user_service_create(user_service, db_session):
    department = db_session.query(Department).filter_by(id=1).first()
    if not department:
        department = Department(id=1, title="Support")
        db_session.add(department)
        db_session.commit()

    user_data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "hashedpassword",
        "departments_id": department.id
    }

    # Vérifier si l'utilisateur existe déjà et le supprimer
    existing_user = db_session.query(User).filter_by(email="testuser@gmail.com").first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    user = user_service.create(user_data)
    assert user.id is not None


def test_contract_status_service_create(contract_status_service):
    status = contract_status_service.create({"status": "Pending"})
    assert status.id is not None
