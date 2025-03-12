import click
from sentry_sdk import capture_exception
from crm.views.event_view import EventView
from crm.services.event_service import EventService
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
            log_info("Consultation de tous les événements")
            list_all_events()
        elif choice == 2:
            log_info("Consultation d'un événement par ID")
            get_event_by_id()
        elif choice == 3:
            log_info("Création d'un événement")
            create_event()
        elif choice == 4:
            log_info("Mise à jour d'un événement")
            update_event()
        elif choice == 5:
            log_info("Suppression d'un événement")
            delete_event()
        elif choice == 6:
            log_info("Filtrage des événements")
            list_filtered_events()
        elif choice == 0:
            log_info("Retour au menu principal")
            break
        else:
            click.secho("Option invalide, veuillez réessayer.", fg="red", bold=True)


@requires_auth(read_only=True)
def list_all_events(user):
    """Liste tous les événements."""
    try:
        with SessionLocal() as session:
            service = EventService(session)
            events = service.get_all()

            if events:
                EventView.display_events(events)
            else:
                click.secho("Aucun événement trouvé.", fg="yellow", bold=True)

    except Exception as e:
        log_error(f"Erreur lors de la récupération des événements : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(read_only=True)
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
                click.secho("Événement introuvable.", fg="yellow", bold=True)

    except Exception as e:
        log_error(f"Erreur lors de la récupération de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(required_roles=[1, 3])
def create_event(user):
    """Création d'un nouvel événement avec support manager optionnel."""
    try:
        with SessionLocal() as session:
            event_service = EventService(session)
            data, support_id = EventView.prompt_event_data()
            new_event = event_service.create(data, support_id=support_id)

            log_info(f"Événement {new_event.id} créé avec succès.")
            click.secho(f"Événement {new_event.id} ajouté avec succès !", fg="green", bold=True)

    except ValueError as e:
        click.secho(f"Erreur de validation : {str(e)}", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la création de l'événement : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(required_roles=[1, 2, 3])
def update_event(user):
    """Mise à jour d'un événement existant."""
    try:
        event_id = click.prompt("Entrez l'ID de l'événement à modifier", type=int)

        with SessionLocal() as session:
            event_service = EventService(session)
            event = event_service.get_by_id(event_id)

            if not event:
                click.secho("Événement introuvable.", fg="yellow", bold=True)
                return

            update_data = EventView.prompt_event_update(event)
            updated_event = event_service.update(event_id, update_data)

            log_info(f"Événement {updated_event.id} mis à jour avec succès.")
            click.secho(f"Événement {updated_event.id} mis à jour avec succès !", fg="green", bold=True)

    except ValueError as e:
        click.secho(f"Erreur de validation : {str(e)}", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(required_roles=[1, 3])
def delete_event(user):
    """Suppression d'un événement."""
    try:
        event_id = click.prompt("Entrez l'ID de l'événement à supprimer", type=int)

        with SessionLocal() as session:
            service = EventService(session)
            event = service.get_by_id(event_id)

            if not event:
                click.secho("Événement introuvable.", fg="yellow", bold=True)
                return

            confirm = click.confirm(f"Voulez-vous vraiment supprimer l'événement {event.id} ?", default=False)
            if confirm:
                service.delete(event_id)
                log_info(f"Événement {event.id} supprimé avec succès.")
                click.secho("Événement supprimé avec succès.", fg="green", bold=True)
            else:
                click.secho("Suppression annulée.", fg="yellow", bold=True)

    except Exception as e:
        log_error(f"Erreur lors de la suppression de l'événement {event_id} : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)


@requires_auth(read_only=True)
def list_filtered_events(user):
    """Affiche la liste des événements en appliquant des filtres sélectionnés par l'utilisateur."""
    session = SessionLocal()
    service = EventService(session)
    try:
        filters = EventView.prompt_event_filters()  # Demande les critères de filtrage
        filtered_events = service.get_all_filtered(filters)
        if filtered_events:
            EventView.display_events(filtered_events)
        else:
            click.secho("Aucun événement trouvé avec ces filtres.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors du filtrage des événements : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)
    finally:
        session.close()
