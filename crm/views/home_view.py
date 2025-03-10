from rich.console import Console
from rich.panel import Panel
import click

console = Console()


class HomeView:
    @staticmethod
    def show_menu():
        console.print(Panel.fit("[bold cyan]Menu Principal[/bold cyan]"))
        console.print("[1] Gérer les Clients")
        console.print("[2] Gérer les Contrats")
        console.print("[3] Gérer les Événements")
        console.print("[4] Gérer les Utilisateurs")
        console.print("[0] Quitter")

        choice = console.input("[bold cyan]Sélectionnez une option > [/bold cyan]")

        return choice

    @staticmethod
    def show_logout():
        click.echo("[bold cyan]Au revoir ![bold cyan]")

    @staticmethod
    def show_invalid_option():
        click.echo("[bold red]Invalid Options ![/bold red]")
