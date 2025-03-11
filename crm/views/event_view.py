from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.panel import Panel
import click
from datetime import datetime

console = Console()


class EventView:

    @staticmethod
    def show_menu():
        """
        Affiche le menu de gestion des événements.
        """
        console.print("\n[bold cyan]╭──────────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Événements  │[/bold cyan]")
        console.print("[bold cyan]╰──────────────────╯[/bold cyan]")
        console.print("\n[1] Lister tous les événements")
        console.print("[2] Voir un événement par ID")
        console.print("[3] Créer un événement")
        console.print("[4] Modifier un événement")
        console.print("[5] Supprimer un événement")
        console.print("[6] Filtrer les événements")

        console.print("[0] Retour au menu principal\n")

    @staticmethod
    def display_events(events):
        """
        Affiche tous les événements sous forme de tableau.
        """
        table = Table(title="\n[bold cyan]Liste des Événements[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Titre")
        table.add_column("Début")
        table.add_column("Fin")
        table.add_column("Lieu")
        table.add_column("Participants", justify="center")
        table.add_column("Contrat")
        table.add_column("Client")
        table.add_column("Support")

        
        for event in events:
            client_info = (
                f"{event.client.id} ({event.client.first_name} {event.client.last_name}) - {event.client.company.title}"
                if event.client and event.client.company
                else f"{event.client.id} ({event.client.first_name} {event.client.last_name}) - Non assigné"
                if event.client
                else "Aucun client"
)

            table.add_row(
                str(event.id),
                event.title,
                event.event_startdate.strftime("%Y-%m-%d") if event.event_startdate else "N/A",
                event.event_enddate.strftime("%Y-%m-%d") if event.event_enddate else "N/A",
                event.location if event.location else "N/A",
                str(event.attendees) if event.attendees else "N/A",
                str(event.contracts_id),
                client_info,
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
        """
        Affiche un événement sous forme de fiche détaillée.
        """

        def format_date(date_value):
            """Convertit un datetime en string formatée, sinon retourne 'N/A'."""
            if isinstance(date_value, datetime):
                return date_value.strftime('%Y-%m-%d')
            return "N/A" if not date_value else str(date_value)
    
        event_details = f"""
        [cyan bold]Fiche Événement: {event.title}, id:{event.id}[/cyan bold]

        ─────────────────

        [cyan bold]Début:[/cyan bold] {format_date(event.event_startdate)}
        [cyan bold]Fin:[/cyan bold] {format_date(event.event_enddate)}
        [cyan bold]Lieu:[/cyan bold] {event.location if event.location else 'N/A'}
        [cyan bold]Participants:[/cyan bold] {event.attendees if event.attendees else 'N/A'}
        [cyan bold]Contrat ID:[/cyan bold] {event.contracts_id}
        [cyan bold]Client:[/cyan bold] {event.client.last_name} {event.client.first_name} (id:{event.clients_id})- {event.client.company.title if event.client.company else 'Non assigné'}(id: {event.client.companies_id if event.client.companies_id else 'N/A'})
        [cyan bold]Note:[/cyan bold] {event.note}
        [cyan bold]Créé le:[/cyan bold] {format_date(event.created_at)}
        [cyan bold]Modifié le:[/cyan bold] {format_date(event.updated_at) if event.updated_at else 'N/A'}
        [cyan bold]Supprimé le:[/cyan bold] {format_date(event.deleted_at) if event.deleted_at else 'Non supprimé'}
        [cyan bold]Support:[/cyan bold] {", ".join(f"ID {user.id} - {user.username}" for user in event.users) if event.users else 'Non assigné'}
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
        """
        Demande les informations pour créer un événement.
        """
        console.print("\n[bold cyan]Création d'un nouvel événement[/bold cyan]")
        title = Prompt.ask("Nom de l'événement").strip()

        event_startdate = Prompt.ask("Date de début (YYYY-MM-DD)", default="").strip()
        event_startdate = event_startdate if event_startdate else None  

        event_enddate = Prompt.ask("Date de fin (YYYY-MM-DD)", default="").strip()
        event_enddate = event_enddate if event_enddate else None  

        location = Prompt.ask("Lieu de l'événement (laisser vide si inconnu)", default="").strip()
        location = location if location else None 

        attendees = Prompt.ask("Nombre de participants (laisser vide si inconnu)", default="")
        attendees = int(attendees) if attendees.isdigit() else None  

        note = Prompt.ask("Commentaires", default="").strip()
        note = note if note else None  

        clients_id = Prompt.ask("ID du Client").strip()
        while not clients_id.isdigit():
            clients_id = Prompt.ask("[red]L'ID du Client doit être un nombre valide.[/red]").strip()
        clients_id = int(clients_id)

        contracts_id = Prompt.ask("ID du Contrat").strip()
        while not contracts_id.isdigit():
            contracts_id = Prompt.ask("[red]L'ID du Contrat doit être un nombre valide.[/red]").strip()
        contracts_id = int(contracts_id)

        support_id = Prompt.ask("ID du Support (laisser vide si aucun)", default="").strip()
        support_id = int(support_id) if support_id.isdigit() else None  # ✅ Convertit en int ou None

        return {
            "title": title,
            "event_startdate": event_startdate,
            "event_enddate": event_enddate,
            "location": location,
            "attendees": attendees,
            "note": note,
            "clients_id": clients_id,
            "contracts_id": contracts_id,
        }, support_id

    @staticmethod
    def prompt_event_update(event):
        """
        Permet de modifier un événement existant.
        """
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

            elif choice == 9:
                new_support_id = Prompt.ask(f"ID du Support actuel : [cyan]{', '.join(f'{user.id} ({user.username})' for user in event.users) if event.users else 'N/A'}[/cyan] ➝ Nouveau ID du Support", default="")
                update_data["support_id"] = int(new_support_id) if new_support_id.isdigit() else None

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
        """
        Affiche un message avec couleur adaptée.
        """
        colors = {"success": "green", "error": "red", "info": "cyan"}
        console.print(f"[{colors.get(msg_type, 'white')}] {message} [/{colors.get(msg_type, 'white')}]")

    @staticmethod
    def prompt_event_filters():
        """
        Affiche un menu pour sélectionner plusieurs critères de filtrage des événements.
        """
        filters = {}

        console.print("\n[bold cyan]Sélection des filtres pour les événements[/bold cyan]")
        
        filter_options = {
            "1": "Date de début",
            "2": "Date de fin",
            "3": "Client ID",
            "4": "Contrat ID",
            "5": "Support ID",
        }

        # Affichage des options
        for key, option in filter_options.items():
            console.print(f"[{key}] {option}")

        selected_options = Prompt.ask(
            "Entrez les numéros des filtres à appliquer (séparés par une virgule)", 
            default="",
        ).split(",")

        for option in selected_options:
            option = option.strip()
            if option in filter_options:
                if option == "1":
                    filters["event_startdate"] = Prompt.ask("Entrez la date de début (YYYY-MM-DD)")
                elif option == "2":
                    filters["event_enddate"] = Prompt.ask("Entrez la date de fin (YYYY-MM-DD)")
                elif option == "3":
                    filters["clients_id"] = Prompt.ask("Entrez l'ID du client")
                elif option == "4":
                    filters["contracts_id"] = Prompt.ask("Entrez l'ID du contrat")
                elif option == "5":
                    filters["support_id"] = Prompt.ask("Entrez l'ID du support")

        return filters