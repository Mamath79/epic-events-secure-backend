# from crm.models.clients_model import Client
# from crm.models.contracts_model import Contract
# from crm.models.contract_status_model import ContractStatus
# from crm.models.events_model import Event
# from crm.models.companies_model import Company

# def test_create_client():
#     """Test de création d'un client"""
#     client = Client(first_name="John", last_name="Doe", email="john.doe@example.com")
#     assert client.first_name == "John"
#     assert client.last_name == "Doe"
#     assert client.email == "john.doe@example.com"

# def test_create_contract():
#     """Test de création d'un contrat"""
#     contract = Contract(total_amount=1000.50, clients_id=1, contract_satement_id=1)
#     assert contract.total_amount == 1000.50
#     assert contract.clients_id == 1
#     assert contract.contract_satement_id == 1
