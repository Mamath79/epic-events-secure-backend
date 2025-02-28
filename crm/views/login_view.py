from rich.console import Console
from rich.prompt import Prompt


console = Console()

class LoginView:
    @staticmethod
    def prompt_login():
        """Affiche l'écran de connexion et demande les identifiants"""
        console.print("[bold cyan]╭─────────────────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Connexion à Epic Events │[/bold cyan]")
        console.print("[bold cyan]╰─────────────────────────╯[/bold cyan]")
        email = Prompt.ask("Email")
        password = Prompt.ask("Mot de passe", password=True)
        return email, password

    @staticmethod
    def show_success_login():
        """Affiche un message de connexion réussie"""
        console.print("[green bold]Connexion réussie ![/green bold]")

    @staticmethod
    def show_error_login():
        """Affiche un message d'erreur"""
        console.print("[red bold]Échec de l'authentification.[/red bold]")
