from crm.services.base_service import BaseService
from crm.repositories.contract_repository import ContractRepository

class ContractService(BaseService):
    def __init__(self, session):
        super().__init__(ContractRepository(session))
    
    def get_contracts_by_client(self, client_id):
        """ Récupère les contrats d'un client spécifique. """
        return self.repository.session.query(self.repository.model).filter_by(clients_id=client_id).all()
