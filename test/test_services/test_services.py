from test.fixture import client_service, contract_service, event_service, user_service, contract_status_service, test_session
from crm.models import Client, Contract, Event, User, ContractStatus, Department


def test_client_service_create(client_service):
    client = client_service.create(
        {"first_name": "Alice", "last_name": "Smith", "email": "alice@email.com"}
    )
    assert client.id is not None


def test_contract_service_create(contract_service, test_session):
    client = Client(first_name="Alice", last_name="Smith", email="alice@email.com")
    test_session.add(client)
    test_session.commit()

    status = test_session.query(ContractStatus).filter_by(status="pending").first()
    if not status:
        status = ContractStatus(status="pending")
        test_session.add(status)
        test_session.commit()

    contract_data = {
        "clients_id": client.id,
        "total_amount": 1000,
        "contract_status_id": status.id,  # Assure-toi que la clé correspond à celle attendue dans ton modèle
    }

    contract = contract_service.create(contract_data)
    assert contract.id is not None


def test_event_service_create(event_service, test_session):
    client = Client(first_name="Alice", last_name="Smith", email="alice@email.com")
    test_session.add(client)
    test_session.commit()

    contract_status = (
        test_session.query(ContractStatus).filter_by(status="Signé").first()
    )
    if not contract_status:
        contract_status = ContractStatus(status="Signé")  # Ajout d'un statut valide
        test_session.add(contract_status)
        test_session.commit()

    contract = Contract(
        clients_id=client.id,
        total_amount=5000,
        contract_status_id=contract_status.id,  # Associer un statut valide
    )
    test_session.add(contract)
    test_session.commit()

    event_data = {
        "title": "Conference",
        "clients_id": client.id,
        "contracts_id": contract.id,  # Correction ici, il manquait cette clé
    }

    event = event_service.create(event_data)
    assert event.id is not None


def test_user_service_create(user_service, test_session):
    department = test_session.query(Department).filter_by(id=1).first()
    if not department:
        department = Department(id=1, title="Support")
        test_session.add(department)
        test_session.commit()

    user_data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "hashedpassword",
        "departments_id": department.id,
    }

    # Vérifier si l'utilisateur existe déjà et le supprimer
    existing_user = (
        test_session.query(User).filter_by(email="testuser@gmail.com").first()
    )
    if existing_user:
        test_session.delete(existing_user)
        test_session.commit()

    user = user_service.create(user_data)
    assert user.id is not None


def test_contract_status_service_create(contract_status_service):
    status = contract_status_service.create({"status": "Pending"})
    assert status.id is not None
