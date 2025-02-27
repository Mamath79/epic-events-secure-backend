from crm.services.base_service import BaseService
from crm.repositories.client_repository import ClientRepository

class ClientService(BaseService):
    def __init__(self, session):
        super().__init__(ClientRepository(session))
    
    def get_clients_by_company(self, company_id):
        """ Récupère tous les clients d'une entreprise spécifique. """
        return self.repository.session.query(self.repository.model).filter_by(company_id=company_id).all()
