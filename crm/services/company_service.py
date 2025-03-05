from crm.services.base_service import BaseService
from crm.repositories.company_repository import CompanyRepository

class CompanyService(BaseService):
    def __init__(self, session):
        super().__init__(CompanyRepository(session))

    def create(self, data):
        """
        Crée une entreprise après validation et nettoyage des données.
        """
        
        # Ici on applique la règle métier : ne pas stocker un SIRET vide
        data["siret"] = data["siret"] if data["siret"] else None

        return super().create(data)
