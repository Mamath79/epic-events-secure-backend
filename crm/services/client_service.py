import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.client_repository import ClientRepository
from crm.utils.logger import log_error

class ClientService(BaseService):
    def __init__(self, session):
        super().__init__(ClientRepository(session))

    def get_clients_by_company(self, company_id):
        """ Récupère tous les clients d'une entreprise spécifique. """
        try:
            return self.safe_execute(
                lambda: self.repository.session.query(self.repository.model).filter_by(company_id=company_id).all()
            )
        except Exception as e:
            log_error(f"Erreur lors de la récupération des clients pour l'entreprise {company_id} : {str(e)}")
            sentry_sdk.capture_exception(e)
            return None
