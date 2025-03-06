import click
from sentry_sdk import capture_exception
from crm.views.event_view import EventView
from crm.services.event_service import EventService
from crm.services.user_service import UserService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info

def event_menu():
    """
    Menu de gestion des événements.
    """
    while True:
        EventView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            list_all_events()
        elif choice == 2:
            get_event_by_id()
        elif choice == 3:
            create_event()
        elif choice == 4:
            update_event()
        elif choice == 5:
            delete_event()
        elif choice == 0:
            break
        else:
            click.echo("[red]Option invalide, veuillez réessayer.[/red]")

@requires_auth(read_only=True)  # Tout le monde peut voir
def list_all_events(user):
    """Liste tous les événements."""
    try:
        with SessionLocal() as session:
            service = EventService(session)
            events = service.get_all()

            if events:
                EventView.display_events(events)
            else:
                click.echo("Aucun événement trouvé.")

    except Exception as e:
        log_error(f"Erreur lors de la récupération des événements : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(read_only=True)  # Tout le monde peut voir
def get_event_by_id(user):
    """Récupère un événement par son ID."""
    try:
        event_id = click.prompt("Entrez l'ID de l'événement", type=int)

        with SessionLocal() as session:
            service = EventService(session)
            event = service.get_by_id(event_id)

            if event:
                EventView.display_event(event)
            else:
                click.echo("[red]Événement introuvable.[/red]")

    except Exception as e:
        log_error(f"Erreur lors de la récupération de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])  # Gestionnaires et Commerciaux peuvent créer
def create_event(user):
    """Création d'un nouvel événement avec support manager optionnel."""
    try:
        with SessionLocal() as session:
            event_service = EventService(session)
            user_service = UserService(session)

            # Récupération des données depuis la Vue
            event_data = EventView.prompt_event_data()

            # Vérification de l'existence du client et du contrat
            if not event_service.validate_client_contract(event_data["clients_id"], event_data["contracts_id"]):
                EventView.display_message("Erreur : Client ou Contrat invalide.", "error")
                return

            # Création de l'événement
            new_event = event_service.create(event_data)

            # Assignation d'un support manager si fourni
            if event_data.get("support_id"):
                support_user = user_service.get_by_id(event_data["support_id"])
                if support_user:
                    event_service.assign_support(new_event, support_user)
                    session.commit()  # Commit après toutes les modifications
                    EventView.display_message(f"Support Manager {support_user.username} assigné à l'événement !", "success")
                else:
                    EventView.display_message(f"Erreur : Aucun utilisateur trouvé avec l'ID {event_data['support_id']}", "error")

            log_info(f"Événement {new_event.id} créé avec succès.")
            EventView.display_message(f"Événement {new_event.id} ajouté avec succès !", "success")

    except Exception as e:
        log_error(f"Erreur lors de la création d'un événement : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 2, 3])  # Gestionnaires, Commerciaux et Support peuvent modifier
def update_event(user):
    """Mise à jour d'un événement existant, y compris l'ajout/suppression du support manager."""
    try:
        event_id = click.prompt("Entrez l'ID de l'événement à modifier", type=int)

        with SessionLocal() as session:
            event_service = EventService(session)
            user_service = UserService(session)
            event = event_service.get_by_id(event_id)

            if not event:
                click.echo("Événement introuvable.")
                return

            update_data = EventView.prompt_event_update(event)

            # Gestion du support manager
            if "support_id" in update_data:
                support_id = update_data.pop("support_id")
                if support_id:
                    support_user = user_service.get_by_id(support_id)
                    if support_user:
                        event_service.assign_support(event, support_user)
                        EventView.display_message(f"Support Manager {support_user.username} mis à jour !", "success")
                    else:
                        EventView.display_message(f"Erreur : Aucun utilisateur trouvé avec l'ID {support_id}", "error")

            # Appliquer les autres modifications
            updated_event = event_service.update(event_id, update_data)
            session.commit()
            log_info(f"Événement {updated_event.id} mis à jour avec succès.")
            EventView.display_message(f"Événement {updated_event.id} mis à jour avec succès !", "success")

    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])  # Gestionnaires et Commerciaux peuvent supprimer
def delete_event(user):
    """Suppression d'un événement."""
    try:
        event_id = click.prompt("Entrez l'ID de l'événement à supprimer", type=int)

        with SessionLocal() as session:
            service = EventService(session)
            event = service.get_by_id(event_id)

            if not event:
                EventView.display_message("Événement introuvable.", "error")
                return

            confirm = click.confirm(f"⚠️ Voulez-vous vraiment supprimer l'événement {event.id} ?", default=False)
            if confirm:
                service.delete(event_id)
                log_info(f"Événement {event.id} supprimé avec succès.")
                EventView.display_message("Événement supprimé avec succès.", "success")
            else:
                EventView.display_message("Suppression annulée.", "info")

    except Exception as e:
        log_error(f"Erreur lors de la suppression de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")
