import click
from sentry_sdk import capture_exception
from crm.views.invoice_view import InvoiceView
from crm.services.invoice_service import InvoiceService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info


def invoice_menu():
    """Menu de gestion des factures."""
    while True:
        InvoiceView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            list_all_invoices()
        elif choice == 2:
            get_invoice_by_id()
        elif choice == 3:
            create_invoice()
        elif choice == 4:
            update_invoice()
        elif choice == 5:
            delete_invoice()
        elif choice == 0:
            break
        else:
            click.echo("Option invalide, veuillez réessayer.")


@requires_auth(read_only=True)
def list_all_invoices(user):
    """Liste toutes les factures."""
    with SessionLocal() as session:
        service = InvoiceService(session)
        try:
            invoices = service.get_all()
            (
                InvoiceView.display_invoices(invoices)
                if invoices
                else click.echo("Aucune facture trouvée.")
            )
        except Exception as e:
            log_error(f"Erreur lors de la récupération des factures : {str(e)}")
            capture_exception(e)
            click.echo("Une erreur s'est produite.")


@requires_auth(read_only=True)
def get_invoice_by_id(user):
    """Récupère une facture par son ID."""
    invoice_id = click.prompt("Entrez l'ID de la facture", type=int)
    with SessionLocal() as session:
        service = InvoiceService(session)
        try:
            invoice = service.get_by_id(invoice_id)
            (
                InvoiceView.display_invoice(invoice)
                if invoice
                else click.echo("Facture introuvable.")
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la récupération de la facture {invoice_id} : {str(e)}"
            )
            capture_exception(e)
            click.echo("Une erreur s'est produite.")


@requires_auth(required_roles=[1, 3])
def create_invoice(user):
    """Création d'une nouvelle facture."""
    invoice_data = InvoiceView.prompt_invoice_data()
    with SessionLocal() as session:
        service = InvoiceService(session)
        try:
            new_invoice = service.create(invoice_data)
            log_info(f"Facture {new_invoice.id} créée avec succès.")
            InvoiceView.display_message(
                f"Facture {new_invoice.id} ajoutée avec succès !", "success"
            )
        except Exception as e:
            log_error(f"Erreur lors de la création d'une facture : {str(e)}")
            capture_exception(e)
            click.echo("Une erreur s'est produite.")


@requires_auth(required_roles=[1, 3])
def update_invoice(user):
    """Mise à jour d'une facture existante."""
    invoice_id = click.prompt("Entrez l'ID de la facture à modifier", type=int)
    with SessionLocal() as session:
        service = InvoiceService(session)
        try:
            invoice = service.get_by_id(invoice_id)
            if not invoice:
                click.echo("Facture introuvable.")
                return

            update_data = InvoiceView.prompt_invoice_update(invoice)
            updated_invoice = service.update(invoice_id, update_data)

            session.commit()
            log_info(f"Facture {updated_invoice.id} mise à jour avec succès.")
            InvoiceView.display_message(
                f"Facture {updated_invoice.id} mise à jour avec succès !", "success"
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la mise à jour de la facture {invoice_id} : {str(e)}"
            )
            capture_exception(e)
            click.echo("Une erreur s'est produite.")


@requires_auth(required_roles=[1])
def delete_invoice(user):
    """Suppression d'une facture."""
    invoice_id = click.prompt("Entrez l'ID de la facture à supprimer", type=int)
    with SessionLocal() as session:
        service = InvoiceService(session)
        try:
            invoice = service.get_by_id(invoice_id)
            if not invoice:
                InvoiceView.display_message("Facture introuvable.", "error")
                return
            confirm = click.confirm(
                f"Voulez-vous vraiment supprimer la facture {invoice.id} ?",
                default=False,
            )
            if confirm:
                service.delete(invoice_id)
                log_info(f"Facture {invoice.id} supprimée.")
                InvoiceView.display_message("Facture supprimée avec succès.", "success")
            else:
                InvoiceView.display_message("Suppression annulée.", "info")
        except Exception as e:
            log_error(
                f"Erreur lors de la suppression de la facture {invoice_id} : {str(e)}"
            )
            capture_exception(e)
            click.echo("Une erreur s'est produite.")
