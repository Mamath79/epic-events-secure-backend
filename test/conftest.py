# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from crm.database.base import Base  # Import de la base SQLAlchemy
# from crm.models.clients_model import Client
# from crm.models.contracts_model import Contract
# from crm.models.contract_status_model import ContractStatus
# from crm.models.events_model import Event
# from crm.models.users_has_clients_model import UserHasClient

# # Création d'un moteur SQLite en mémoire pour les tests
# TEST_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(TEST_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def db_session():
#     """Fixture qui crée une base temporaire pour chaque test"""
#     Base.metadata.create_all(bind=engine)  # Création des tables
#     session = TestingSessionLocal()
#     yield session  # Donne accès à la session
#     session.close()
#     Base.metadata.drop_all(bind=engine)  # Supprime la base après chaque test
