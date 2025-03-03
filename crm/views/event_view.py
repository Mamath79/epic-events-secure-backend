from rich.console import Console
from rich.panel import Panel

console = Console()

class EventView:
    @staticmethod
    def show_menu():
        console.print(Panel.fit("[bold blue]Menu Evenements[/bold blue]"))
        console.print("[1] Lister tous les Evenements")
        choice = console.input("[bold cyan]Sélectionnez une option > [/bold cyan]")

        return choice

