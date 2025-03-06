import sentry_sdk
from crm.services.base_service import BaseService
from crm.repositories.invoice_repository import InvoiceRepository
from crm.utils.logger import log_error

class InvoiceService(BaseService):
    def __init__(self, session):
        super().__init__(InvoiceRepository(session))

    def get_invoice_by_id(self, invoice_id):
        """ Récupère une facture par son ID. """
        try:
            return self.safe_execute(lambda: self.repository.get_by_id(invoice_id))
        except Exception as e:
            error_message = f"Erreur lors de la récupération de la facture {invoice_id} : {str(e)}"
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return None  #Évite un crash si erreur SQL

    def get_all_invoices(self):
        """ Récupère toutes les factures. """
        try:
            return self.safe_execute(lambda: self.repository.get_all())
        except Exception as e:
            error_message = f"Erreur lors de la récupération des factures : {str(e)}"
            log_error(error_message)  # Log en local
            sentry_sdk.capture_exception(e)  # Envoi à Sentry
            return []  # 🔥 Retourne une liste vide si erreur (évite un crash)

    def create_invoice(self, data):
        """ Crée une facture après validation. """
        try:
            return self.safe_execute(lambda: self.repository.create(data))
        except Exception as e:
            error_message = f"Erreur lors de la création de la facture : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return None

    def update_invoice(self, invoice_id, new_data):
        """ Met à jour une facture existante. """
        try:
            invoice = self.repository.get_by_id(invoice_id)
            if not invoice:
                raise ValueError("Facture introuvable.")

            return self.safe_execute(lambda: self.repository.update(invoice, new_data))
        except Exception as e:
            error_message = f"Erreur lors de la mise à jour de la facture {invoice_id} : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
            return None

    def delete_invoice(self, invoice_id):
        """ Supprime une facture. """
        try:
            invoice = self.repository.get_by_id(invoice_id)
            if not invoice:
                raise ValueError("Facture introuvable.")

            self.safe_execute(lambda: self.repository.delete(invoice))
        except Exception as e:
            error_message = f"Erreur lors de la suppression de la facture {invoice_id} : {str(e)}"
            log_error(error_message)
            sentry_sdk.capture_exception(e)
