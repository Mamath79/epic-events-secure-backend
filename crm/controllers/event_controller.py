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

@requires_auth(required_roles=[1, 3])
def create_event(user):
    """ Création d'un nouvel événement avec support manager optionnel. """
    try:
        with SessionLocal() as session:
            event_service = EventService(session)
            event_data = EventView.prompt_event_data()
            new_event = event_service.create(event_data)

            log_info(f"Événement {new_event.id} créé avec succès.")
            click.echo(f"Événement {new_event.id} ajouté avec succès !")

    except ValueError as e:
        click.echo(f"Erreur de validation : {str(e)}")
    except Exception as e:
        log_error(f"Erreur lors de la création de l'événement : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")


@requires_auth(required_roles=[1, 2, 3])
def update_event(user):
    """ Mise à jour d'un événement existant. """
    try:
        event_id = click.prompt("Entrez l'ID de l'événement à modifier", type=int)

        with SessionLocal() as session:
            event_service = EventService(session)
            event = event_service.get_by_id(event_id)

            if not event:
                click.echo("Événement introuvable.")
                return

            update_data = EventView.prompt_event_update(event)
            updated_event = event_service.update(event_id, update_data)

            log_info(f"Événement {updated_event.id} mis à jour avec succès.")
            click.echo(f"Événement {updated_event.id} mis à jour avec succès !")

    except ValueError as e:
        click.echo(f"Erreur de validation : {str(e)}")
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")


@requires_auth(required_roles=[1, 3])
def delete_event(user):
    """ Suppression d'un événement. """
    try:
        event_id = click.prompt("Entrez l'ID de l'événement à supprimer", type=int)

        with SessionLocal() as session:
            service = EventService(session)
            event = service.get_by_id(event_id)

            if not event:
                click.echo("Événement introuvable.")
                return

            confirm = click.confirm(f"Voulez-vous vraiment supprimer l'événement {event.id} ?", default=False)
            if confirm:
                service.delete(event_id)
                log_info(f"Événement {event.id} supprimé avec succès.")
                click.echo("Événement supprimé avec succès.")
            else:
                click.echo("Suppression annulée.")

    except Exception as e:
        log_error(f"Erreur lors de la suppression de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")