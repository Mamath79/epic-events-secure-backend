import click
from sentry_sdk import capture_exception
from crm.views.client_view import ClientView
from crm.services.client_service import ClientService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info
from crm.controllers.company_controller import company_menu

def client_menu():
    """ Menu de gestion des clients. """
    while True:
        ClientView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            list_all_clients()
        elif choice == 2:
            get_client_by_id()
        elif choice == 3:
            create_client()
        elif choice == 4:
            update_client()
        elif choice == 5:
            delete_client()
        elif choice == 6:
            company_menu()
        elif choice == 0:
            break
        else:
            click.echo("Option invalide, veuillez réessayer.")

@requires_auth(read_only=True)
def list_all_clients(user):
    """ Liste tous les clients. """
    try:
        with SessionLocal() as session:
            service = ClientService(session)
            clients = service.get_all()
            ClientView.display_clients(clients) if clients else click.echo("Aucun client trouvé.")
    except Exception as e:
        log_error(f"Erreur lors de la récupération des clients : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(read_only=True)
def get_client_by_id(user):
    """ Récupère un client par son ID. """
    try:
        client_id = click.prompt("Entrez l'ID du client", type=int)
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            ClientView.display_client(client) if client else click.echo("Client introuvable.")
    except Exception as e:
        log_error(f"Erreur lors de la récupération du client {client_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])
def create_client(user):
    """ Création d'un nouveau client. """
    try:
        data = ClientView.prompt_client_data()
        with SessionLocal() as session:
            service = ClientService(session)
            new_client = service.create(data)
            log_info(f"Client {new_client.first_name} {new_client.last_name} créé avec succès.")
            click.echo(f"Client {new_client.first_name} {new_client.last_name} ajouté avec succès !")
    except Exception as e:
        log_error(f"Erreur lors de la création du client : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])
def update_client(user):
    """ Mise à jour d'un client existant. """
    try:
        client_id = click.prompt("Entrez l'ID du client à modifier", type=int)
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            if not client:
                click.echo("Client introuvable.")
                return
            new_data = ClientView.prompt_client_update(client)
            updated_client = service.update(client_id, new_data)
            log_info(f"Client {updated_client.first_name} {updated_client.last_name} mis à jour.")
            click.echo(f"Client {updated_client.first_name} {updated_client.last_name} mis à jour !")
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour du client {client_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1])
def delete_client(user):
    """ Suppression d'un client. """
    try:
        client_id = click.prompt("Entrez l'ID du client à supprimer", type=int)
        with SessionLocal() as session:
            service = ClientService(session)
            client = service.get_by_id(client_id)
            if not client:
                click.echo("Client introuvable.")
                return
            if click.confirm(f"Voulez-vous vraiment supprimer {client.first_name} {client.last_name} ?", default=False):
                service.delete(client_id)
                log_info(f"Client {client.first_name} {client.last_name} supprimé.")
                click.echo("Client supprimé avec succès.")
            else:
                click.echo("Suppression annulée.")
    except Exception as e:
        log_error(f"Erreur lors de la suppression du client {client_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")
