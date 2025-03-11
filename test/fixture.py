import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from crm.database.base import Base, engine
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

# Connexion à une base de données temporaire SQLite en mémoire
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# --- Fixtures ---
@pytest.fixture
def test_session():
    """Fixture qui crée une session de base de données pour chaque test"""
    Base.metadata.create_all(bind=engine)  # Création des tables
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)  # Suppression des tables après chaque test


@pytest.fixture
def client_repo(test_session):
    return ClientRepository(test_session)


@pytest.fixture
def contract_repo(test_session):
    return ContractRepository(test_session)


@pytest.fixture
def event_repo(test_session):
    return EventRepository(test_session)


@pytest.fixture
def user_repo(test_session):
    return UserRepository(test_session)


@pytest.fixture
def contract_status_repo(test_session):
    return ContractStatusRepository(test_session)


@pytest.fixture
def client_service(test_session):
    return ClientService(test_session)


@pytest.fixture
def contract_service(test_session):
    return ContractService(test_session)


@pytest.fixture
def event_service(test_session):
    return EventService(test_session)


@pytest.fixture
def user_service(test_session):
    return UserService(test_session)


@pytest.fixture
def contract_status_service(test_session):
    return ContractStatusService(test_session)
