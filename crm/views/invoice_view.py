from rich.console import Console
from rich.panel import Panel

console = Console()

class InvoiceView:
    @staticmethod
    def show_menu():
        console.print(Panel.fit("[bold blue]Menu Facture[/bold blue]"))
        
        console.print("[1] Lister tous les Factures")
        # console.print("[2] Lister un Evenement par son Id")
        # console.print("[3] Créer un Evenement")
        # console.print("[4] Modifier un Evenement")
        # console.print("[5] Supprimer un Evenement")
        # console.print("[6] Afficher mes Evenements")

        console.print("[0] Retour au menu principal")

        choice = console.input("[bold cyan]Sélectionnez une option > [/bold cyan]")

        return choice