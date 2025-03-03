import click
from crm.views.client_view import ClientView
from crm.services.client_service import ClientService
from crm.database.base import SessionLocal

def client_menu():
    """
    Menu de gestion des clients.
    """
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
        elif choice == 0:
            break
        else:
            click.echo("Option invalide, veuillez réessayer.")

def list_all_clients():
    """Liste tous les clients."""
    session = SessionLocal()
    service = ClientService(session)
    clients = service.get_all()
    session.close()

    if clients:
        ClientView.display_clients(clients)
    else:
        click.echo("Aucun client trouvé.")

def get_client_by_id():
    """Récupère un client par son ID."""
    client_id = click.prompt("Entrez l'ID du client", type=int)
    
    session = SessionLocal()
    service = ClientService(session)
    client = service.get_by_id(client_id)
    session.close()

    if client:
        ClientView.display_client(client)
    else:
        click.echo("Client introuvable.")

def create_client():
    """Création d'un nouveau client."""
    data = ClientView.prompt_client_data()

    session = SessionLocal()
    service = ClientService(session)
    try:
        new_client = service.create(data)
        session.close()
        click.echo(f"Client {new_client.first_name} {new_client.last_name} ajouté avec succès !")
    except Exception as e:
        click.echo(f"Erreur lors de la création du client : {e}")

def update_client():
    """Mise à jour d'un client existant."""
    client_id = click.prompt("Entrez l'ID du client à modifier", type=int)
    
    session = SessionLocal()
    service = ClientService(session)
    client = service.get_by_id(client_id)

    if not client:
        session.close()
        click.echo("Client introuvable.")
        return

    new_data = ClientView.prompt_client_update(client)
    try:
        updated_client = service.update(client_id, new_data)
        session.close()
        click.echo(f"Client {updated_client.first_name} {updated_client.last_name} mis à jour !")
    except Exception as e:
        click.echo(f"Erreur lors de la mise à jour : {e}")

def delete_client():
    """Suppression d'un client."""
    client_id = click.prompt("Entrez l'ID du client à supprimer", type=int)

    session = SessionLocal()
    service = ClientService(session)
    client = service.get_by_id(client_id)

    if not client:
        session.close()
        click.echo("Client introuvable.")
        return

    confirm = click.confirm(f"Voulez-vous vraiment supprimer {client.first_name} {client.last_name} ?", default=False)
    if confirm:
        service.delete(client_id)
        session.close()
        click.echo("Client supprimé avec succès.")
    else:
        session.close()
        click.echo("Suppression annulée.")
