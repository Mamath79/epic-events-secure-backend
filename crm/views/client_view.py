from rich.console import Console
from rich.panel import Panel

console = Console()

class ClientView:
    @staticmethod
    def show_menu():
        console.print(Panel.fit("[bold blue]Menu Client[/bold blue]"))
        
        console.print("[1] Lister tous les Clients")
        console.print("[0] retour au menu principal")

        choice = console.input("[bold cyan]Sélectionnez une option > [/bold cyan]")

        return choice

