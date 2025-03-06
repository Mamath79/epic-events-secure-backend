import sentry_sdk
from crm.utils.logger import log_error

class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def safe_execute(self, func, *args, **kwargs):
        """
        Exécute une fonction en capturant les erreurs avec Sentry et log_error.
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = f"Erreur dans {func.__name__} : {str(e)}"
            log_error(error_message)  # Enregistrement dans le log local
            sentry_sdk.capture_exception(e)  # Capture dans Sentry
            return None  # Éviter une exception bloquante

    def get_by_id(self, entity_id):
        """ Récupère une entité par son ID. """
        return self.safe_execute(self.repository.get_by_id, entity_id)

    def get_all(self):
        """ Récupère toutes les entités. """
        return self.safe_execute(self.repository.get_all)

    def create(self, data):
        """ Crée une nouvelle entité. """
        return self.safe_execute(self.repository.create, data)

    def update(self, entity_id, new_data):
        """ Met à jour une entité existante. """
        entity = self.get_by_id(entity_id)
        if not entity:
            log_error(f"Tentative de mise à jour d'une entité inexistante (ID: {entity_id})")
            return None  # On ne lève pas d'erreur bloquante
        return self.safe_execute(self.repository.update, entity, new_data)

    def delete(self, entity_id):
        """ Supprime une entité. """
        entity = self.get_by_id(entity_id)
        if not entity:
            log_error(f"Tentative de suppression d'une entité inexistante (ID: {entity_id})")
            return None
        return self.safe_execute(self.repository.delete, entity)
