import click
from crm.views.event_view import EventView
from crm.services.event_service import EventService
from crm.database.base import SessionLocal
from crm.services.user_service import UserService


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
    """Création d'un nouvel événement avec support manager optionnel."""
    session = SessionLocal()
    event_service = EventService(session)
    user_service = UserService(session)

    try:
        # Récupération des données depuis la Vue
        event_data = EventView.prompt_event_data()

        # Vérification de l'existence du client et du contrat
        if not event_service.validate_client_contract(event_data["clients_id"], event_data["contracts_id"]):
            EventView.display_message("Erreur: Client ou Contrat invalide.", "error")
            return

        # Création de l'événement
        new_event = event_service.create({
            "title": event_data["title"],
            "event_startdate": event_data["event_startdate"],
            "event_enddate": event_data["event_enddate"],
            "location": event_data["location"],
            "attendees": event_data["attendees"],
            "note": event_data["note"],
            "contracts_id": event_data["contracts_id"],
            "clients_id": event_data["clients_id"]
        })

        # Assignation d'un support manager si fourni
        if event_data["support_id"]:
            support_user = user_service.get_by_id(event_data["support_id"])
            if support_user:
                event_service.assign_support(new_event, support_user)
                session.commit()  # ✅ On commit ici pour sauvegarder tout en une seule transaction
                EventView.display_message(f"Support Manager {support_user.username} assigné à l'événement !", "success")
            else:
                EventView.display_message(f"Erreur: Aucun utilisateur trouvé avec l'ID {event_data['support_id']}", "error")

        EventView.display_message(f"Événement {new_event.id} ajouté avec succès !", "success")

    except Exception as e:
        session.rollback()
        EventView.display_message(f"Erreur lors de la création de l'événement : {e}", "error")

    finally:
        session.close()


def update_event():
    """
    Mise à jour d'un événement existant, y compris l'ajout/suppression du support manager.
    """
    event_id = click.prompt("Entrez l'ID de l'événement à modifier", type=int)
    
    session = SessionLocal()
    event_service = EventService(session)
    user_service = UserService(session)
    event = event_service.get_by_id(event_id)

    if not event:
        session.close()
        click.echo("Événement introuvable.")
        return

    update_data = EventView.prompt_event_update(event)

    try:
        # Si un ID de support est fourni, on l'ajoute ou on le retire
        if "support_id" in update_data:
            support_id = update_data.pop("support_id")
            if support_id:
                support_user = user_service.get_by_id(support_id)
                if support_user:
                    event_service.assign_support(event, support_user)
                    EventView.display_message(f"Support Manager {support_user.username} mis à jour !", "success")
                else:
                    EventView.display_message(f"Erreur: Aucun utilisateur trouvé avec l'ID {support_id}", "error")

        # Appliquer les autres modifications
        updated_event = event_service.update(event_id, update_data)
        session.commit()
        EventView.display_message(f"Événement {updated_event.id} mis à jour !", "success")

    except Exception as e:
        session.rollback()
        EventView.display_message(f"Erreur lors de la mise à jour : {e}", "error")

    finally:
        session.close()



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
