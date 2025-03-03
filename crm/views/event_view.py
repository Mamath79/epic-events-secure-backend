from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

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
        table = Table(title="Liste des Événements", show_lines=True)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Nom", style="green")
        table.add_column("Date", style="yellow")
        table.add_column("Contrat ID", style="magenta")
        table.add_column("Support ID", style="blue")

        for event in events:
            table.add_row(
                str(event.id),
                event.name,
                event.date.strftime("%d/%m/%Y"),
                str(event.contract_id),
                str(event.support_id) if event.support_id else "Non assigné"
            )

        console.print(table)

    @staticmethod
    def display_event(event):
        """Affiche les détails d'un événement."""
        console.print(f"[cyan bold]ID:[/cyan bold] {event.id}")
        console.print(f"[cyan bold]Nom:[/cyan bold] {event.name}")
        console.print(f"[cyan bold]Date:[/cyan bold] {event.date.strftime('%d/%m/%Y')}")
        console.print(f"[cyan bold]Contrat ID:[/cyan bold] {event.contract_id}")
        console.print(f"[cyan bold]Support ID:[/cyan bold] {event.support_id or 'Non assigné'}")

    @staticmethod
    def prompt_event_data():
        """Demande les informations pour créer un événement."""
        name = Prompt.ask("Nom de l'événement")
        date = Prompt.ask("Date (YYYY-MM-DD)")
        contract_id = Prompt.ask("ID du Contrat", type=int)
        support_id = Prompt.ask("ID du Support (laisser vide si aucun)", default=None)

        return {
            "name": name,
            "date": date,
            "contract_id": contract_id,
            "support_id": support_id
        }

    @staticmethod
    def prompt_event_update(event):
        """Demande les nouvelles informations pour modifier un événement."""
        name = Prompt.ask("Nom de l'événement", default=event.name)
        date = Prompt.ask("Date (YYYY-MM-DD)", default=event.date.strftime('%Y-%m-%d'))
        support_id = Prompt.ask("ID du Support", default=str(event.support_id) if event.support_id else "N/A")

        return {
            "name": name,
            "date": date,
            "support_id": support_id if support_id != "N/A" else None
        }
