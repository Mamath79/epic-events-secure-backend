import click
from sentry_sdk import capture_exception
from crm.services.company_service import CompanyService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.views.company_view import CompanyView
from crm.utils.logger import log_error, log_info

def company_menu():
    """ Menu de gestion des entreprises. """
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
            click.echo("Option invalide, veuillez réessayer.")

@requires_auth(read_only=True)
def get_companies_list(user):
    """ Affiche toutes les entreprises. """
    try:
        with SessionLocal() as session:
            companies = CompanyService(session).get_all()
            CompanyView.display_companies(companies) if companies else click.echo("Aucune entreprise trouvée.")
    except Exception as e:
        log_error(f"Erreur lors de la récupération des entreprises : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(read_only=True)
def get_company_by_id(user):
    """ Affiche une entreprise par son ID. """
    try:
        company_id = click.prompt("Entrez l'ID de l'entreprise", type=int)

        with SessionLocal() as session:
            company_service = CompanyService(session)
            company = company_service.get_by_id(company_id)

            if company:
                CompanyView.display_company(company)
            else:
                click.echo("Entreprise introuvable.")
    except Exception as e:
        log_error(f"Erreur lors de la récupération de l'entreprise {company_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")


@requires_auth(required_roles=[1, 3])  # Gestionnaires et Commerciaux peuvent créer
def create_company(user):
    """ Crée une nouvelle entreprise. """
    try:
        company_data = CompanyView.prompt_company_data()
        if not company_data:
            return  # Annulation si aucune donnée

        with SessionLocal() as session:
            company_service = CompanyService(session)
            new_company = company_service.create(company_data)

            if new_company:
                log_info(f"Entreprise '{new_company.title}' créée avec succès.")
                click.echo(f"Entreprise '{new_company.title}' ajoutée avec succès !")
            else:
                click.echo("Erreur lors de l'ajout de l'entreprise.")
    except Exception as e:
        log_error(f"Erreur lors de la création de l'entreprise : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")


@requires_auth(required_roles=[1, 3])
def update_company(user):
    """ Modifie une entreprise existante. """
    try:
        company_id = click.prompt("Entrez l'ID de l'entreprise à modifier", type=int)

        with SessionLocal() as session:
            company_service = CompanyService(session)
            company = company_service.get_by_id(company_id)

            if not company:
                click.echo("Entreprise introuvable.")
                return

            updated_data = CompanyView.prompt_company_update(company)
            if not updated_data:
                return

            updated_company = company_service.update(company_id, updated_data)
            log_info(f"Entreprise '{updated_company.title}' mise à jour avec succès.")
            click.echo(f"Entreprise '{updated_company.title}' mise à jour avec succès !")

    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de l'entreprise {company_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")


@requires_auth(required_roles=[1])
def delete_company(user):
    """ Supprime une entreprise. """
    try:
        company_id = click.prompt("Entrez l'ID de l'entreprise à supprimer", type=int)

        with SessionLocal() as session:
            company_service = CompanyService(session)
            company = company_service.get_by_id(company_id)

            if not company:
                click.echo("Entreprise introuvable.")
                return

            confirm = click.confirm(f"Voulez-vous vraiment supprimer l'entreprise '{company.title}' ?", default=False)
            if confirm:
                company_service.delete(company_id)
                log_info(f"Entreprise '{company.title}' supprimée avec succès.")
                click.echo("Entreprise supprimée avec succès.")
            else:
                click.echo("Suppression annulée.")

    except Exception as e:
        log_error(f"Erreur lors de la suppression de l'entreprise {company_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")
