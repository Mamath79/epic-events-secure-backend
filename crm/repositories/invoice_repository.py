from crm.repositories.base_repository import BaseRepository
from crm.models.invoices_model import Invoice

class InvoiceRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Invoice, session)
