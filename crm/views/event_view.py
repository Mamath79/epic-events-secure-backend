from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import click

console = Console()

class EventView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des événements."""
        console.print("\n[bold cyan]╭───────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Événements │[/bold cyan]")
        console.print("[bold cyan]╰───────────────╯[/bold cyan]")
        console.print("[1] Lister tous les Événements")
        console.print("[2] Voir un Événement par ID")
        console.print("[3] Créer un Événement")
        console.print("[4] Modifier un Événement")
        console.print("[5] Supprimer un Événement")
        console.print("[0] Retour au menu principal")

    @staticmethod
    def display_events(events):
        """Affiche tous les événements sous forme de tableau."""
        table = Table(title="📋 Liste des Événements", show_lines=True)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Titre", style="green")
        table.add_column("Début", style="yellow")
        table.add_column("Fin", style="yellow")
        table.add_column("Lieu", style="magenta")
        table.add_column("Participants", style="blue", justify="center")
        table.add_column("Contrat ID", style="magenta")
        table.add_column("Client ID", style="cyan")
        table.add_column("Support", style="blue")

        for event in events:
            table.add_row(
                str(event.id),
                event.title,
                event.event_startdate.strftime("%Y-%m-%d") if event.event_startdate else "N/A",
                event.event_enddate.strftime("%Y-%m-%d") if event.event_enddate else "N/A",
                event.location if event.location else "N/A",
                str(event.attendees) if event.attendees else "N/A",
                str(event.contracts_id),
                str(event.clients_id),
                ", ".join(f"{user.id} ({user.username})" for user in event.users) if event.users else "Non assigné"
            )

        console.print(table)

    @staticmethod
    def display_event(event):
        """Affiche les détails d'un événement."""
        console.print("\n📌 [bold cyan]Détails de l'Événement[/bold cyan]")
        console.print(f"🆔 ID: [bold cyan]{event.id}[/bold cyan]")
        console.print(f"🏷️ Titre: [bold green]{event.title}[/bold green]")
        console.print(f"📅 Début: [bold yellow]{event.event_startdate.strftime('%Y-%m-%d') if event.event_startdate else 'N/A'}[/bold yellow]")
        console.print(f"📅 Fin: [bold yellow]{event.event_enddate.strftime('%Y-%m-%d') if event.event_enddate else 'N/A'}[/bold yellow]")
        console.print(f"📍 Lieu: [bold magenta]{event.location if event.location else 'N/A'}[/bold magenta]")
        console.print(f"👥 Participants: [bold blue]{event.attendees if event.attendees else 'N/A'}[/bold blue]")
        console.print(f"📄 Contrat ID: [bold magenta]{event.contracts_id}[/bold magenta]")
        console.print(f"👤 Client ID: [bold cyan]{event.clients_id}[/bold cyan]")
        
        support_info = ", ".join(f"ID {user.id} - {user.username}" for user in event.users) if event.users else "Non assigné"
        console.print(f"🛠️ Support: [bold blue]{support_info}[/bold blue]")

    @staticmethod
    def prompt_event_data():
        """Demande les informations pour créer un événement."""
        title = Prompt.ask("Nom de l'événement")
        event_startdate = Prompt.ask("Date de début (YYYY-MM-DD)")
        event_enddate = Prompt.ask("Date de fin (YYYY-MM-DD)")
        location = Prompt.ask("Lieu de l'événement (laisser vide si inconnu)", default="")
        attendees = Prompt.ask("Nombre de participants (laisser vide si inconnu)", default="")
        note = Prompt.ask("Commentaires",default="")
        clients_id = Prompt.ask("ID du Client")
        if not clients_id.isdigit():
            console.print("\n❌ [red]L'ID du Client doit être un nombre valide.[/red]")
            return None  # Annule la saisie si l'ID client est incorrect
        clients_id = int(clients_id)

        contracts_id = Prompt.ask("ID du Contrat")
        if not contracts_id.isdigit():
            console.print("\n❌ [red]L'ID du Contrat doit être un nombre valide.[/red]")
            return None
        contracts_id = int(contracts_id)

        support_id = Prompt.ask("ID du Support (laisser vide si aucun)", default="")
        support_id = int(support_id) if support_id.isdigit() else None

        return {
            "title": title,
            "event_startdate": event_startdate,
            "event_enddate": event_enddate,
            "location": location or None,
            "attendees": int(attendees) if attendees.isdigit() else None,
            "note":note,
            "clients_id": clients_id,
            "contracts_id": contracts_id,
            "support_id": support_id
        }

    @staticmethod
    def prompt_event_update(event):
        """
        Permet de choisir un ou plusieurs paramètres à modifier sans tout ressaisir.
        """

        update_data = {}

        while True:
            console.print("\n📌 [bold cyan]Mise à jour d'un événement[/bold cyan]")
            console.print("[bold yellow]Sélectionnez un paramètre à modifier :[/bold yellow]")
            console.print("[1] Nom de l'événement")
            console.print("[2] Date de début")
            console.print("[3] Date de fin")
            console.print("[4] Lieu de l'événement")
            console.print("[5] Nombre de participants")
            console.print("[6] Commentaires")
            console.print("[7] ID du Client")
            console.print("[8] ID du Contrat")
            console.print("[9] ID du Support (ajouter/enlever)")
            console.print("[0] Terminer la modification")

            choice = click.prompt("Entrez le numéro du champ à modifier", type=int)

            if choice == 1:
                new_value = Prompt.ask(f"Nom actuel : [cyan]{event.title}[/cyan] ➝ Nouveau nom")
                update_data["title"] = new_value

            elif choice == 2:
                new_value = Prompt.ask(f"Date de début actuelle : [yellow]{event.event_startdate.strftime('%Y-%m-%d')}[/yellow] ➝ Nouvelle date (YYYY-MM-DD)")
                update_data["event_startdate"] = new_value

            elif choice == 3:
                new_value = Prompt.ask(f"Date de fin actuelle : [yellow]{event.event_enddate.strftime('%Y-%m-%d')}[/yellow] ➝ Nouvelle date (YYYY-MM-DD)")
                update_data["event_enddate"] = new_value

            elif choice == 4:
                new_value = Prompt.ask(f"Lieu actuel : [blue]{event.location if event.location else 'Non défini'}[/blue] ➝ Nouveau lieu")
                update_data["location"] = new_value

            elif choice == 5:
                new_value = Prompt.ask(f"Participants actuels : [magenta]{event.attendees if event.attendees else 'N/A'}[/magenta] ➝ Nouveau nombre de participants")
                update_data["attendees"] = int(new_value) if new_value.isdigit() else None

            elif choice == 6:
                new_value = Prompt.ask(f"Commentaires actuels : [green]{event.note if event.note else 'N/A'}[/green] ➝ Nouveaux commentaires")
                update_data["note"] = new_value

            elif choice == 7:
                new_value = Prompt.ask(f"ID Client actuel : [cyan]{event.clients_id}[/cyan] ➝ Nouvel ID Client")
                update_data["clients_id"] = int(new_value) if new_value.isdigit() else None

            elif choice == 8:
                new_value = Prompt.ask(f"ID Contrat actuel : [red]{event.contracts_id}[/red] ➝ Nouvel ID Contrat")
                update_data["contracts_id"] = int(new_value) if new_value.isdigit() else None

            elif choice == 9:
                new_value = Prompt.ask(f"Entrez un ID support à ajouter/enlever, ou laissez vide pour ne rien changer ()")
                if new_value.isdigit():
                    update_data["support_id"] = int(new_value)

            elif choice == 0:
                if update_data:
                    console.print("\n✅ [green]Modifications enregistrées.[/green]")
                else:
                    console.print("\n⚠️ [yellow]Aucune modification effectuée.[/yellow]")
                break  # Sort de la boucle

            else:
                console.print("\n❌ [red]Option invalide, veuillez réessayer.[/red]")

        return update_data


    @staticmethod
    def display_message(message, msg_type="info"):
        colors = {"success": "green", "error": "red", "info": "cyan"}
        console.print(f"[{colors.get(msg_type, 'white')}] {message} [/{colors.get(msg_type, 'white')}]")
