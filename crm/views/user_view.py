from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import click

console = Console()

class UserView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des utilisateurs."""
        console.print("\n[bold cyan]╭────────────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Utilisateurs │[/bold cyan]")
        console.print("[bold cyan]╰────────────────────╯[/bold cyan]")
        console.print("[1] Lister tous les utilisateurs")
        console.print("[2] Voir un utilisateur par ID")
        console.print("[3] Créer un utilisateur")
        console.print("[4] Modifier un utilisateur")
        console.print("[5] Supprimer un utilisateur")
        console.print("[0] Retour au menu principal")

    @staticmethod
    def display_users(users):
        """Affiche tous les utilisateurs sous forme de tableau."""
        table = Table(title="📋 Liste des utilisateurs 📋")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom", style="green")
        table.add_column("Prénom", style="green")
        table.add_column("Nom d'utilisateur", style="magenta")
        table.add_column("Email", style="yellow")
        table.add_column("Département", justify="center", style="blue")

        for user in users:
            table.add_row(
                str(user.id),
                user.last_name,
                user.first_name,
                user.username,
                user.email,
                str(user.departments_id)
            )

        console.print(table)

    @staticmethod
    def display_user(user):
        """Affiche un utilisateur sous forme de fiche détaillée."""
        user_details = f"""
        [cyan bold]📄 Fiche Utilisateur 📄[/cyan bold]
        ────────────────────────────────────────
        [white bold]🆔 ID:[/white bold] {user.id}
        [white bold]👤 Nom:[/white bold] {user.last_name} {user.first_name}
        [yellow bold]📧 Email:[/yellow bold] {user.email}
        [blue bold]👤 Nom d'utilisateur:[/blue bold] {user.username}
        [magenta bold]🏢 Département:[/magenta bold] {user.departments_id}
        """

        console.print(Panel.fit(user_details, title="[bold cyan]📌 Détails Utilisateur[/bold cyan]", style="bold cyan"))

    @staticmethod
    def prompt_user_data():
        """Demande les informations pour créer un utilisateur."""
        console.print("\n[bold cyan]🆕 Création d'un nouvel utilisateur[/bold cyan]")
        last_name = Prompt.ask("Nom de famille").strip()
        first_name = Prompt.ask("Prénom").strip()
        email = Prompt.ask("Email").strip()
        username = Prompt.ask("Nom d'utilisateur").strip()
        password = Prompt.ask("Mot de passe", password=True).strip()
        departments_id = Prompt.ask("ID du département", default="1").strip()

        return {
            "last_name": last_name,
            "first_name": first_name,
            "email": email,
            "username": username,
            "password": password,
            "departments_id": int(departments_id)
        }

    @staticmethod
    def prompt_user_update(user):
        """Demande les informations à modifier pour un utilisateur."""
        console.print("\n📌 [bold cyan]Mise à jour d'un utilisateur[/bold cyan]")
        update_data = {}

        while True:
            console.print("[1] Modifier Nom")
            console.print("[2] Modifier Prénom")
            console.print("[3] Modifier Email")
            console.print("[4] Modifier Nom d'utilisateur")
            console.print("[5] Modifier Département")
            console.print("[0] Terminer la modification")

            choice = click.prompt("Choisissez une option", type=int)

            if choice == 1:
                update_data["last_name"] = Prompt.ask("Nouveau Nom", default=user.last_name)
            elif choice == 2:
                update_data["first_name"] = Prompt.ask("Nouveau Prénom", default=user.first_name)
            elif choice == 3:
                update_data["email"] = Prompt.ask("Nouvel Email", default=user.email)
            elif choice == 4:
                update_data["username"] = Prompt.ask("Nouveau Nom d'utilisateur", default=user.username)
            elif choice == 5:
                update_data["departments_id"] = Prompt.ask("Nouveau ID Département", default=str(user.departments_id))
            elif choice == 0:
                break
            else:
                console.print("❌ Option invalide, veuillez réessayer.")

        return update_data
