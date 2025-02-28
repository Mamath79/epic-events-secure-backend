from rich.console import Console
from rich.panel import Panel

console = Console()

class MenuView:
    @staticmethod
    def show_menu():
        console.print(Panel.fit("[bold blue]Menu Principal[/bold blue]"))
        console.print("[1] Gérer les Clients")
        console.print("[2] Gérer les Contrats")
        console.print("[3] Gérer les Événements")
        console.print("[4] Gérer les Utilisateurs")
        console.print("[0] Quitter")

        choice = console.input("[bold cyan]Sélectionnez une option > [/bold cyan]")

        return choice

