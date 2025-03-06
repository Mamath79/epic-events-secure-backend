import click
from sentry_sdk import capture_exception
from crm.services.company_service import CompanyService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.views.company_view import CompanyView
from crm.utils.logger import log_error, log_info

def company_menu():
    """
    Menu de gestion des entreprises.
    """
    while True:
        CompanyView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            get_companies_list()
        elif choice == 2:
            get_company_by_id()
        elif choice == 3:
            create_company()
        elif choice == 4:
            update_company()
        elif choice == 5:
            delete_company()
        elif choice == 0:
            break
        else:
            click.echo("[red]Option invalide, veuillez réessayer.[/red]")

@requires_auth(read_only=True)  # Tout le monde peut voir
def get_companies_list(user):
    """
    Récupère et affiche la liste des entreprises existantes.
    """
    try:
        with SessionLocal() as session:
            company_service = CompanyService(session)
            companies = company_service.get_all()

            if companies:
                CompanyView.display_companies(companies)
            else:
                click.echo("Aucune entreprise trouvée.")

    except Exception as e:
        log_error(f"Erreur lors de la récupération des entreprises : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(read_only=True)  # Tout le monde peut voir
def get_company_by_id(user):
    """
    Récupère et affiche une entreprise par son ID.
    """
    try:
        company_id = click.prompt("Entrez l'ID de l'entreprise", type=int)

        with SessionLocal() as session:
            company_service = CompanyService(session)
            company = company_service.get_by_id(company_id)

            if company:
                CompanyView.display_company(company)
            else:
                click.echo("[red]Entreprise introuvable.[/red]")

    except Exception as e:
        log_error(f"Erreur lors de la récupération de l'entreprise {company_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])  # Gestionnaires et Commerciaux peuvent créer
def create_company(user):
    """
    Demande les infos d'une nouvelle entreprise et la crée.
    """
    try:
        company_data = CompanyView.prompt_company_data()
        if not company_data:
            return None  # Annulation si aucune donnée

        with SessionLocal() as session:
            company_service = CompanyService(session)
            new_company = company_service.create(company_data)

            log_info(f"Entreprise '{new_company.title}' créée avec succès.")
            CompanyView.display_message(f"Entreprise '{new_company.title}' ajoutée avec succès !", "success")
            return new_company

    except Exception as e:
        log_error(f"Erreur lors de la création de l'entreprise : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])  # Gestionnaires et Commerciaux peuvent modifier
def update_company(user):
    """Permet de modifier une entreprise existante."""
    try:
        company_id = click.prompt("Entrez l'ID de l'entreprise à modifier", type=int)

        with SessionLocal() as session:
            company_service = CompanyService(session)
            company = company_service.get_by_id(company_id)

            if not company:
                CompanyView.display_message("Entreprise introuvable.", "error")
                return

            updated_data = CompanyView.prompt_company_update(company)
            if not updated_data:
                return

            updated_company = company_service.update(company_id, updated_data)
            log_info(f"Entreprise '{updated_company.title}' mise à jour avec succès.")
            CompanyView.display_message(f"Entreprise '{updated_company.title}' mise à jour avec succès !", "success")

    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de l'entreprise {company_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1])  # Seuls les gestionnaires peuvent supprimer
def delete_company(user):
    """Permet de supprimer une entreprise."""
    try:
        company_id = click.prompt("Entrez l'ID de l'entreprise à supprimer", type=int)

        with SessionLocal() as session:
            company_service = CompanyService(session)
            company = company_service.get_by_id(company_id)

            if not company:
                CompanyView.display_message("Entreprise introuvable.", "error")
                return

            confirm = click.confirm(f"⚠️ Voulez-vous vraiment supprimer l'entreprise '{company.title}' ?", default=False)
            if confirm:
                company_service.delete(company_id)
                log_info(f"Entreprise '{company.title}' supprimée avec succès.")
                CompanyView.display_message("Entreprise supprimée avec succès.", "success")
            else:
                CompanyView.display_message("Suppression annulée.", "info")

    except Exception as e:
        log_error(f"Erreur lors de la suppression de l'entreprise {company_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")
