from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import click

console = Console()


class EventView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des événements."""
        console.print("\n[bold cyan]╭──────────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Événements │[/bold cyan]")
        console.print("[bold cyan]╰──────────────────╯[/bold cyan]")
        console.print("\n[1] Lister tous les événements")
        console.print("[2] Voir un événement par ID")
        console.print("[3] Créer un événement")
        console.print("[4] Modifier un événement")
        console.print("[5] Supprimer un événement")
        console.print("[0] Retour au menu principal\n")

    @staticmethod
    def display_events(events):
        """Affiche tous les événements sous forme de tableau."""
        table = Table(title="\n[bold cyan]Liste des Événements[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Titre", style="green")
        table.add_column("Début", style="yellow")
        table.add_column("Fin", style="yellow")
        table.add_column("Lieu", style="blue")
        table.add_column("Participants", justify="center")
        table.add_column("Contrat ID", justify="center")
        table.add_column("Client ID", justify="center")
        table.add_column("Support", style="magenta")

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
                ", ".join(f"{user.id} ({user.username})" for user in event.users) if event.users else "Non assigné",
            )

        # Calcul de la largeur de la table
        table_width = console.measure(table).maximum

        # Affichage dynamique des séparateurs
        console.print("\n" + "═" * table_width, style="bold white")
        console.print(table)
        console.print("\n" + "═" * table_width, style="bold white")

    @staticmethod
    def display_event(event):
        """Affiche un événement sous forme de fiche détaillée."""
        event_details = f"""
        [cyan bold]Fiche Événement[/cyan bold]

        ─────────────────

        [cyan bold]ID:[/cyan bold] {event.id}
        [green bold]Titre:[/green bold] {event.title}
        [yellow bold]Début:[/yellow bold] {event.event_startdate.strftime('%Y-%m-%d') if event.event_startdate else 'N/A'}
        [yellow bold]Fin:[/yellow bold] {event.event_enddate.strftime('%Y-%m-%d') if event.event_enddate else 'N/A'}
        [blue bold]Lieu:[/blue bold] {event.location if event.location else 'N/A'}
        [cyan bold]Participants:[/cyan bold] {event.attendees if event.attendees else 'N/A'}
        [white bold]Contrat ID:[/white bold] {event.contracts_id}
        [white bold]Client ID:[/white bold] {event.clients_id}
        [magenta bold]Support:[/magenta bold] {", ".join(f"ID {user.id} - {user.username}" for user in event.users) if event.users else 'Non assigné'}
        """

        console.print(
            Panel.fit(
                event_details,
                title="\n[bold cyan]Détails Événement[/bold cyan]",
                style="white",
            )
        )

    @staticmethod
    def prompt_event_data():
        """Demande les informations pour créer un événement."""
        console.print("\n[bold cyan]Création d'un nouvel événement[/bold cyan]")
        title = Prompt.ask("Nom de l'événement")
        event_startdate = Prompt.ask("Date de début (YYYY-MM-DD)")
        event_enddate = Prompt.ask("Date de fin (YYYY-MM-DD)")
        location = Prompt.ask("Lieu de l'événement (laisser vide si inconnu)", default="")
        attendees = Prompt.ask("Nombre de participants (laisser vide si inconnu)", default="")
        note = Prompt.ask("Commentaires", default="")
        
        clients_id = Prompt.ask("ID du Client")
        while not clients_id.isdigit():
            clients_id = Prompt.ask("[red]L'ID du Client doit être un nombre valide.[/red]")
        clients_id = int(clients_id)

        contracts_id = Prompt.ask("ID du Contrat")
        while not contracts_id.isdigit():
            contracts_id = Prompt.ask("[red]L'ID du Contrat doit être un nombre valide.[/red]")
        contracts_id = int(contracts_id)

        support_id = Prompt.ask("ID du Support (laisser vide si aucun)", default="")
        support_id = int(support_id) if support_id.isdigit() else None

        return {
            "title": title,
            "event_startdate": event_startdate,
            "event_enddate": event_enddate,
            "location": location or None,
            "attendees": int(attendees) if attendees.isdigit() else None,
            "note": note,
            "clients_id": clients_id,
            "contracts_id": contracts_id,
            "support_id": support_id,
        }

    @staticmethod
    def prompt_event_update(event):
        """Permet de modifier un événement existant."""
        console.print("\n[bold cyan]Mise à jour d'un événement[/bold cyan]")
        update_data = {}

        while True:
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

            fields = {
                1: ("title", "Nom de l'événement"),
                2: ("event_startdate", "Date de début (YYYY-MM-DD)"),
                3: ("event_enddate", "Date de fin (YYYY-MM-DD)"),
                4: ("location", "Lieu"),
                5: ("attendees", "Nombre de participants"),
                6: ("note", "Commentaires"),
                7: ("clients_id", "ID du Client"),
                8: ("contracts_id", "ID du Contrat"),
                9: ("support_id", "ID du Support"),
            }

            if choice in fields:
                field, label = fields[choice]
                new_value = Prompt.ask(f"{label} actuel : [cyan]{getattr(event, field, 'N/A')}[/cyan] ➝ Nouveau {label}")
                update_data[field] = int(new_value) if new_value.isdigit() else new_value

            elif choice == 0:
                if update_data:
                    console.print("\n[green]Modifications enregistrées.[/green]")
                else:
                    console.print("\n[yellow]Aucune modification effectuée.[/yellow]")
                break

            else:
                console.print("\n[red]Option invalide, veuillez réessayer.[/red]")

        return update_data

    @staticmethod
    def display_message(message, msg_type="info"):
        """Affiche un message avec couleur adaptée."""
        colors = {"success": "green", "error": "red", "info": "cyan"}
        console.print(f"[{colors.get(msg_type, 'white')}] {message} [/{colors.get(msg_type, 'white')}]")
