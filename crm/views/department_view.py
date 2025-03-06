from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class DepartmentView:
    
    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des départements."""
        console.print("\n📌 [bold cyan]Menu Départements[/bold cyan]")
        console.print("[1] Lister tous les Départements")
        console.print("[2] Voir un Département par ID")
        console.print("[3] Créer un Département")
        console.print("[4] Modifier un Département")
        console.print("[5] Supprimer un Département")
        console.print("[0] Retour au menu Utilisateurs")

    @staticmethod
    def display_departments(departments):
        """Affiche tous les départements sous forme de tableau."""
        table = Table(title="📌 Liste des Départements")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Nom", style="green")

        for department in departments:
            table.add_row(str(department.id), department.name)

        console.print(table)

    @staticmethod
    def display_department(department):
        """Affiche les détails d'un département spécifique."""
        console.print("\n📌 [bold cyan]Détails du Département[/bold cyan]")
        console.print(f"[cyan]ID :[/cyan] {department.id}")
        console.print(f"[green]Nom :[/green] {department.name}")

    @staticmethod
    def prompt_department_data():
        """Demande les informations pour créer un département."""
        name = Prompt.ask("[bold cyan]Nom du département[/bold cyan]").strip()
        if not name:
            console.print("[red]❌ Le nom du département est requis.[/red]")
            return None
        return {"name": name}

    @staticmethod
    def prompt_department_update(department):
        """Permet de modifier un département existant."""
        console.print(f"\n📌 Modification du département [cyan]{department.name}[/cyan]")

        new_name = Prompt.ask(f"Nom actuel : [green]{department.name}[/green] ➝ Nouveau nom", default=department.name).strip()
        if new_name == department.name:
            console.print("[yellow]⚠️ Aucune modification effectuée.[/yellow]")
            return None
        
        return {"name": new_name}
