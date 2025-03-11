import click
from sentry_sdk import capture_exception
from crm.services.company_service import CompanyService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.views.company_view import CompanyView
from crm.utils.logger import log_error, log_info


def company_menu():
    """
    Menu interactif pour la gestion des entreprises.
    """
    while True:
        CompanyView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            log_info("Consultation de toutes les entreprises")
            get_companies_list()
        elif choice == 2:
            log_info("Consultation d'une entreprise par ID")
            get_company_by_id()
        elif choice == 3:
            log_info("Création d'une entreprise")
            create_company()
        elif choice == 4:
            log_info("Mise à jour d'une entreprise")
            update_company()
        elif choice == 5:
            log_info("Suppression d'une entreprise")
            delete_company()
        elif choice == 0:
            log_info("Retour au menu principal")
            break
        else:
            log_error(f"Option invalide sélectionnée : {choice}")
            click.echo("\n[bold red]Option invalide, veuillez réessayer.[/bold red]")


@requires_auth(read_only=True)
def get_companies_list(user):
    """
    Affiche la liste des entreprises.
    """
    session = SessionLocal()
    service = CompanyService(session)
    try:
        companies = service.get_all()
        if companies:
            CompanyView.display_companies(companies)
        else:
            click.echo("\n[bold yellow]Aucune entreprise trouvée.[/bold yellow]")
    except Exception as e:
        log_error(
            f"\n[bold red]Erreur lors de la récupération des entreprises : {e} [/bold red]"
        )
        capture_exception(e)
        click.echo(
            "\n[bold red]Une erreur est survenue lors de l'affichage des entreprises.[/bold red]"
        )
    finally:
        session.close()


@requires_auth(read_only=True)
def get_company_by_id(user):
    """
    Affiche les détails d'une entreprise par ID.
    """
    company_id = click.prompt(
        "\n[bold cyan]Entrez l'ID de l'entreprise[/bold cyan]", type=int
    )

    session = SessionLocal()
    service = CompanyService(session)
    try:
        company = service.get_by_id(company_id)
        if company:
            CompanyView.display_company(company)
        else:
            click.echo("\n[bold yellow]Entreprise introuvable.[/bold yellow]")
    except Exception as e:
        log_error(
            f"\n[bold red]Erreur lors de la récupération de l'entreprise {company_id} : {e}[/bold red]"
        )
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def create_company(user):
    """
    Ajoute une nouvelle entreprise.
    """
    company_data = CompanyView.prompt_company_data()
    if not company_data:
        return  # Annulation si aucune donnée

    session = SessionLocal()
    service = CompanyService(session)
    try:
        new_company = service.create(company_data)
        log_info(
            f"[bold green]Entreprise '{new_company.title}' créée avec succès ![/bold green]"
        )
        click.echo(
            f"[bold green]Entreprise '{new_company.title}' ajoutée avec succès ![/bold green]"
        )
    except Exception as e:
        log_error(
            f"\n[bold red]Erreur lors de la création de l'entreprise : {e}[/bold red]"
        )
        capture_exception(e)
        click.echo("\n[bold red]Erreur lors de la création de l'entreprise.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def update_company(user):
    """
    Met à jour une entreprise existante avec un menu interactif.
    """
    company_id = click.prompt(
        "\n[bold cyan]Entrez l'ID de l'entreprise à modifier[/bold cyan]", type=int
    )

    session = SessionLocal()
    service = CompanyService(session)
    try:
        company = service.get_by_id(company_id)
        if not company:
            click.echo("\n[bold yellow]Entreprise introuvable.[/bold yellow]")
            return

        updated_data = CompanyView.prompt_company_update(company)
        if not updated_data:
            return

        updated_company = service.update(company_id, updated_data)
        log_info(
            f"[bold green]Entreprise '{updated_company.title}' mise à jour ![/bold green]"
        )
        click.echo(
            f"[bold green]Entreprise '{updated_company.title}' mise à jour avec succès ![/bold green]"
        )

    except Exception as e:
        log_error(
            f"\n[bold red]Erreur lors de la mise à jour de l'entreprise {company_id} : {e}[/bold red]"
        )
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1])
def delete_company(user):
    """
    Supprime une entreprise avec confirmation.
    """
    company_id = click.prompt(
        "\n[bold cyan]Entrez l'ID de l'entreprise à supprimer[/bold cyan]", type=int
    )

    session = SessionLocal()
    service = CompanyService(session)
    try:
        company = service.get_by_id(company_id)
        if not company:
            click.echo("\n[bold yellow]Entreprise introuvable.[/bold yellow]")
            return

        confirm = click.confirm(
            f"[bold yellow]Voulez-vous vraiment supprimer l'entreprise '{company.title}' ?[/bold yellow]",
            default=False,
        )
        if confirm:
            service.delete(company_id)
            log_info(
                f"[bold green]Entreprise '{company.title}' supprimée avec succès.[/bold green]"
            )
            click.echo("\n[bold green]Entreprise supprimée avec succès.[/bold green]")
        else:
            click.echo("\n[bold yellow]Suppression annulée.[/bold yellow]")
    except Exception as e:
        log_error(
            f"\n[bold red]Erreur lors de la suppression de l'entreprise {company_id} : {e}[/bold red]"
        )
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()
