from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import click
from crm.controllers.company_controller import get_companies_list, create_company


console = Console()

class ClientView:

    @staticmethod
    def show_menu():
        """
        Affiche le menu de gestion des clients.
        """
        console.print("\n[bold cyan]╭─────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Client │[/bold cyan]")
        console.print("[bold cyan]╰─────────────╯[/bold cyan]")
        console.print("\n[1] Lister tous les Clients")
        console.print("[2] Lister un Client par ID")
        console.print("[3] Créer un Client")
        console.print("[4] Modifier un Client")
        console.print("[5] Supprimer un Client")
        console.print("[6] Gestion Client Company")
        console.print("[7] filter les clients")
        console.print("[0] Retour au menu principal")

    @staticmethod
    def display_clients(clients):
        """
        Affiche tous les clients sous forme de tableau.
        """
        table = Table(title="\n[bold cyan]Liste des clients[/bold cyan]\n")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Email")
        table.add_column("Téléphone")
        table.add_column("Entreprise_id")
        table.add_column("Entreprise_title")
        table.add_column("Créé le")
        table.add_column("Modifié le")
        table.add_column("Supprimé le")

        for client in clients:
            company_name = client.company.title if client.company else "Non assigné"
            table.add_row(
                str(client.id),
                client.last_name,
                client.first_name,
                client.email,
                client.phone_number or "N/A",
                str(client.companies_id) if client.companies_id else "N/A",
                company_name,
                client.creation_date.strftime("%d/%m/%Y %H:%M") if client.creation_date else "N/A",
                client.updated_date.strftime("%d/%m/%Y %H:%M") if client.updated_date else "N/A",
                client.deleted_at.strftime("%d/%m/%Y %H:%M") if client.deleted_at else "Non supprimé",
            )

        console.print("\n" + "═" * console.measure(table).maximum, style="bold white")
        console.print(table)
        console.print("\n" + "═" * console.measure(table).maximum, style="bold white")

    @staticmethod
    def display_client(client):
        """
        Affiche un client sous forme de fiche détaillée.
        """
        company_name = client.company.title if client.company else "Non assigné"

        client_details = f"""
        [cyan bold]Fiche Client ID:{client.id}[/cyan bold]

        ──────────────────

        [cyan bold]Nom:[/cyan bold] {client.last_name} {client.first_name}
        [cyan bold]Email:[/cyan bold] {client.email}
        [cyan bold]Téléphone:[/cyan bold] {client.phone_number or "N/A"}
        [cyan bold]Nom Entreprise:[/cyan bold] {company_name}, id: {client.companies_id if client.companies_id else "N/A"}
        [cyan bold]Créé le:[/cyan bold] {client.creation_date.strftime('%d/%m/%Y %H:%M') if client.creation_date else "N/A"}
        [cyan bold]Modifié le:[/cyan bold] {client.updated_date.strftime('%d/%m/%Y %H:%M') if client.updated_date else "N/A"}
        [cyan bold]Supprimé le:[/cyan bold] {client.deleted_at.strftime('%d/%m/%Y %H:%M') if client.deleted_at else "Non supprimé"}
        """

        console.print(
            Panel.fit(
                client_details,
                title="[bold cyan]Détails Client[/bold cyan]",
                style="white",
            )
        )

    @staticmethod
    def prompt_client_data():
        """
        Demande les informations pour créer un client.
        """
        console.print("\n[bold cyan]Création d'un nouveau client[/bold cyan]")
        last_name = Prompt.ask("Nom").strip()
        first_name = Prompt.ask("Prénom").strip()
        email = Prompt.ask("Email").strip()
        phone_number = Prompt.ask("Téléphone").strip()

        console.print("\n[bold cyan]Sélection de l'entreprise[/bold cyan]")
        companies = get_companies_list()
        for company in companies:
            console.print(f"[bold cyan]{company.id}[/bold cyan] - {company.title}")

        company_choice = Prompt.ask("Entrez l'ID de l'entreprise", default="0")
        companies_id = int(company_choice) if company_choice.isdigit() else None

        return {
            "last_name": last_name,
            "first_name": first_name,
            "email": email,
            "phone_number": phone_number,
            "companies_id": companies_id,
        }

    @staticmethod
    def prompt_client_update(client):
        """
        Permet de choisir un ou plusieurs paramètres à modifier sans tout ressaisir.
        """
        update_data = {}
        
        while True:
            console.print("\n[bold cyan]Mise à jour d'un client[/bold cyan]")
            console.print("[1] Modifier le prénom")
            console.print("[2] Modifier le nom")
            console.print("[3] Modifier l'email")
            console.print("[4] Modifier le téléphone")
            console.print("[5] Modifier l'entreprise")
            console.print("[0] Terminer la modification")

            choice = click.prompt("Entrez le numéro du champ à modifier", type=int)

            if choice == 1:
                update_data["first_name"] = Prompt.ask("Nouveau prénom", default=client.first_name)
            elif choice == 2:
                update_data["last_name"] = Prompt.ask("Nouveau nom", default=client.last_name)
            elif choice == 3:
                update_data["email"] = Prompt.ask("Nouvel email", default=client.email)
            elif choice == 4:
                update_data["phone_number"] = Prompt.ask("Nouveau téléphone", default=client.phone_number or "")
            elif choice == 5:
                update_data["companies_id"] = Prompt.ask("Nouvel ID d'entreprise", default=str(client.companies_id or ""))
            elif choice == 0:
                break
            else:
                console.print("[bold red]Option invalide, veuillez réessayer.[/bold red]")
        
        return update_data

    @staticmethod
    def prompt_client_filters():
        """
        Affiche un menu pour sélectionner plusieurs critères de filtrage des clients.
        """
        filters = {}

        console.print("\n[bold cyan]Sélection des filtres pour les clients[/bold cyan]")
        
        filter_options = {
            "1": "Prénom",
            "2": "Nom de famille",
            "3": "Email",
            "4": "Numéro de téléphone",
            "5": "ID de la société",
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
                    filters["first_name"] = Prompt.ask("Entrez le prénom")
                elif option == "2":
                    filters["last_name"] = Prompt.ask("Entrez le nom de famille")
                elif option == "3":
                    filters["email"] = Prompt.ask("Entrez l'email")
                elif option == "4":
                    filters["phone_number"] = Prompt.ask("Entrez le numéro de téléphone")
                elif option == "5":
                    filters["companies_id"] = Prompt.ask("Entrez l'ID de la société")

        return filters
