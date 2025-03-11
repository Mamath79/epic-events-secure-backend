import sentry_sdk
from crm.utils.logger import log_error
from crm.utils.validation import (
    validate_email,
    validate_siret,
    validate_date,
    validate_numeric,
    clean_text,
    validate_mandatory_field,
    validate_date_order,
)


class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def safe_execute(self, func, *args, **kwargs):
        """Exécute une fonction en capturant les erreurs avec Sentry et log_error."""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = f"Erreur dans {func.__name__} : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return None

    def get_by_id(self, entity_id):
        """Récupère une entité par son ID."""
        return self.safe_execute(self.repository.get_by_id, entity_id)

    def get_all(self):
        """Récupère toutes les entités."""
        return self.safe_execute(self.repository.get_all)

    def create(self, data):
        """Crée une nouvelle entité après validation des données."""
        self.validate_inputs(data)
        return self.safe_execute(self.repository.create, data)

    def update(self, entity_id, new_data):
        """Met à jour une entité après validation des données."""
        entity = self.get_by_id(entity_id)
        if not entity:
            log_error(
                f"Tentative de mise à jour d'une entité inexistante (ID: {entity_id})"
            )
            return None
        self.validate_inputs(new_data)
        return self.safe_execute(self.repository.update, entity, new_data)

    def delete(self, entity_id):
        """Supprime une entité."""
        entity = self.get_by_id(entity_id)
        if not entity:
            log_error(
                f"Tentative de suppression d'une entité inexistante (ID: {entity_id})"
            )
            return None
        return self.safe_execute(self.repository.delete, entity)

    def validate_inputs(self, data):
        """Valide et nettoie les entrées utilisateur avant insertion en base."""
        for field, value in data.items():
            if value is None:
                continue  

            if isinstance(value, str):
                data[field] = clean_text(value)  # Nettoyage de la chaîne

            if field == "email" and value:
                if not validate_email(value):
                    raise ValueError(f"L'email '{value}' est invalide.")

            if field == "siret" and value:
                if not validate_siret(value):
                    raise ValueError(
                        f"Le SIRET '{value}' est invalide (14 chiffres requis)."
                    )

            if field.endswith("_date") and value:
                if not validate_date(value):
                    raise ValueError(
                        f"La date '{value}' est invalide (format attendu : YYYY-MM-DD)."
                    )

            if field in ["total_amount", "payed_amount"] and value:
                if not validate_numeric(str(value)):
                    raise ValueError(
                        f"Le montant '{value}' doit être un nombre valide."
                    )

            if field in ["first_name", "last_name", "title"] and value:
                validate_mandatory_field(value, field)

        # Vérifier la cohérence des dates uniquement si les deux existent
        if "event_startdate" in data and "event_enddate" in data:
            start_date, end_date = data["event_startdate"], data["event_enddate"]
            if start_date and end_date:  
                if not validate_date_order(start_date, end_date, allow_same=True):
                    raise ValueError(
                        "La date de début d'événement doit être antérieure ou égale à la date de fin."
                    )
