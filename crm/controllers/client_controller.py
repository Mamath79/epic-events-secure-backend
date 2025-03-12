import click
from sentry_sdk import capture_exception
from crm.views.client_view import ClientView
from crm.services.client_service import ClientService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info
from crm.controllers.company_controller import company_menu


def client_menu():
    """Menu de gestion des clients."""
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
            click.secho("Option invalide, veuillez réessayer.", fg="red", bold=True)


@requires_auth(read_only=True)
def list_all_clients(user):
    """Liste tous les clients."""
    try:
        with SessionLocal() as session:
            service = ClientService(session)
            clients = service.get_all()
            if clients:
                ClientView.display_clients(clients)
            else:
                click.secho("Aucun client trouvé.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la récupération des clients : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(read_only=True)
def get_client_by_id(user):
    """Récupère un client par son ID."""
    try:
        client_id = click.prompt("Entrez l'ID du client", type=int)
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            if client:
                ClientView.display_client(client)
            else:
                click.secho("Client introuvable.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la récupération du client {client_id} : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(required_roles=[1, 3])
def create_client(user):
    """Création d'un nouveau client."""
    try:
        data = ClientView.prompt_client_data()
        with SessionLocal() as session:
            service = ClientService(session)
            new_client = service.create(data)
            log_info(f"Client {new_client.first_name} {new_client.last_name} créé avec succès.")
            click.secho(f"Client {new_client.first_name} {new_client.last_name} ajouté avec succès !", fg="green", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la création du client : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(required_roles=[1, 3])
def update_client(user):
    """Mise à jour d'un client existant."""
    try:
        client_id = click.prompt("Entrez l'ID du client à modifier", type=int)
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            if not client:
                click.secho("Client introuvable.", fg="yellow", bold=True)
                return
            new_data = ClientView.prompt_client_update(client)
            updated_client = service.update(client_id, new_data)
            log_info(f"Client {updated_client.first_name} {updated_client.last_name} mis à jour.")
            click.secho(f"Client {updated_client.first_name} {updated_client.last_name} mis à jour !", fg="green", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour du client {client_id} : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(required_roles=[1])
def delete_client(user):
    """Suppression d'un client."""
    try:
        client_id = click.prompt("Entrez l'ID du client à supprimer", type=int)
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            if not client:
                click.secho("Client introuvable.", fg="yellow", bold=True)
                return
            if click.confirm(f"Voulez-vous vraiment supprimer {client.first_name} {client.last_name} ?", default=False):
                service.delete(client_id)
                log_info(f"Client {client.first_name} {client.last_name} supprimé.")
                click.secho("Client supprimé avec succès.", fg="green", bold=True)
            else:
                click.secho("Suppression annulée.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la suppression du client {client_id} : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(read_only=True)
def filter_clients(user):
    """Filtre les clients selon des critères définis par l'utilisateur."""
    try:
        with SessionLocal() as session:
            service = ClientService(session)
            filters = ClientView.prompt_client_filters()
            filtered_clients = service.get_all_filtered(filters)

            if filtered_clients:
                ClientView.display_clients(filtered_clients)
            else:
                click.secho("Aucun client ne correspond aux critères sélectionnés.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors du filtrage des clients : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)
