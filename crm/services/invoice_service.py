from crm.services.base_service import BaseService
from crm.repositories.invoice_repository import InvoiceRepository

class InvoiceService(BaseService):
    def __init__(self, session):
        super().__init__(InvoiceRepository(session))