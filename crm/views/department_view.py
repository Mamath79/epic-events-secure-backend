from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()


class DepartmentView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des départements."""
        console.print("\n[bold cyan]╭───────────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Départements │[/bold cyan]")
        console.print("[bold cyan]╰───────────────────╯[/bold cyan]")
        console.print("\n[1] Lister tous les départements")
        console.print("[2] Voir un département par ID")
        console.print("[3] Créer un département")
        console.print("[4] Modifier un département")
        console.print("[5] Supprimer un département")
        console.print("[0] Retour au menu utilisateurs\n")

    @staticmethod
    def display_departments(departments):
        """Affiche tous les départements sous forme de tableau."""
        table = Table(title="\n[bold cyan]Liste des départements[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom", style="green", no_wrap=True)

        for department in departments:
            table.add_row(str(department.id), department.name)

        # Calcul de la largeur de la table
        table_width = console.measure(table).maximum

        # Affichage dynamique des séparateurs
        console.print("\n" + "═" * table_width, style="bold white")
        console.print(table)
        console.print("\n" + "═" * table_width, style="bold white")

    @staticmethod
    def display_department(department):
        """Affiche les détails d'un département sous forme de fiche détaillée."""
        department_details = f"""
        [cyan bold]Fiche Département[/cyan bold]

        ─────────────────

        [cyan bold]ID:[/cyan bold] {department.id}
        [green bold]Nom:[/green bold] {department.name}
        """

        console.print(
            Panel.fit(
                department_details,
                title="\n[bold cyan]Détails Département[/bold cyan]",
                style="white",
            )
        )

    @staticmethod
    def prompt_department_data():
        """Demande les informations pour créer un département."""
        console.print("\n[bold cyan]Création d'un nouveau département[/bold cyan]")
        name = Prompt.ask("\n[bold cyan]Nom du département[/bold cyan]").strip()

        while not name:
            name = Prompt.ask("[red]Nom requis, veuillez entrer un nom :[/red]").strip()

        return {"name": name}

    @staticmethod
    def prompt_department_update(department):
        """Demande les informations à modifier pour un département."""
        console.print(
            f"\n[bold cyan]Modification du département ID {department.id}[/bold cyan]"
        )

        new_name = Prompt.ask(
            f"Nom actuel : [green]{department.name}[/green] ➝ Nouveau nom",
            default=department.name,
        ).strip()

        if new_name == department.name:
            console.print("\n[yellow]Aucune modification effectuée.[/yellow]\n")
            return None

        return {"name": new_name}

    @staticmethod
    def display_message(message, msg_type="info"):
        """Affiche un message en fonction du type (success, error, info)."""
        colors = {"success": "green", "error": "red", "info": "cyan"}
        console.print(
            f"[{colors.get(msg_type, 'white')}] {message} [/{colors.get(msg_type, 'white')}]"
        )
