import click
from sentry_sdk import capture_exception
from crm.views.client_view import ClientView
from crm.services.client_service import ClientService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info
from crm.controllers.company_controller import company_menu


def client_menu():
    """
    Menu de gestion des clients.
    """
    while True:
        ClientView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            log_info("Consultation de tous les clients")
            list_all_clients()
        elif choice == 2:
            log_info("Consultation d'un client par ID")
            get_client_by_id()
        elif choice == 3:
            log_info("Création d'un client")
            create_client()
        elif choice == 4:
            log_info("Mise à jour d'un client")
            update_client()
        elif choice == 5:
            log_info("Suppression d'un client")
            delete_client()
        elif choice == 6:
            log_info("Gestion Client Company")
            company_menu()
        elif choice == 7:
            log_info("Filtrage des clients")
            filter_clients()
        elif choice == 0:
            break
        else:
            click.echo("\n[bold red]Option invalide, veuillez réessayer.[/bold red]")


@requires_auth(read_only=True)
def list_all_clients(user):
    """
    Liste tous les clients.
    """
    try:
        with SessionLocal() as session:
            service = ClientService(session)
            clients = service.get_all()
            (
                ClientView.display_clients(clients)
                if clients
                else click.echo("[bold yellow]Aucun client trouvé.[/bold yellow]")
            )
    except Exception as e:
        log_error(
            f"[bold red]Erreur lors de la récupération des clients : {str(e)}[/bold red]"
        )
        capture_exception(e)
        click.echo(
            "[bold red]Une erreur s'est produite. Veuillez réessayer.[/bold red]"
        )


@requires_auth(read_only=True)
def get_client_by_id(user):
    """
    Récupère un client par son ID.
    """
    try:
        client_id = click.prompt(
            "[bold cyan]Entrez l'ID du client[/bold cyan]", type=int
        )
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            (
                ClientView.display_client(client)
                if client
                else click.echo("[bold yellow]Client introuvable.[/bold yellow]")
            )
    except Exception as e:
        log_error(
            f"[bold red]Erreur lors de la récupération du client {client_id} : {str(e)}[/bold red]"
        )
        capture_exception(e)
        click.echo(
            "[bold red]Une erreur s'est produite. Veuillez réessayer.[/bold red]"
        )


@requires_auth(required_roles=[1, 3])
def create_client(user):
    """
    Création d'un nouveau client.
    """
    try:
        data = ClientView.prompt_client_data()
        with SessionLocal() as session:
            service = ClientService(session)
            new_client = service.create(data)
            log_info(
                f"[bold green]Client {new_client.first_name} {new_client.last_name} créé avec succès.[/bold green]"
            )
            click.echo(
                f"[bold green]Client {new_client.first_name} {new_client.last_name} ajouté avec succès ![/bold green]"
            )
    except Exception as e:
        log_error(
            f"[bold red]Erreur lors de la création du client : {str(e)}[/bold red]"
        )
        capture_exception(e)
        click.echo(
            "[bold red]Une erreur s'est produite. Veuillez réessayer.[/bold red]"
        )


@requires_auth(required_roles=[1, 3])
def update_client(user):
    """
    Mise à jour d'un client existant.
    """
    try:
        client_id = click.prompt("Entrez l'ID du client à modifier", type=int)
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            if not client:
                click.echo("[bold yelow]Client introuvable.[/bold yellow]")
                return
            new_data = ClientView.prompt_client_update(client)
            updated_client = service.update(client_id, new_data)
            log_info(
                f"[bold green]Client {updated_client.first_name} {updated_client.last_name} mis à jour.[/bold green]"
            )
            click.echo(
                f"[bold green]Client {updated_client.first_name} {updated_client.last_name} mis à jour ![/bold green]"
            )
    except Exception as e:
        log_error(
            f"[bold red]Erreur lors de la mise à jour du client {client_id} : {str(e)}[/bold red]"
        )
        capture_exception(e)
        click.echo(
            "[bold red]Une erreur s'est produite. Veuillez réessayer.[/bold red]"
        )


@requires_auth(required_roles=[1])
def delete_client(user):
    """
    Suppression d'un client.
    """
    try:
        client_id = click.prompt(
            "\n[bold cyan]Entrez l'ID du client à supprimer[/bod cyan]", type=int
        )
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            if not client:
                click.echo("[bold yellow]Client introuvable.[/bold yellow]")
                return
            if click.confirm(
                f"[bold yellow]Voulez-vous vraiment supprimer {client.first_name} {client.last_name} ?[/bold yellow]",
                default=False,
            ):
                service.delete(client_id)
                log_info(
                    f"[bold green]Client {client.first_name} {client.last_name} supprimé.[/bold green]"
                )
                click.echo("[bold green]Client supprimé avec succès.[/bold green]")
            else:
                click.echo("[bold yellow]Suppression annulée.[/bold yellow]")
    except Exception as e:
        log_error(
            f"[bold red]Erreur lors de la suppression du client {client_id} : {str(e)}[/bold red]"
        )
        capture_exception(e)
        click.echo(
            "[bold red]Une erreur s'est produite. Veuillez réessayer.[/bold red]"
        )


@requires_auth(read_only=True)
def filter_clients(user):
    """
    Filtre les clients selon des critères définis par l'utilisateur.
    """
    try:
        with SessionLocal() as session:
            service = ClientService(session)
            filters = ClientView.prompt_client_filters()
            filtered_clients = service.get_all_filtered(filters)

            if filtered_clients:
                ClientView.display_clients(filtered_clients)
            else:
                click.echo(
                    "[bold yellow]Aucun client ne correspond aux critères sélectionnés.[/bold yellow]"
                )

    except Exception as e:
        log_error(f"Erreur lors du filtrage des clients : {str(e)}")
        capture_exception(e)
        click.echo(
            "[bold red]Une erreur s'est produite. Veuillez réessayer.[/bold red]"
        )
