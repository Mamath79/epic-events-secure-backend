from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
import click
from crm.controllers.company_controller import get_companies_list, create_company

console = Console()

class ClientView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des clients."""
        console.print("\n[bold cyan]╭─────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Client │[/bold cyan]")
        console.print("[bold cyan]╰─────────────╯[/bold cyan]")
        console.print("[1] Lister tous les Clients")
        console.print("[2] Lister un Client par ID")
        console.print("[3] Créer un Client")
        console.print("[4] Modifier un Client")
        console.print("[5] Supprimer un Client")
        console.print("[0] Retour au menu principal")

    @staticmethod
    def display_clients(clients):
        """Affiche tous les clients sous forme de tableau détaillé avec une largeur dynamique."""

        # Création du tableau détaillé
        table = Table(show_header=True, header_style="bold magenta", title="📋 Liste des Clients 📋")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom", style="green", no_wrap=True)
        table.add_column("Prénom", style="green", no_wrap=True)
        table.add_column("Email", style="yellow", no_wrap=False)
        table.add_column("Téléphone", style="blue", no_wrap=False)
        table.add_column("Company", style="magenta", no_wrap=True)
        table.add_column("Créé le", style="white", no_wrap=True)
        table.add_column("Modifié le", style="white", no_wrap=True)
        table.add_column("Supprimé le", style="red", no_wrap=True)

        for client in clients:
            table.add_row(
                str(client.id),
                client.last_name,
                client.first_name,
                client.email,
                client.phone_number or "N/A",
                str(client.companies_id) if client.companies_id else "N/A",
                client.creation_date.strftime("%d/%m/%Y %H:%M") if client.creation_date else "N/A",
                client.updated_date.strftime("%d/%m/%Y %H:%M") if client.updated_date else "N/A",
                client.deleted_at.strftime("%d/%m/%Y %H:%M") if client.deleted_at else "Non supprimé"
            )

        # Calcul de la largeur de la table
        table_width = console.measure(table).maximum

        # Affichage dynamique des séparateurs
        console.print("\n" + "═" * table_width, style="bold white")
        console.print(table)
        console.print("\n" + "═" * table_width, style="bold white")

    @staticmethod
    def display_client(client):
        """Affiche un client sous forme de fiche détaillée proprement formatée."""

        client_details = f"""
            [cyan bold]📄 Fiche Client 📄[/cyan bold]
            ────────────────────────────────────────
            [white bold]🆔 ID:[/white bold] {client.id}
            [white bold]👤 Nom:[/white bold] {client.last_name} {client.first_name}
            [yellow bold]📧 Email:[/yellow bold] {client.email}
            [blue bold]📞 Téléphone:[/blue bold] {client.phone_number or "N/A"}
            [magenta bold]🏢 Entreprise:[/magenta bold] {client.companies_id or "N/A"}
            [green bold]🕒 Créé le:[/green bold] {client.creation_date.strftime('%d/%m/%Y %H:%M') if client.creation_date else "N/A"}
            [cyan bold]🔄 Modifié le:[/cyan bold] {client.updated_date.strftime('%d/%m/%Y %H:%M') if client.updated_date else "N/A"}
            [red bold]🗑 Supprimé le:[/red bold] {client.deleted_at.strftime('%d/%m/%Y %H:%M') if client.deleted_at else "Non supprimé"}
            """

        console.print(Panel.fit(client_details, title="[bold cyan]📌 Détails Client[/bold cyan]", style="bold cyan"))

    @staticmethod
    def prompt_client_data():
        """Demande les informations pour créer un client (tous les champs sont obligatoires)."""
        first_name = Prompt.ask("Prénom").strip()
        while not first_name:
            first_name = Prompt.ask("[red]❌ Prénom requis, veuillez entrer un prénom : [/red]").strip()

        last_name = Prompt.ask("Nom").strip()
        while not last_name:
            last_name = Prompt.ask("[red]❌ Nom requis, veuillez entrer un nom : [/red]").strip()

        email = Prompt.ask("Email").strip()
        while not email:
            email = Prompt.ask("[red]❌ Email requis, veuillez entrer un email : [/red]").strip()

        phone_number = Prompt.ask("Téléphone").strip()
        while not phone_number:
            phone_number = Prompt.ask("[red]❌ Téléphone requis, veuillez entrer un numéro : [/red]").strip()

        # Affichage des entreprises disponibles via CompanyController
        console.print("\n📌 [bold cyan]Sélection de l'entreprise[/bold cyan]")
        console.print("[bold yellow]0 - Ajouter une nouvelle entreprise[/bold yellow]")

        companies = get_companies_list()
        for company in companies:
            console.print(f"[bold green]{company.id}[/bold green] - {company.title}")

        company_choice = Prompt.ask("Entrez l'ID de l'entreprise ou 0 pour en ajouter une", default="0")

        if company_choice == "0":
            new_company = create_company()
            companies_id = new_company.id if new_company else None
        else:
            companies_id = int(company_choice) if company_choice.isdigit() else None

        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "companies_id": companies_id
        }

    @staticmethod
    def prompt_client_update(client):
        """
        Permet de choisir un ou plusieurs paramètres à modifier sans tout ressaisir.
        """

        update_data = {}

        while True:
            console.print("\n📌 [bold cyan]Mise à jour d'un client[/bold cyan]")
            console.print("[bold yellow]Sélectionnez un paramètre à modifier :[/bold yellow]")
            console.print("[1] Prénom")
            console.print("[2] Nom")
            console.print("[3] Email")
            console.print("[4] Téléphone")
            console.print("[5] Entreprise")
            console.print("[0] Terminer la modification")

            choice = click.prompt("Entrez le numéro du champ à modifier", type=int)

            if choice == 1:
                new_value = Prompt.ask(f"Prénom actuel : [cyan]{client.first_name}[/cyan] ➝ Nouveau prénom")
                update_data["first_name"] = new_value

            elif choice == 2:
                new_value = Prompt.ask(f"Nom actuel : [cyan]{client.last_name}[/cyan] ➝ Nouveau nom")
                update_data["last_name"] = new_value

            elif choice == 3:
                new_value = Prompt.ask(f"Email actuel : [yellow]{client.email}[/yellow] ➝ Nouvel email")
                update_data["email"] = new_value

            elif choice == 4:
                new_value = Prompt.ask(f"Téléphone actuel : [blue]{client.phone_number or 'N/A'}[/blue] ➝ Nouveau téléphone")
                update_data["phone_number"] = new_value

            elif choice == 5:
                # Affichage des entreprises disponibles via CompanyController
                console.print("\n📌 [bold cyan]Mise à jour de l'entreprise[/bold cyan]")
                console.print("[bold yellow]0 - Ajouter une nouvelle entreprise[/bold yellow]")
                console.print("[bold yellow]Laissez vide pour ne pas changer d'entreprise.[/bold yellow]")

                companies = get_companies_list()
                for company in companies:
                    console.print(f"[bold green]{company.id}[/bold green] - {company.name}")

                company_choice = Prompt.ask(f"Entreprise actuelle : [magenta]{client.companies_id or 'N/A'}[/magenta] ➝ ID de la nouvelle entreprise", default="")

                if company_choice.strip():
                    if company_choice == "0":
                        new_company = create_company()
                        update_data["companies_id"] = new_company.id if new_company else None  # ✅ Correction ici
                    elif company_choice.isdigit():
                        update_data["companies_id"] = int(company_choice)  # ✅ Utilisation correcte

            elif choice == 0:
                if update_data:
                    console.print("\n✅ [green]Modifications enregistrées.[/green]")
                else:
                    console.print("\n⚠️ [yellow]Aucune modification effectuée.[/yellow]")
                break  # Sort de la boucle

            else:
                console.print("\n❌ [red]Option invalide, veuillez réessayer.[/red]")

        return update_data