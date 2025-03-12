from test.fixture import test_session, client_repo, contract_repo, event_repo, user_repo, contract_status_repo
from crm.models import Client, Contract, Event, User, ContractStatus, Department


# --- Tests Repositories ---
def test_client_repository_create(client_repo):
    client = Client(first_name="John", last_name="Doe", email="johndoe@email.com")
    client_repo.create(client)
    assert client.id is not None


def test_contract_repository_create(contract_repo, test_session):
    client = Client(first_name="John", last_name="Doe", email="johndoe@email.com")
    test_session.add(client)
    test_session.commit()

    status = test_session.query(ContractStatus).filter_by(status="pending").first()
    if not status:
        status = ContractStatus(status="pending")
        test_session.add(status)
        test_session.commit()

    contract = Contract(clients_id=client.id, total_amount=1000, status=status)
    contract_repo.create(contract)
    assert contract.id is not None


def test_event_repository_create(event_repo, test_session):
    client = Client(first_name="John", last_name="Doe", email="johndoe@email.com")
    test_session.add(client)
    test_session.commit()

    # Vérification et création d'un statut de contrat valide
    contract_status = (
        test_session.query(ContractStatus).filter_by(status="Signé").first()
    )
    if not contract_status:
        contract_status = ContractStatus(status="Signé")
        test_session.add(contract_status)
        test_session.commit()

    # Création et enregistrement du contrat avec un statut valide
    contract = Contract(
        clients_id=client.id, total_amount=1000, contract_status_id=contract_status.id
    )
    test_session.add(contract)
    test_session.commit()

    # --- Correction ici : Ajout de contracts_id pour éviter l'erreur d'intégrité ---
    event = Event(title="Event Test", clients_id=client.id, contracts_id=contract.id)
    event_repo.create(event)

    assert event.id is not None  # Vérification que l'event est bien créé


def test_user_repository_create(user_repo, test_session):
    department = test_session.query(Department).filter_by(id=1).first()
    if not department:
        department = Department(id=1, title="Support")
        test_session.add(department)
        test_session.commit()

    # Vérifier si l'utilisateur existe déjà et le supprimer
    existing_user = (
        test_session.query(User).filter_by(email="testuser@gmail.com").first()
    )
    if existing_user:
        test_session.delete(existing_user)
        test_session.commit()

    user = User(
        username="testuser",
        email="testuser@gmail.com",
        password="hashedpassword",
        departments_id=department.id,
    )
    user_repo.create(user)
    assert user.id is not None


def test_contract_status_repository_create(contract_status_repo):
    status = ContractStatus(status="Approved")
    contract_status_repo.create(status)
    assert status.id is not None
