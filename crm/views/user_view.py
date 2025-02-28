from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class UserView:
    @staticmethod
    def display_users(users):
        """Affiche tous les utilisateurs sous forme de tableau"""
        table = Table(title="Liste des utilisateurs")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom d'utilisateur", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Département", justify="center", style="yellow")

        for user in users:
            table.add_row(str(user.id), user.username, user.email, str(user.departments_id))

        console.print(table)

    @staticmethod
    def display_user(user):
        """Affiche un utilisateur spécifique"""
        console.print("[bold cyan]Détails de l'utilisateur :[/bold cyan]")
        console.print(f"[yellow]ID : {user.id}[/yellow]")
        console.print(f"[yellow]Nom d'utilisateur : {user.username}[/yellow]")
        console.print(f"[yellow]Email : {user.email}[/yellow]")
        console.print(f"[yellow]Département : {user.departments_id}[/yellow]")

    @staticmethod
    def prompt_create_user():
        """Demande les informations pour créer un utilisateur"""
        console.print("[bold cyan]Création d'un nouvel utilisateur[/bold cyan]")
        email = Prompt.ask("Email")
        username = Prompt.ask("Nom d'utilisateur")
        password = Prompt.ask("Mot de passe", password=True)
        departments_id = Prompt.ask("ID du département", default="1")
        return {
            "email": email,
            "username": username,
            "password": password,
            "departments_id": int(departments_id)
        }

    @staticmethod
    def show_user_creation(user):
        """Affiche un message après la création d'un utilisateur"""
        if user:
            console.print(f"[green bold]Utilisateur {user.username} créé avec succès ![/green bold]")
        else:
            console.print("[red bold]Échec de la création de l'utilisateur.[/red bold]")

    @staticmethod
    def prompt_update_user():
        """Demande les nouvelles informations pour mettre à jour un utilisateur"""
        console.print("[bold cyan]Mise à jour d'un utilisateur[/bold cyan]")
        user_id = Prompt.ask("ID de l'utilisateur à modifier")
        email = Prompt.ask("Nouveau Email (laisser vide pour ne pas modifier)")
        username = Prompt.ask("Nouveau Nom d'utilisateur (laisser vide pour ne pas modifier)")
        departments_id = Prompt.ask("Nouveau ID du département (laisser vide pour ne pas modifier)")

        update_data = {"user_id": int(user_id)}
        if email:
            update_data["email"] = email
        if username:
            update_data["username"] = username
        if departments_id:
            update_data["departments_id"] = int(departments_id)

        return update_data

    @staticmethod
    def show_user_update(user):
        """Affiche un message après une mise à jour"""
        console.print(f"[green bold]Utilisateur {user.username} mis à jour avec succès ![/green bold]")

    @staticmethod
    def prompt_delete_user():
        """Demande la confirmation de suppression"""
        console.print("[bold red]Suppression d'un utilisateur[/bold red]")
        user_id = Prompt.ask("ID de l'utilisateur à supprimer")
        return int(user_id)

    @staticmethod
    def show_user_deletion(user_id):
        """Affiche un message après suppression"""
        console.print(f"[red bold]Utilisateur ID {user_id} supprimé avec succès ![/red bold]")
