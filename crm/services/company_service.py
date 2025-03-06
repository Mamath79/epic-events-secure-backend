import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.company_repository import CompanyRepository
from crm.utils.logger import log_error

class CompanyService(BaseService):
    def __init__(self, session):
        super().__init__(CompanyRepository(session))

    def create(self, data):
        """
        Crée une entreprise après validation et nettoyage des données.
        Empêche l'ajout d'un SIRET vide.
        """
        try:
            if "siret" in data and not data["siret"]:
                data["siret"] = None  # Évite d'enregistrer un SIRET vide

            return self.safe_execute(lambda: super().create(data))

        except Exception as e:
            error_message = f"Erreur lors de la création d'une entreprise : {str(e)}"
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return None  #Évite un crash en cas d'erreur
