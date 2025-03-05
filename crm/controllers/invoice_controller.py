from crm.views.invoice_view import InvoiceView
from crm.utils.auth import requires_auth


def invoice_menu():
    InvoiceView.show_menu()