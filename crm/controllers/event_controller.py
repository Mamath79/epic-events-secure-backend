import click
from crm.views.event_view import EventView
from crm.services.event_service import EventService
from crm.database.base import SessionLocal

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
            click.echo("Option invalide, veuillez réessayer.")

def list_all_events():
    """Liste tous les événements."""
    session = SessionLocal()
    service = EventService(session)
    events = service.get_all()
    session.close()

    if events:
        EventView.display_events(events)
    else:
        click.echo("Aucun événement trouvé.")

def get_event_by_id():
    """Récupère un événement par son ID."""
    event_id = click.prompt("Entrez l'ID de l'événement", type=int)
    
    session = SessionLocal()
    service = EventService(session)
    event = service.get_by_id(event_id)
    session.close()

    if event:
        EventView.display_event(event)
    else:
        click.echo("Événement introuvable.")

def create_event():
    """Création d'un nouvel événement."""
    data = EventView.prompt_event_data()

    session = SessionLocal()
    service = EventService(session)
    try:
        new_event = service.create(data)
        session.close()
        click.echo(f"Événement {new_event.id} ajouté avec succès !")
    except Exception as e:
        click.echo(f"Erreur lors de la création de l'événement : {e}")

def update_event():
    """Mise à jour d'un événement existant."""
    event_id = click.prompt("Entrez l'ID de l'événement à modifier", type=int)
    
    session = SessionLocal()
    service = EventService(session)
    event = service.get_by_id(event_id)

    if not event:
        session.close()
        click.echo("Événement introuvable.")
        return

    new_data = EventView.prompt_event_update(event)
    try:
        updated_event = service.update(event_id, new_data)
        session.close()
        click.echo(f"Événement {updated_event.id} mis à jour !")
    except Exception as e:
        click.echo(f"Erreur lors de la mise à jour : {e}")

def delete_event():
    """Suppression d'un événement."""
    event_id = click.prompt("Entrez l'ID de l'événement à supprimer", type=int)

    session = SessionLocal()
    service = EventService(session)
    event = service.get_by_id(event_id)

    if not event:
        session.close()
        click.echo("Événement introuvable.")
        return

    confirm = click.confirm(f"Voulez-vous vraiment supprimer l'événement {event.id} ?", default=False)
    if confirm:
        service.delete(event_id)
        session.close()
        click.echo("Événement supprimé avec succès.")
    else:
        session.close()
        click.echo("Suppression annulée.")
