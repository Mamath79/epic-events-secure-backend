from rich.console import Console
from rich.prompt import Prompt


console = Console()


class LoginView:

    @staticmethod
    def login_menu():
        """
        Affiche l'écran de connexion
        """
        console.print("[bold cyan]╭─────────────────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Connexion à Epic Events │[/bold cyan]")
        console.print("[bold cyan]╰─────────────────────────╯[/bold cyan]")

        console.print("[1] Login")
        console.print("[0] exit")

        choice = console.input("[bold cyan]Sélectionnez une option > [/bold cyan]")

        return choice

    @staticmethod
    def prompt_login():
        """
        demande les identifiants
        """
        email = Prompt.ask("[bold cyan]Email[/bold cyan]")
        password = Prompt.ask("[bold cyan]Mot de passe[/bold cyan]", password=True)
        return email, password

    @staticmethod
    def show_success_login():
        """
        Affiche un message de connexion réussie
        """
        console.print("[green bold]Connexion réussie ![/green bold]")

    @staticmethod
    def show_error_login():
        """
        Affiche un message d'erreur
        """
        console.print("[red bold]Échec de l'authentification.[/red bold]")
